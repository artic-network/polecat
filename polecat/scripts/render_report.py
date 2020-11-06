#!/usr/bin/env python3
import os
import argparse

from polecat import __version__
from datetime import date

from mako.template import Template
from mako.runtime import Context
from io import StringIO


import csv



def parse_args():
    parser = argparse.ArgumentParser(description="Report generator script")
    parser.add_argument("--metadata", required=True, help="metadata file", dest="metadata")
    parser.add_argument("--command",help="command string", dest="command")
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
            cluster_dict = {"cluster_no":row["node_number"],
                            "most_recent_tip": row["most_recent_tip"], 
                            "tip_count": row["tip_count"],
                            "admin0_count":row["admin0_count"],
                            "admin1_count": row["admin1_count"],
                            "admin2_count": row["admin2_count"]}
            summary_data.append(cluster_dict)
    return summary_data

def make_cluster_data(metadata,include_stats,tree_dir):
    cluster_data = []
    with open(metadata, "r") as f:
        reader = csv.DictReader(f)
        table_no = 1
        for row in reader:

            table_no += 1
            
            cluster_no = row["node_number"]

            stats = []
            for stat in include_stats:
                stats.append({
                    "statistic": stat,
                    "information": row[stat]
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

    today = date.today()
    

    mytemplate = Template(filename=args.template)
    buf = StringIO()

    ctx = Context(buf, command = args.command, date = date, version = __version__, summary_data = summary_data, cluster_data = cluster_data)

    mytemplate.render_context(ctx)
    with open(args.report,"w") as fw:
        fw.write(buf.getvalue())

# command = "polecat --CLIMB --outdir test --rank-by ^location-entropy"

# date = "2020-11-06"

# summary_data = [
#     {"cluster_no":19436,
#      "Most recent tip": "2020-10-03", 

#      "Tip Count":12,
#      "Admin0 Count":1,
#      "Admin1 Count":1},
#      {"cluster_no":17516,
#      "Most recent tip": "2020-10-09", 
#      "Tip Count":15,
#      "Admin0 Count":1,
#      "Admin1 Count":3},
#      {"cluster_no":16678,
#      "Most recent tip": "2020-10-09", 
#      "Tip Count":15,
#      "Admin0 Count":1,
#      "Admin1 Count":3},
#      {"cluster_no":18889,
#      "Most recent tip": "2020-10-09", 
#      "Tip Count":15,
#      "Admin0 Count":1,
#      "Admin1 Count":3}
# ]
# cluster_data = [
#     {"cluster_no":19436,
#     #     "lineage":
#     # "uk_lineage":
#      "stats": [{"statistic": 'node_number', "information": 19436},{"statistic": 'day_range', "information": 26},{"statistic": 'tip_count', "information": 12}], 
#      "table_no":2,
#      "treeString":"(('England/QEUH-9F3DC4/2020':4.999999999970306E-9,(('England/QEUH-9F8961/2020':3.3896999999999964E-5,'England/NORT-2A7C7E/2020':5.999999999986051E-9,'England/NORT-2A7C8D/2020':4.999999999970306E-9):3.3896999999999964E-5,'England/NORT-2A4A1D/2020':0.0,'England/QEUH-9C94E0/2020':0.0,'England/NORT-2A48F5/2020':4.999999999970306E-9,'England/QEUH-A0BF4A/2020':3.3896999999999964E-5,'England/QEUH-9B5256/2020':3.389799999999998E-5):1.645800000000001E-5):1.7434999999999998E-5,'England/QEUH-9D2A97/2020':4.999999999970306E-9,'England/QEUH-9D2657/2020':0.0,'England/QEUH-9D261B/2020':0.0);"},
#      {"cluster_no":17516,
#      "stats": [{"statistic": 'node_number', "information": 17516},{"statistic": 'day_range', "information": 26},{"statistic": 'tip_count', "information": 12}], 
#      "table_no":3,
#      "treeString":"((('Northern_Ireland/QEUH-96E4DE/2020':4.999999999970306E-9,'Northern_Ireland/QEUH-96EA81/2020':4.999999999970306E-9,'Northern_Ireland/QEUH-96DBE9/2020':0.0,'Northern_Ireland/QEUH-96DBDA/2020':0.0,'Northern_Ireland/QEUH-96D8B5/2020':4.999999999970306E-9,'Northern_Ireland/QEUH-96D008/2020':4.999999999970306E-9):3.389799999999998E-5,'Northern_Ireland/QEUH-96DABF/2020':3.404600000000003E-5,'Ireland/KK-NVRL-72IRL24802/2020':4.999999999970306E-9,'Northern_Ireland/QEUH-96DA55/2020':4.999999999970306E-9,'Northern_Ireland/QEUH-96DC31/2020':0.0,'Northern_Ireland/QEUH-96CBF9/2020':0.0,'Northern_Ireland/QEUH-96CFB1/2020':0.0,'Northern_Ireland/QEUH-96D897/2020':0.0):2.3736599999999992E-4,'Bangladesh/BCSIR-NILMRC-359/2020':1.0171099999999988E-4,'Bangladesh/BCSIR-NILMRC-320/2020':1.6956099999999993E-4);"}
#      ]

if __name__ == "__main__":
    make_report()

