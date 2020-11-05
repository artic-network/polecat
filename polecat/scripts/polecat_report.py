#!/usr/bin/env python3
import os
import argparse
import shutil
import sys
import yaml
import csv

import matplotlib.pyplot as pyplot

import os
import matplotlib.font_manager as font_manager
import matplotlib as mpl

import csv
import numpy as np
import scipy as sp

import datetime as dt

from reportfunk.funks import io_functions as qcfunk


thisdir = os.path.abspath(os.path.dirname(__file__))


def parse_args():
    parser = argparse.ArgumentParser(description="Report generator script")
    parser.add_argument("--config", required=True, help="config yaml file", dest="config") 
    parser.add_argument("--report", help="output report file", dest="report")
    return parser.parse_args()

def make_report():

    args = parse_args()
    config = {}
    qcfunk.parse_yaml_file(args.config,config)

    summary_fields = config["summary_fields"].split(",")
    cluster_fields = config["cluster_fields"].split(",")

    report_file = open(args.report, "w")

    today = config["today"]

    report_file.write(f"## Cluster report {today}\n\n")

    ## Make summary table at top
    summary_header = " | ".join(summary_fields)
    table_string = ""
    for field in summary_fields:
        table_string+=":-----|"

    report_file.write(f"| {summary_header} |\n|{table_string}\n")

    
    cluster_info = {}
    with open(config["all_clusters"],"r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            summary_table_data = []
            cluster_info[row["node_number"]] = row
            for field in summary_fields:
                summary_table_data.append(row[field])
            table_items = " | ".join(summary_table_data)
            report_file.write(f"| {table_items} |\n")

    ## Make cluster table at top
    cluster_header = "| Statistic | Info |\n|:----|:----|\n"

    c  = 0
    for cluster in cluster_info:
        c +=1 
        report_file.write(f"### {c}) Cluster {cluster}\n\n")
        report_file.write(f"{cluster_header}")
        for field in cluster_fields:
            row = cluster_info[cluster]
            data = row[field]
            
            report_file.write(f"| {field} | {data} |\n")
        
        report_file.write(f"\n[](./figures/{cluster}.tree.svg)\n\n")



    report_file.close()


if __name__ == "__main__":
    make_report()


