#!/usr/bin/env python3
from polecat import __version__

import setuptools
import argparse
import os.path
import snakemake
import sys
import tempfile
import csv
import os
import yaml
from datetime import datetime
from Bio import SeqIO
import pkg_resources
from . import _program

from reportfunk.funks import io_functions as qcfunk
from reportfunk.funks import report_functions as rfunk
from reportfunk.funks import custom_logger as custom_logger
from reportfunk.funks import log_handler_handle as lh
import polecatfunks as pfunk

thisdir = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()

def main(sysargs = sys.argv[1:]):

    parser = argparse.ArgumentParser(prog = _program, 
    description='polecat: Phylogenetic Overview & Local Epidemiological Cluster Analysis Tool', 
    usage='''polecat -i <config.yaml> [options]''')

    io_group = parser.add_argument_group('input output options')
    io_group.add_argument('-i',"--input", action="store",help="Input config file", dest="input")
    io_group.add_argument('-t',"--tree",action="store",help="Input tree file", dest="tree")
    #io_group.add_argument('-m',"--metadata",action="store",help="Input metadata csv", dest="metadata")
    io_group.add_argument('-o','--outdir', action="store",help="Output directory. Default: current working directory")

    cluster_group = parser.add_argument_group('cluster options')
    cluster_group.add_argument('--criterion', action="store",help="Citerion to use to find optimal cluster. Default: none", dest="citerion")
    cluster_group.add_argument('--min-size', action='store',type=int,help="Minimum cluster size. Default: 5", dest="threshold")
    cluster_group.add_argument('--rank-by', action="store",help="Statistic to rank clusters by. Default: rate", dest="rank_by")
    cluster_group.add_argument('--number', action="store",help="Number of clusters to return. Default: 10", dest="rank_number")

    report_group = parser.add_argument_group('report options')
    report_group.add_argument('--report-fields', action="store",help="Comma-separated string of which statistics to include in the report. Default: most_recent_tip,tip_count,admin0_count,admin1_count", dest="report_fields")

    misc_group = parser.add_argument_group('misc options')
    misc_group.add_argument('--tempdir',action="store",help="Specify where you want the temporary stuff to go Default: $TMPDIR")
    misc_group.add_argument("--no-temp",action="store_true",help="Output all intermediate files")
    misc_group.add_argument("--verbose",action="store_true",help="Print lots of stuff to screen")
    misc_group.add_argument('--threads', action='store',dest="threads",type=int,help="Number of threads")
    misc_group.add_argument("-v","--version", action='version', version=f"polecat {__version__}")
    
    """
    Exit with help menu if no args supplied
    """
    if len(sysargs)<1: 
        parser.print_help()
        sys.exit(-1)
    else:
        args = parser.parse_args(sysargs)
    
    """
    Initialising dicts
    """
    # create the config dict to pass through to the snakemake file
    config = {}
    # get the default values from polecatfunks
    default_dict = pfunk.get_defaults()

    """
    Output directory 
    """
    # default output dir
    qcfunk.get_outdir(args.outdir,cwd,config)

    """
    Input file (-i/--input) 
    Valid inputs are config.yaml/config.yml
    
    """
    # find the query csv, or string of ids, or config file
    query,configfile = qcfunk.type_input_file(args.input,cwd,config)

    # if a yaml file is detected, add everything in it to the config dict
    if configfile:
        config = qcfunk.parse_yaml_file(configfile, config)
    
    
    """
    Get tempdir 
    Check if data has the right columns needed.
    The following rely on things that come out of the 
    input config or csv files so shouldnt be moved up above that.

    """
    
    # specifying temp directory, outdir if no_temp (tempdir becomes working dir)
    tempdir = qcfunk.get_temp_dir(args.tempdir, args.no_temp,cwd,config)


    """
    The query file could have been from one of
    - input.csv
    - id string input, created csv
    - from_metadata generated query csv

    (all either specified in config or via command line)
    """
    # check query exists or add ids to temp query file
    qcfunk.check_query_file(query, cwd, config)

    """
    Input fasta file 
    sourcing and qc checks
    """
    # find the query fasta
    qcfunk.get_query_fasta(args.fasta,cwd, config)
    
    # run qc on the input sequence file
    qcfunk.input_file_qc(args.minlen,args.maxambig,config,default_dict)


    """
    Parsing the tree_group arguments, 
    config or default options
    """

    # global now the only search option
    pfunk.define_seq_db(config,default_dict)

    # extraction radius configuration
    qcfunk.distance_config(args.distance,args.up_distance,args.down_distance,config,default_dict) 

    """
    Parsing the report_group arguments, 
    config or default options
    """
    
    # check if metadata has the right columns, background_metadata_header added to config
    pfunk.check_metadata_for_report_fields(config)


    for key in default_dict:
        if key not in config:
            config[key] = default_dict[key]

    """
    Miscellaneous options parsing

    """
    if args.launch_browser:
        config["launch_browser"]=True

    # don't run in quiet mode if verbose specified
    if args.verbose:
        quiet_mode = False
        config["log_string"] = ""
    else:
        quiet_mode = True
        lh_path = os.path.realpath(lh.__file__)
        config["log_string"] = f"--quiet --log-handler-script {lh_path} "


    threads = qcfunk.check_arg_config_default("threads",args.threads,config,default_dict)
    config["threads"]= int(threads)

    if args.generate_config:
        qcfunk.make_config_file("polecat_config.yaml",config)
    
    # find the master Snakefile
    snakefile = qcfunk.get_snakefile(thisdir)

    if args.verbose:
        
        for k in sorted(config):
            print(qcfunk.green(k), config[k])
        status = snakemake.snakemake(snakefile, printshellcmds=True, forceall=True, force_incomplete=True,
                                    workdir=tempdir,config=config, cores=threads,lock=False
                                    )
    else:
        logger = custom_logger.Logger()
        status = snakemake.snakemake(snakefile, printshellcmds=False, forceall=True,force_incomplete=True,workdir=tempdir,
                                    config=config, cores=threads,lock=False,quiet=True,log_handler=logger.log_handler
                                    )

    if status: # translate "success" into shell exit code of 0
       return 0

    return 1

if __name__ == '__main__':
    main()