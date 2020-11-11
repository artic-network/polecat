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
from datetime import date
from Bio import SeqIO
import pkg_resources
from . import _program

from reportfunk.funks import report_functions as rfunk
from reportfunk.funks import custom_logger as custom_logger
from reportfunk.funks import log_handler_handle as lh
import polecatfunks as pfunk

thisdir = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()

def main(sysargs = sys.argv[1:]):

    parser = argparse.ArgumentParser(prog = _program, 
    description=pfunk.preamble(), 
    usage='''polecat -i <config.yaml> [options]''')

    io_group = parser.add_argument_group('input output options')
    io_group.add_argument('-c',"--config", action="store",help="Input config file", dest="config")
    io_group.add_argument('--outdir', action="store",help="Output directory. Default: current working directory")
    io_group.add_argument('-o','--output-prefix', action="store",help="Output prefix. Default: polecat",dest="output_prefix")

    data_group = parser.add_argument_group('data source options')
    data_group.add_argument('-d','--datadir', action="store",help="Local directory that contains the data files. Default: civet-cat")
    data_group.add_argument("-m","--background-metadata",action="store",dest="background_metadata",help="Custom metadata file that corresponds to the large global tree/ alignment. Should have a column `sequence_name`.")
    data_group.add_argument('--CLIMB', action="store_true",dest="climb",help="Indicates you're running CIVET from within CLIMB, uses default paths in CLIMB to access data")
    data_group.add_argument("-r",'--remote', action="store_true",dest="remote",help="Remotely access lineage trees from CLIMB")
    data_group.add_argument("-uun","--your-user-name", action="store", help="Your CLIMB COG-UK username. Required if running with --remote flag", dest="uun")
    data_group.add_argument('--data-column', action="store",help="Option to search COG database for a different id type. Default: COG-UK ID", dest="data_column")

    cluster_group = parser.add_argument_group('cluster options')
    cluster_group.add_argument('--max-age', action="store",help="Maximum age of a cluster. Default: none", dest="max_age")
    cluster_group.add_argument('--max-count', action="store",help="Maximum number of clusters to report. Default: all", dest="max_count")
    cluster_group.add_argument('--max-recency', action="store",help="Maximum recency of a cluster. Default: none", dest="max_recency")
    cluster_group.add_argument('--max-size', action="store",help="Maximum number of tips in a subcluster. Default: none", dest="max_size")
    cluster_group.add_argument('--min-size', action='store',type=int,help="Minimum cluster size. Default: 5", dest="min_size")
    cluster_group.add_argument('--min-UK', action='store',type=int,help="Minimum proportion of UK tips. Default: none", dest="min_UK")
    cluster_group.add_argument('--optimize-by', action="store",help="Citerion to use to find optimal cluster. Default: none", dest="optimize_by")
    cluster_group.add_argument('--rank-by', action="store",help="Statistic to rank clusters by. Default: rate", dest="rank_by")

    report_group = parser.add_argument_group('report options')
    report_group.add_argument('--stats', action="store",help="Comma-separated string of which columns to include in the cluster tables. Default: sequence_name,lineage,country", dest="stats")
    report_group.add_argument("--background-fields",help="Comma-separated string of to include in metadata tooltips",dest="background_fields")

    misc_group = parser.add_argument_group('misc options')
    misc_group.add_argument('-b','--launch-browser', action="store_true",help="Optionally launch md viewer in the browser using grip",dest="launch_browser")
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

    # get the default values from polecatfunks
    config = pfunk.get_defaults()

    """
    Valid inputs are config.yaml/config.yml
    
    """
    # find config file
    pfunk.add_arg_to_config("config",args.config,config)

    # if a yaml file is detected, add everything in it to the config dict
    if config["config"]:
        pfunk.parse_yaml_file(config["config"], config)
    
    """
    Output directory 
    """
    # default output dir
    pfunk.get_outdir(args.outdir,args.output_prefix,cwd,config)

    """
    Get tempdir 
    """
    
    # specifying temp directory, outdir if no_temp (tempdir becomes working dir)
    tempdir = pfunk.get_temp_dir(args.tempdir, args.no_temp,cwd,config)

    """
    Parsing the cluster_group arguments, 
    config options
    """
    
    pfunk.cluster_group_to_config(args,config)

    """
    Data dir finding or rsyncing
    """

    pfunk.add_arg_to_config("remote",args.remote, config)

    pfunk.get_datadir(args.climb,args.uun,args.datadir,args.background_metadata,cwd,config)

    # add data column to config
    pfunk.add_arg_to_config("data_column",args.data_column, config)


    """
    Parsing the report_group arguments, 
    config options
    """
    template = pkg_resources.resource_filename('polecat', 'data/html_template.mako')
    command = " ".join(sys.argv[1:])
    config["command"] = f"polecat {command}"

    config["template"] = template
    pfunk.add_arg_to_config("stats",args.stats, config)
    pfunk.add_arg_to_config("background_fields",args.background_fields, config)

    # check if metadata has the right columns, background_metadata_header added to config
    pfunk.check_metadata_for_stat_fields(config)
    pfunk.check_metadata_for_background_fields(config)

    """
    Miscellaneous options parsing

    """
    pfunk.add_arg_to_config("launch_browser",args.launch_browser,config)

    # don't run in quiet mode if verbose specified
    if args.verbose:
        quiet_mode = False
        config["log_string"] = ""
    else:
        quiet_mode = True
        lh_path = os.path.realpath(lh.__file__)
        config["log_string"] = f"--quiet --log-handler-script {lh_path} "

    
    pfunk.add_arg_to_config("threads",args.threads,config)
    
    try:
        config["threads"]= int(config["threads"])
    except:
        sys.stderr.write(pfunk.cyan('Error: Please specifiy an integer for variable `threads`.\n'))
        sys.exit(-1)
    threads = config["threads"]


    # find the master Snakefile
    snakefile = pfunk.get_snakefile(thisdir)

    if args.verbose:
        
        for k in sorted(config):
            print(pfunk.green(k), config[k])
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