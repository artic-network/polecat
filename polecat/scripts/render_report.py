#!/usr/bin/env python3
import os
import argparse

from polecat import __version__
from datetime import date

from mako.template import Template
from mako.runtime import Context
from mako.exceptions import RichTraceback
from io import StringIO
import json

import csv



def parse_args():
    parser = argparse.ArgumentParser(description="Report generator script")
    parser.add_argument("--metadata", required=True, help="metadata file", dest="metadata")
    parser.add_argument("--background-metadata", required=True, help="background metadata file", dest="background_metadata")
    parser.add_argument("--command",help="command string", dest="command")
    parser.add_argument("--background-fields",help="stats to include in metadata tooltips",dest="background_fields")
    parser.add_argument("--include-stats",help="stats to include in detailed table",dest="include_stats")
    parser.add_argument("--template",help="template mako html",dest="template")
    parser.add_argument("--report", help="output report file", dest="report")
    parser.add_argument("--tree-dir",help="path to trees",dest="tree_dir")
    return parser.parse_args()

def make_summary_data(metadata):
    summary_data = []
    with open(metadata, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cluster_dict = {"cluster_no":row["node_id"],
                            "most_recent_tip": row["most_recent_tip"], 
                            "tip_count": row["tip_count"],
                            "admin0_count":row["admin0_count"],
                            "admin1_count": row["admin1_count"],
                            "admin2_count": row["admin2_count"]}
            summary_data.append(cluster_dict)
    return summary_data

def make_background_metadata(background_metadata,background_fields):
    background_data = {}
    with open(background_metadata, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cluster_dict = {}
            for field in background_fields:
                cluster_dict[field] = row[field]
            background_data[row["sequence_name"]] = cluster_dict
    data = json.dumps(background_data) 
    return data

def make_cluster_data(metadata,include_stats,tree_dir):
    cluster_data = []
    with open(metadata, "r") as f:
        reader = csv.DictReader(f)
        table_no = 1
        for row in reader:

            table_no += 1
            
            cluster_no = row["node_id"]

            stats = []
            for stat in include_stats:
                info = row[stat]
                try:
                    info = float(info)
                    round_info = round(info, 2)
                except:
                    round_info = info
                stats.append({
                    "statistic": stat,
                    "information": round_info
                })

            treeString = ""
            tree_file = os.path.join(tree_dir, f"{cluster_no}",f"{cluster_no}_subtree_1.newick")
            if not os.path.isfile(tree_file):
                print("not a tree file", tree_file)
                sys.exit(-1)
            with open(tree_file,"r") as f:
                for l in f:
                    treeString = l.rstrip("\n")

            cluster_data.append({
                "cluster_no":cluster_no,
                "table_no":table_no,
                "stats":stats,
                "treeString":treeString
            })
    return cluster_data

def make_report():

    args = parse_args()

    summary_data = make_summary_data(args.metadata)

    include_stats = args.include_stats.split(",")
    cluster_data = make_cluster_data(args.metadata, include_stats, args.tree_dir)

    background_fields = args.background_fields.split(",")
    background_data = make_background_metadata(args.background_metadata,background_fields)

    today = date.today()
    

    mytemplate = Template(filename=args.template)
    buf = StringIO()

    ctx = Context(buf, command = args.command, date = today, version = __version__, summary_data = summary_data, cluster_data = cluster_data, background_data = background_data)


    try:
    
        mytemplate.render_context(ctx)
    except:
        traceback = RichTraceback()
        for (filename, lineno, function, line) in traceback.traceback:
            print("File %s, line %s, in %s" % (filename, lineno, function))
            print(line, "\n")
        print("%s: %s" % (str(traceback.error.__class__.__name__), traceback.error))

    with open(args.report,"w") as fw:
        fw.write(buf.getvalue())

if __name__ == "__main__":
    make_report()

