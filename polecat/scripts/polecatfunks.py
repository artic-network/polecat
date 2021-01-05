#!/usr/bin/env python3

import os
import argparse
import csv 
import sys
from Bio import SeqIO
from datetime import datetime 
from datetime import date

import tempfile
import pkg_resources
import yaml



END_FORMATTING = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[93m'
CYAN = '\u001b[36m'
DIM = '\033[2m'

def get_defaults():
    default_dict = {"threads":1,
                    "max_age":"",
                    "max_count":"",
                    "max_recency":"",
                    "max_size":"",
                    "min_size":"",
                    "stats":"node_number,day_range,growth_rate,tip_count,lineage,uk_lineage",
                    "background_fields":"sequence_name,sample_date,epi_week,country,adm2,uk_lineage,lineage,phylotype",
                    "command":"",
                    "min_UK":"",
                    "optimize_by":"",
                    "rank_by":"growth-rate",
                    "sample_date_column":"sample_date",
                    "database_sample_date_column":"sample_date",
                    "display_name":False,
                    "tree_fields":"country",
                    "node_summary":"country",
                    "colour_by":"country=Paired",
                    "label_fields":False,
                    "date_fields":False,
                    "test":"/Users/s1680070/repositories/polecat/polecat/tests/test.csv",                  
                    "CLIMB":False,
                    "remote":False,
                    "config":False,
                    "data_column":"sequence_name",
                    "output_prefix":"polecat",
                    "summary_fields":"node_number,most_recent_tip,tip_count,admin0_count,admin1_count",
                    "cluster_fields":"node_number,day_range,tip_count,uk_tip_count,uk_chain_count,identical_count",
                    "no_temp":False,
                    "force":True,
                    "launch_browser":False,
                    "safety_level":0
                    }
    return default_dict

def make_timestamped_outdir(cwd,outdir,config):

    output_prefix = config["output_prefix"]
    split_prefix = output_prefix.split("_")
    if split_prefix[-1].startswith("20"):
        output_prefix = '_'.join(split_prefix[:-1])
    config["output_prefix"] = output_prefix
    timestamp = str(datetime.now().isoformat(timespec='milliseconds')).replace(":","").replace(".","").replace("T","-")
    outdir = os.path.join(cwd, f"{output_prefix}_{timestamp}")
    rel_outdir = os.path.join(".",timestamp)

    return outdir, rel_outdir

def get_outdir(outdir_arg,output_prefix_arg,cwd,config):
    outdir = ''
    
    add_arg_to_config("output_prefix",output_prefix_arg, config)
    
    if outdir_arg:
        expanded_path = os.path.expanduser(outdir_arg)
        outdir = os.path.join(cwd,expanded_path)
        rel_outdir = os.path.relpath(outdir, cwd) 

    elif "outdir" in config:
        expanded_path = os.path.expanduser(config["outdir"])
        outdir = os.path.join(config["path_to_query"],expanded_path)
        rel_outdir = os.path.relpath(outdir, cwd) 

    else:
        outdir, rel_outdir = make_timestamped_outdir(cwd,outdir,config)
    
    today = date.today()
    
    d = today.strftime("%Y-%m-%d")
    config["today"] = f"{d}"
    output_prefix = config["output_prefix"]
    split_prefix = output_prefix.split("_")
    if split_prefix[-1].startswith("20"):
        output_prefix = '_'.join(split_prefix[:-1])
    config["output_prefix"] = f"{output_prefix}_{d}"

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    report_output = os.path.join(outdir, "report")
    if not os.path.exists(report_output):
        os.mkdir(report_output)

    print(green(f"Output dir:") + f" {outdir}")
    config["outdir"] = outdir 
    config["rel_outdir"] = os.path.join(".",rel_outdir) 
        
def qc_cluster_arg(key,arg,type_var,config):
    if config[key]:
        var = config[key]
        try:
            var = type_var(var)
            config[key] = f"{arg} {var}"
        except:
            sys.stderr.write(cyan(f"Error: {arg} must be {type_var}\n"))
            sys.exit(-1)
    else:
        config[key] = ""

def get_snakefile(thisdir):
    snakefile = os.path.join(thisdir, 'scripts','Snakefile')
    if not os.path.exists(snakefile):
        sys.stderr.write(cyan(f'Error: cannot find Snakefile at {snakefile}\n Check installation\n'))
        sys.exit(-1)
    return snakefile

def get_temp_dir(tempdir_arg,no_temp_arg, cwd,config):
    tempdir = ''
    outdir = config["outdir"]
    if no_temp_arg:
        print(green(f"--no-temp:") + f" All intermediate files will be written to {outdir}")
        tempdir = outdir
        config["no_temp"] = no_temp_arg
    elif config["no_temp"]:
        print(green(f"--no-temp:") + f" All intermediate files will be written to {outdir}")
        tempdir = outdir
    elif tempdir_arg:
        expanded_path = os.path.expanduser(tempdir_arg)
        to_be_dir = os.path.join(cwd,expanded_path)
        if not os.path.exists(to_be_dir):
            os.mkdir(to_be_dir)
        temporary_directory = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=to_be_dir)
        tempdir = temporary_directory.name

    elif "tempdir" in config:
        expanded_path = os.path.expanduser(config["tempdir"])
        to_be_dir = os.path.join(cwd,expanded_path)
        if not os.path.exists(to_be_dir):
            os.mkdir(to_be_dir)
        temporary_directory = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=to_be_dir)
        tempdir = temporary_directory.name

    else:
        temporary_directory = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
        tempdir = temporary_directory.name
    
    config["tempdir"] = tempdir 
    return tempdir
    
