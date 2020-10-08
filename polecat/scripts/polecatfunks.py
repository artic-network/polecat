#!/usr/bin/env python3

import os
import argparse
import csv 
import sys
from Bio import SeqIO
from datetime import datetime 
import tempfile
import pkg_resources
import yaml

from reportfunk.funks import io_functions as qcfunk

def get_defaults():
    default_dict = {"report_fields":0.5,
                    "threads":1,
                    "force":True
                    }
    return default_dict

def check_metadata_for_report_fields(config):
    report_fields,metadata = config["report_fields"], config["metadata"]
    with open(metadata, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        for field in report_fields:
            if field not in header:
                sys.stderr.write(qcfunk.cyan(f'Error: {field} not found in metadata file\n'))
                sys.exit(-1)