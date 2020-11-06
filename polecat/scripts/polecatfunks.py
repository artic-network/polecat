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

from reportfunk.funks import io_functions as qcfunk
from reportfunk.funks import tree_functions as tree_funk

def get_defaults():
    default_dict = {"threads":1,
                    "max_age":"",
                    "max_count":"",
                    "max_recency":"",
                    "max_size":"",
                    "min_size":"",
                    "stats":"node_number,day_range,growth_rate,tip_count,lineage,uk_lineage",
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
    
    qcfunk.add_arg_to_config("output_prefix",output_prefix_arg, config)
    
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
    figure_output = os.path.join(report_output, "figures")
    if not os.path.exists(figure_output):
        os.mkdir(figure_output)

    print(qcfunk.green(f"Output dir:") + f" {outdir}")
    config["outdir"] = outdir 
    config["rel_outdir"] = os.path.join(".",rel_outdir) 
        
def qc_cluster_arg(key,arg,type_var,config):
    if config[key]:
        var = config[key]
        try:
            var = type_var(var)
            config[key] = f"{arg} {var}"
        except:
            sys.stderr.write(qcfunk.cyan(f"Error: {arg} must be {type_var}\n"))
            sys.exit(-1)
    else:
        config[key] = ""

def cluster_group_to_config(args,config):
    ## max_age
    qcfunk.add_arg_to_config("max_age",args.max_age, config)
    qc_cluster_arg("max_age","--max-age",int,config)

    ## max_count
    qcfunk.add_arg_to_config("max_count",args.max_count, config)
    qc_cluster_arg("max_count","--max-count",int,config)

    ## max_recency
    qcfunk.add_arg_to_config("max_recency",args.max_recency, config)
    qc_cluster_arg("max_recency","--max-recency",int,config)

    ## max_size
    qcfunk.add_arg_to_config("max_size",args.max_size, config)
    qc_cluster_arg("max_size","--max-size",int,config)

    ## min_size
    qcfunk.add_arg_to_config("min_size",args.min_size, config)
    qc_cluster_arg("min_size","--min-size",int,config)

    ## min_UK
    qcfunk.add_arg_to_config("min_UK",args.min_UK, config)
    qc_cluster_arg("min_UK","--min-UK",float,config)

    ## optimize_by
    qcfunk.add_arg_to_config("optimize_by",args.optimize_by, config)
    qc_cluster_arg("optimize_by","--optimize-by",str,config)

    ## rank_by
    qcfunk.add_arg_to_config("rank_by",args.rank_by, config)
    qc_cluster_arg("rank_by","--rank-by",str,config)

def report_group_to_config(args,config):
    ## summary_fields
    qcfunk.add_arg_to_config("summary_fields",args.summary_fields, config)

    ## cluster_fields
    qcfunk.add_arg_to_config("cluster_fields",args.cluster_fields, config)
        
    # ## display_name
    # qcfunk.add_arg_to_config("display_name", args.display_name, config)
    
    # ## colour_by
    # qcfunk.add_arg_to_config("colour_by",args.colour_by, config)

    # ## tree_fields
    # qcfunk.add_arg_to_config("tree_fields",args.tree_fields, config)

    # ## label_fields
    # qcfunk.add_arg_to_config("label_fields",args.label_fields, config)

    # ##date_fields
    # qcfunk.add_arg_to_config("date_fields", args.date_fields, config)

    # ##sample date column
    # qcfunk.add_arg_to_config("sample_date_column", args.sample_date_column,config)
    # qcfunk.add_arg_to_config("database_sample_date_column", args.database_sample_date_column, config)

    # ## node-summary
    # qcfunk.add_arg_to_config("node_summary",args.node_summary, config)

def get_stat_list():
    return "node_number,parent_number,most_recent_tip,least_recent_tip,day_range,persistence,recency,age,tip_count,uk_tip_count,uk_child_count,uk_chain_count,identical_count,divergence_ratio,mean_tip_divergence,stem_length,growth_rate,lineage,uk_lineage,proportion_uk,admin0_count,admin1_count,admin2_count,admin0_mode,admin1_mode,admin2_mode,admin1_entropy,admin2_entropy,tips".split(",")

def check_metadata_for_stat_fields(config):

    stat_list = get_stat_list()

    show_stats = config["stats"].split(",")

    for stat in show_stats:
        if stat not in stat_list:
            sys.stderr.write(qcfunk.cyan(f'Error: {stat} not a valid polecat statistic\n'))
            sys.exit(-1)


def print_data_error(data_dir):
    sys.stderr.write(qcfunk.cyan(f"Error: data directory should contain the following files or additionally supply a background metadata file:\n") + f"\
    - cog_global_2020-XX-YY_tree.nexus\n\
    - cog_global_2020-XX-YY_metadata.csv\n\
    - cog_global_2020-XX-YY_alignment.fasta\n"+qcfunk.cyan(f"\
To run civet please either\n1) ssh into CLIMB and run with --CLIMB flag\n\
2) Run using `--remote` flag and your CLIMB username specified e.g. `-uun climb-covid19-smithj`\n\
3) Specify a local directory with the appropriate files, optionally supply a custom metadata file\n\n"""))

def rsync_data_from_climb(uun, data_dir):
    rsync_command = f"rsync -avzh --exclude 'cog' --delete-after {uun}@bham.covid19.climb.ac.uk:/cephfs/covid/bham/results/phylogenetics/latest/civet/ '{data_dir}'"
    print(qcfunk.green(f"Syncing civet data to {data_dir}"))
    status = os.system(rsync_command)
    if status != 0:
        sys.stderr.write(qcfunk.cyan("Error: rsync command failed.\nCheck your user name is a valid CLIMB username e.g. climb-covid19-smithj\nAlso, check if you have access to CLIMB from this machine and are in the UK\n\n"))
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
            elif fn.endswith(".nexus") and fn.startswith("cog_global_"):
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
            sys.stderr.write(qcfunk.cyan("Error: rsync command failed.\nCheck your ssh is configured with Host bham.covid19.climb.ac.uk\nAlternatively enter your CLIMB username with -uun e.g. climb-covid19-smithj\nAlso, check if you have access to CLIMB from this machine and check if you are in the UK\n\n"))
            sys.exit(-1)

    background_seqs, background_tree, background_metadata, data_date = get_background_files(data_dir,background_metadata)

    config["datadir"] = data_dir
    config["data_date"] = data_date
    if not os.path.exists(config["datadir"]):
        print(qcfunk.cyan(f"Error: data directory not found at {data_dir}.\n"))
        sys.exit(-1)

    if not os.path.isfile(background_tree) or not os.path.isfile(background_seqs) or not os.path.isfile(background_metadata):
        print_data_error(data_dir)
        sys.exit(-1)
    else:
        config["background_metadata"] = background_metadata
        config["background_seqs"] = background_seqs
        config["background_tree"] = background_tree

        print(qcfunk.green("Found data:"))
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
            sys.stderr.write(qcfunk.cyan(f"Error: can't find metadata file at {background_metadata}.\n"))
            sys.exit(-1)

    elif "background_metadata" in config:
        if config["background_metadata"]:
            expanded_path = os.path.expanduser(config["background_metadata"])
            background_metadata = os.path.join(config["path_to_query"], expanded_path)
            if not os.path.exists(background_metadata):
                sys.stderr.write(qcfunk.cyan(f"Error: can't find metadata file at {background_metadata}.\n"))
                sys.exit(-1)
            
    if args_climb:
        data_dir = "/cephfs/covid/bham/results/phylogenetics/latest/civet/cog"
        if os.path.exists(data_dir):
            config["remote"] = False
            config["username"] = ""
        else:
            sys.stderr.write(qcfunk.cyan(f"Error: --CLIMB argument called, but CLIMB data path doesn't exist.\n"))
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

            print("Found data:")
            print("    -",background_seqs)
            print("    -",background_metadata)
            print("    -",background_tree,"\n")

    elif remote:
        
        get_remote_data(args_uun, background_metadata, data_dir, config)

    config["datadir"]=data_dir


def make_all_of_the_trees(treedir, tree_name_stem, taxon_dict,config):

    tallest_height = tree_funk.find_tallest_tree(treedir)
    config["tallest_height"] = tallest_height

    trees = []
    for r,d,f in os.walk(treedir):
        for fn in f:
            if fn.endswith(".tree"):
                tree_name = ".".join(fn.split(".")[:-1])
                trees.append((os.path.join(r,fn), tree_name))
    
    tree_to_num_tips = {}
    num_tips = 0
    for treefile,tree_name in trees:

        with open(treefile,"r") as f:
            for l in f:
                l = l.rstrip("\n")
                if l.startswith(" Dimensions NTax="):
                    num_tips = int(l.rstrip(";").split("=")[1])
                    tree_to_num_tips[treefile] = num_tips

        if num_tips > 1: 
            tree = bt.loadNewick(treefile, absoluteTime=False)

            #make root line
            old_node = tree.root
            new_node = bt.node()
            new_node.children.append(old_node)
            old_node.parent = new_node
            old_node.length=0.000015
            new_node.height = 0
            new_node.y = old_node.y
            tree.root = new_node

            tree.Objects.append(new_node)

            overall_tree_count += 1      
            
            if len(tips) < 500:
                outfile = os.path.join(config["figdir"], f"{tree_name}.svg")
                make_cluster_tree(tree, tree_name, num_tips, taxon_dict,outfile,config)     
            