def parse_yaml_file(configfile,config):
    with open(configfile,"r") as f:
        input_config = yaml.load(f, Loader=yaml.FullLoader)
        for key in input_config:
            snakecase_key = key.replace("-","_")
            config[snakecase_key] = input_config[key]

def add_arg_to_config(key,arg,config):
    if arg:
        config[key] = arg

def cluster_group_to_config(args,config):
    ## max_age
    add_arg_to_config("max_age",args.max_age, config)
    qc_cluster_arg("max_age","--max-age",int,config)

    ## max_count
    add_arg_to_config("max_count",args.max_count, config)
    qc_cluster_arg("max_count","--max-count",int,config)

    ## max_recency
    add_arg_to_config("max_recency",args.max_recency, config)
    qc_cluster_arg("max_recency","--max-recency",int,config)

    ## max_size
    add_arg_to_config("max_size",args.max_size, config)
    qc_cluster_arg("max_size","--max-size",int,config)

    ## min_size
    add_arg_to_config("min_size",args.min_size, config)
    qc_cluster_arg("min_size","--min-size",int,config)

    ## min_UK
    add_arg_to_config("min_UK",args.min_UK, config)
    qc_cluster_arg("min_UK","--min-UK",float,config)

    ## optimize_by
    add_arg_to_config("optimize_by",args.optimize_by, config)
    qc_cluster_arg("optimize_by","--optimize-by",str,config)

    ## rank_by
    add_arg_to_config("rank_by",args.rank_by, config)
    qc_cluster_arg("rank_by","--rank-by",str,config)

def report_group_to_config(args,config):
    ## summary_fields
    add_arg_to_config("summary_fields",args.summary_fields, config)

    ## cluster_fields
    add_arg_to_config("cluster_fields",args.cluster_fields, config)
        

def get_stat_list():
    return "node_number,parent_number,most_recent_tip,least_recent_tip,day_range,persistence,recency,age,tip_count,uk_tip_count,uk_child_count,uk_chain_count,identical_count,divergence_ratio,mean_tip_divergence,stem_length,growth_rate,lineage,uk_lineage,proportion_uk,admin0_count,admin1_count,admin2_count,admin0_mode,admin1_mode,admin2_mode,admin1_entropy,admin2_entropy,tips".split(",")

def check_metadata_for_stat_fields(config):

    stat_list = get_stat_list()

    show_stats = config["stats"].split(",")

    for stat in show_stats:
        if stat not in stat_list:
            sys.stderr.write(cyan(f'Error: {stat} not a valid polecat statistic\n'))
            sys.exit(-1)

def check_metadata_for_background_fields(config):

    with open(config["background_metadata"],"r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames


        background_fields = config["background_fields"].split(",")

        if "sequence_name" not in header:
            sys.stderr.write(cyan(f'Error: "sequence_name" is a required field in background metadata\n'))
            sys.exit(-1)

        for field in background_fields:
            if field not in header:
                sys.stderr.write(cyan(f'Error: {field} not present in background metadata\n'))
                sys.exit(-1)


def print_data_error(data_dir):
    sys.stderr.write(cyan(f"Error: data directory should contain the following files or additionally supply a background metadata file:\n") + f"\
    - cog_global_2020-XX-YY_tree.newick\n\
    - cog_global_2020-XX-YY_metadata.csv\n\
    - cog_global_2020-XX-YY_alignment.fasta\n"+cyan(f"\
To run civet please either\n1) ssh into CLIMB and run with --CLIMB flag\n\
2) Run using `--remote` flag and your CLIMB username specified e.g. `-uun climb-covid19-smithj`\n\
3) Specify a local directory with the appropriate files, optionally supply a custom metadata file\n\n"""))

def rsync_data_from_climb(uun, data_dir):
    rsync_command = f"rsync -avzh --exclude 'cog' --delete-after {uun}@bham.covid19.climb.ac.uk:/cephfs/covid/bham/results/phylogenetics/latest/civet/ '{data_dir}'"
    print(green(f"Syncing civet data to {data_dir}"))
    status = os.system(rsync_command)
    if status != 0:
        sys.stderr.write(cyan("Error: rsync command failed.\nCheck your user name is a valid CLIMB username e.g. climb-covid19-smithj\nAlso, check if you have access to CLIMB from this machine and are in the UK\n\n"))
        sys.exit(-1)

def get_background_files(data_dir,background_metadata):
    background_seqs = ""
    background_tree = ""
    data_date = ""
    for r,d,f in os.walk(data_dir):
        for fn in f:
            if fn.endswith(".fasta") and fn.startswith("cog_global_"):
                background_seqs = os.path.join(data_dir, fn)
                data_date = fn.split("_")[2]
                if not data_date.startswith("20"):
                    data_date = ""
            elif fn.endswith(".newick") and fn.startswith("cog_global_"):
                background_tree = os.path.join(data_dir, fn)
            elif background_metadata == "" and fn.endswith(".csv") and fn.startswith("cog_global_"):
                background_metadata = os.path.join(data_dir, fn)

    return background_seqs, background_tree, background_metadata, data_date
    

def get_remote_data(uun,background_metadata,data_dir,config):
    config["remote"]= True

    if uun:
        config["username"] = uun
        rsync_data_from_climb(uun, data_dir)
    elif "username" in config:
        uun = config["username"]
        rsync_data_from_climb(uun, data_dir)
    elif "uun" in config:
        uun = config["uun"]
        rsync_data_from_climb(uun, data_dir)
    else:
        rsync_command = f"rsync -avzh --exclude 'cog' --delete-after  bham.covid19.climb.ac.uk:/cephfs/covid/bham/results/phylogenetics/latest/civet/ '{data_dir}'"
        print(f"Syncing civet data to {data_dir}")
        status = os.system(rsync_command)
        if status != 0:
            sys.stderr.write(cyan("Error: rsync command failed.\nCheck your ssh is configured with Host bham.covid19.climb.ac.uk\nAlternatively enter your CLIMB username with -uun e.g. climb-covid19-smithj\nAlso, check if you have access to CLIMB from this machine and check if you are in the UK\n\n"))
            sys.exit(-1)

    background_seqs, background_tree, background_metadata, data_date = get_background_files(data_dir,background_metadata)

    config["datadir"] = data_dir
    config["data_date"] = data_date
    if not os.path.exists(config["datadir"]):
        print(cyan(f"Error: data directory not found at {data_dir}.\n"))
        sys.exit(-1)

    if not os.path.isfile(background_tree) or not os.path.isfile(background_seqs) or not os.path.isfile(background_metadata):
        print_data_error(data_dir)
        sys.exit(-1)
    else:
        config["background_metadata"] = background_metadata
        config["background_seqs"] = background_seqs
        config["background_tree"] = background_tree

        print(green("Found data:"))
        print("    -",background_seqs)
        print("    -",background_metadata)
        print("    -",background_tree,"\n")

def get_datadir(args_climb,args_uun,args_datadir,args_metadata,cwd,config):
    data_dir = ""
    background_metadata = ""
    remote= config["remote"]

    if args_metadata:
        expanded_path = os.path.expanduser(args_metadata)
        background_metadata = os.path.join(cwd, expanded_path)
        if not os.path.exists(background_metadata):
            sys.stderr.write(cyan(f"Error: can't find metadata file at {background_metadata}.\n"))
            sys.exit(-1)

    elif "background_metadata" in config:
        if config["background_metadata"]:
            expanded_path = os.path.expanduser(config["background_metadata"])
            background_metadata = os.path.join(config["path_to_query"], expanded_path)
            if not os.path.exists(background_metadata):
                sys.stderr.write(cyan(f"Error: can't find metadata file at {background_metadata}.\n"))
                sys.exit(-1)
            
    if args_climb:
        data_dir = "/cephfs/covid/bham/results/phylogenetics/latest/civet/cog"
        if os.path.exists(data_dir):
            config["remote"] = False
            config["username"] = ""
        else:
            sys.stderr.write(cyan(f"Error: --CLIMB argument called, but CLIMB data path doesn't exist.\n"))
            sys.exit(-1)

    elif args_datadir:
        data_dir = os.path.join(cwd, args_datadir)

    elif "datadir" in config:
        if config["datadir"]:
            expanded_path = os.path.expanduser(config["datadir"])
            data_dir = os.path.join(config["path_to_query"], expanded_path)
        else:
            data_dir = os.path.join(cwd, "civet-cat")


    if not remote:
        if not os.path.exists(data_dir):
            print_data_error(data_dir)
            sys.exit(-1)
            
        background_seqs, background_tree, background_metadata, data_date = get_background_files(data_dir,background_metadata)

        config["datadir"] = data_dir
        config["data_date"] = data_date

        if not os.path.isfile(background_tree) or not os.path.isfile(background_seqs) or not os.path.isfile(background_metadata):
            print_data_error(data_dir)
            sys.exit(-1)
        else:
            config["background_metadata"] = background_metadata
            config["background_seqs"] = background_seqs
            config["background_tree"] = background_tree

            print(green("Found data:"))
            print("    -",background_seqs)
            print("    -",background_metadata)
            print("    -",background_tree,"\n")

    elif remote:
        
        get_remote_data(args_uun, background_metadata, data_dir, config)

    config["datadir"]=data_dir

def preamble():
    print(green("""\n
                               __                        __   
                ______   ____ |  |   ____   ____    ____/  |_ 
                \____ \ /    \|  |  / __ \_/ ___\  /  \    __|
                |  |_\ |   |  |  |_\  ___/\  \___ / __ \|  |   
                |   __/ \____/|____/\____/ \____/ ____  /__|  
                |__|                                          

                            Phylogenetic Overview 
                                        & 
                    Local Epidemiological Cluster Analysis Tool 

                    ****************************************

                    JT McCrone, Aine O'Toole & Andrew Rambaut  
                                    Rambaut Group              
                                Edinburgh University          
                """))


def colour(text, text_colour):
    bold_text = 'bold' in text_colour
    text_colour = text_colour.replace('bold', '')
    underline_text = 'underline' in text_colour
    text_colour = text_colour.replace('underline', '')
    text_colour = text_colour.replace('_', '')
    text_colour = text_colour.replace(' ', '')
    text_colour = text_colour.lower()
    if 'red' in text_colour:
        coloured_text = RED
    elif 'green' in text_colour:
        coloured_text = GREEN
    elif 'yellow' in text_colour:
        coloured_text = YELLOW
    elif 'dim' in text_colour:
        coloured_text = DIM
    elif 'cyan' in text_colour:
        coloured_text = 'cyan'
    else:
        coloured_text = ''
    if bold_text:
        coloured_text += BOLD
    if underline_text:
        coloured_text += UNDERLINE
    if not coloured_text:
        return text
    coloured_text += text + END_FORMATTING
    return coloured_text

def red(text):
    return RED + text + END_FORMATTING

def cyan(text):
    return CYAN + text + END_FORMATTING

def green(text):
    return GREEN + text + END_FORMATTING

def yellow(text):
    return YELLOW + text + END_FORMATTING

def bold_underline(text):
    return BOLD + UNDERLINE + text + END_FORMATTING
