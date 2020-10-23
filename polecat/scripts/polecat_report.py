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

from dateutil.relativedelta import relativedelta, FR
import datetime as dt

from reportfunk.funks import time_functions as time_func
from reportfunk.funks import io_functions as qcfunk

from reportfunk.funks import prep_data_functions as prep_data
from reportfunk.funks import tree_functions as tree_viz
from reportfunk.funks import parsing_functions as dp
from reportfunk.funks import table_functions as table_func
import polecatfunks as pfunk

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
        report_file.write(f"| {cluster_header} |\n")
        for field in cluster_fields:
            row = cluster_info[cluster]
            data = row[field]
            
            report_file.write(f"| {field} | {data} |\n")



    report_file.close()

#     """
#     to do: 
#     - write out a summary table of all the clusters from metadata
#     - tree figures
#     - summary of tips in each tree
#     - snipit? 
#     """


if __name__ == "__main__":
    make_report()


# database_column = "sequence_name"
# full_tax_dict, query_dict, tree_to_tip, tree_to_all_tip, inserted_node_dict, adm2_present_in_metadata, full_query_count = dp.parse_all_metadata(treedir, collapse_summary, filtered_background_metadata, background_metadata, query, input_column, database_column, database_sample_date_column, display_name, sample_date_column, label_fields, tree_fields, table_fields, node_summary, date_fields=date_fields, UK_adm2_adm1_dict=adm2_to_adm1)


# ```python, name="early descriptions", echo=False, results='tex'
# number_seqs = len(query_dict)
# not_found_in_climb = full_query_count - number_seqs

# cog_number = 0
# not_in_cog_number = 0
# for tax in query_dict.values():
#     if tax.in_db:
#         cog_number += 1
#     else:
#         not_in_cog_number += 1


# prep_data.analyse_inputs(inputs)

# print("\n")

# print(str(full_query_count) + " queries (" + str(cog_number) + " matched to COG-UK database)")
# print(str(not_in_cog_number) + " sequences input")
# if not_found_in_climb:
#     print(str(not_found_in_climb) + " not found in background data")

# if dates_present:
#     print("Time fields provided: " + ",".join(date_fields))
#     print("Earliest date: " + min_string)
#     print("Latest date: " + max_string)
# else:
#     print("No time information provided")
# ```


# ```python, name="first_table", echo=False, results="tex"
# output = table_func.make_custom_table(query_dict, table_fields, include_snp_table)
# if cog_number != 0 and not_in_cog_number != 0:
#     df_cog, df_seqs = output
#     print("**Table 1** | Queries found in COG-UK database.\n")
#     print(df_cog.to_markdown())
#     print("\n")
#     print("**Table 2** | Queries matched to closest COG-UK sequence using input sequences\n")
#     print(df_seqs.to_markdown())
# elif cog_number == 0 and not_in_cog_number != 0:
#     df_seqs = output
#     print("**Table 1** | Queries matched to closest COG-UK sequence using input sequences\n")
#     print(df_seqs.to_markdown())
# elif not_in_cog_number == 0 and cog_number != 0:
#     df_cog = output
#     print("**Table 1** | Queries found in COG-UK database.\n")
#     print(df_cog.to_markdown())
# ```

# ```python, name="make_legend", echo=False, include=False, results='tex'
# for trait, colour_dict in colour_dict_dict.items():
#     tree_viz.make_legend(colour_dict_dict)
#     number_of_options = len(colour_dict)
#     if number_of_options > 15:
#         print("WARNING: There are more than 15 options to colour by for " + trait + ", which will make it difficult to see the differences between colours. Consider adding the trait to the taxon labels on the tree by using the flag _--label-fields_ when calling CIVET.")
# ```
# ```python, name="time_plot", echo=False, results='raw', include=False
# if dates_present:
#     count = 0
#     tree_to_time_series = {}
#     for tree in tree_order:
#         count += 1
#         lookup = f"{tree_name_stem}_{tree}"
#         tips = tree_to_tip[lookup]
#         if len(tips) > 1:
#             time_func.plot_time_series(tips, query_dict, max_overall_date, min_overall_date, date_fields, label_fields, lookup, svg_figdir, safety_level = safety_level)
#             tree_to_time_series[lookup] = count
# ```

# ```python, name="show_trees", echo=False, results='raw'
# for i in range(1,overall_tree_number+1):
#     tree_name = "Tree " + str(i)
#     lookup = f"{tree_name_stem}_{i}"
#     print(f"> **Tree {i}** | ")
#     if len(tree_to_tip[lookup]) == 1:
#         print(f"1 sequence of interest")
#     else:
#         print(f"{len(tree_to_tip[lookup])} sequences of interest")
#     print("   ")
    
#     if lookup not in too_tall_trees:
#         print(f"![]({figdir}/{name_stem}_make_trees_{i}.png)")

#         print(f'<img src="{figdir}/{name_stem}_make_legend_1.png" alt="drawing" style="width:100%;"/>')
#         print("\n")

#         if dates_present and lookup in tree_to_time_series.keys():
#             print("![](" + figdir + "/" + name_stem + "_time_plot_" + str(tree_to_time_series[lookup]) + ".png)")

#         if not no_snipit:
#             print(f"![]({figdir}/genome_graph_{lookup}.png)")

#     else:
#         print(tree_name + " was too large to be rendered. Please see summary table below. If visualisation is required, please use intermediate tree files and use software such as Figtree.")

# if too_tall_trees != []:
#     print("### Large tree summaries\n")
#     print("NB: data in subtrees within this tree is not included in the summary here.")
#     df_large_trees = pd.DataFrame(too_large_tree_dict)
#     df_large_trees.set_index("Tree name", inplace=True)
#     print(df_large_trees.to_markdown())

# ```

# ```python, name="tree_background", echo=False, include=False,  results='raw'
# if include_bars:
#     print("""### Tree background\n\nThe following plots describe the data in the collapsed nodes in more detail.\nIf more than one """ + node_summary + """ was present, the bar chart describes the number of sequences present in each """ + node_summary + """. \nWhere there were 10 options or more, the largest 10 have been taken.""")
#     bar_count = tree_viz.describe_collapsed_nodes(full_tax_dict, tree_name_stem, treedir, node_summary)
#     if node_summary == "country":
#         print("If a UK sequence is present in the collapsed node, it is always shown in the plot.")
# ```
# ```python, name="show_background",echo=False,include=False,results='raw'
# if include_bars:
#     if bar_count == 0:
#         print(f"There were no nodes that needed to be shown, as there were no collapsed nodes with more than two of {node_summary} in.")
#     for i in range(bar_count):
#         print(f"![]({figdir}/{name_stem}_tree_background_{i+1}.png)")

# ```

# ```python, name="map_sequences", echo=False, results='raw', include=False
# if map_sequences:
#     stop_map = False
#     if map_info == "adm2":
#         output = mapping.map_adm2(query_dict, clean_locs, mapping_json_files, svg_figdir)
#         if output:
#             adm2_in_map, adm2_percentages = output
#         else:
#             stop_map = True
#     else:
#         output = mapping.map_sequences_using_coordinates(query, mapping_json_files, urban_centres, pc_file, colour_map_by, map_info, input_crs, svg_figdir)
#         if output:
#             adm2_in_map, adm2_percentages = output
#         else:
#             stop_map = True
        
#     if not stop_map:
#         print("## Plotting sequences")

#         print("There are sequences from " + str(len(adm2_in_map)) + " admin2 regions")

#         print("This is divided into:")
#         for adm2, percentage in adm2_percentages.items():
#             print(str(percentage) + "% (" + str(adm2_in_map[adm2]) + ") in " + adm2)

#         if colour_map_by:
#             print("This is shown in the map below, and is coloured by " + colour_map_by + " and urban centres are shown in the darker grey")
#         else:
#             if map_info != "adm2":
#                 print("This is shown in the map below, with urban centres shown in the darker grey")

#     else:
#         print("Insufficient geographical information to plot sequences")
# ```
# ```python, name="show_map", echo=False, results='raw'
# if map_sequences and not stop_map:
#     print("![](" + figdir + "/" + name_stem + "_map_sequences_1.png)")
# ```

# ```python, name='Regional-scale', echo=False, results='raw'
# if local_lineages:
#     print("## Regional-scale background UK lineage mapping")
#     try:
#         mapping.local_lineages_section(lineage_maps, lineage_tables)
#     except:
#         print("There was no adm2 data available to map with, as none was provided and none of the sequences were found in COG")
# ```

# ```python, name="print conclusions", echo=False, results='raw'
# ##CONCLUSIONS

# ```
# ```python, name='write_summary_file', echo=False, results='raw'
# cfunk.make_full_civet_table(query_dict, full_tax_dict, tree_fields, label_fields, input_column, outdir, table_fields)
# ```

# ##APPENDIX

# ### Software versions

# This report was made using:

# ```python, name='software versions', echo=False, results='raw'

# import platform


# print("Python " + platform.python_version())

# print("Matplotlib version " + matplotlib.__version__)
# print("Pandas version " + pd.__version__)
# print("Tabulate version " + tabulate.__version__)
# print("CSV version " + csv.__version__)
# print("Numpy version " + np.__version__)
# print("Scipy version " + sp.__version__)
# print("No version number for Baltic")

# if data_date != "":
#     print("COG data from " + data_date + " was used as background data.")
# else:
#     yesterday = dt.date.today() - dt.timedelta(1)
#     print("COG data from " + str(yesterday))


# print("CIVET version is 2.0")
# ```

# ## Acknowledgements

# This report was generated by CIVET, made primarily by Áine O'Toole and Verity Hill, using code from Rambaut Lab members.

# The background data from the UK was generated by the COG consortium (https://www.cogconsortium.uk/), a national, multi-centre consortium for the sequencing and analysis of SARS-CoV-2 genomes for Public Health.

# We also use some background data from GISAID (https://www.gisaid.org/) in the phylogenies. We thank everyone involved in the global sequencing effort for making their data available. 

# Tree data was visualised using baltic (https://github.com/evogytis/baltic)

# Mapping data was downloaded from the Global Administrative Database (https://gadm.org/) and Natural Earth (https://www.naturalearthdata.com/)

# ```python, name="footer", echo=False, results='raw'
# print("![](" + figdir + "/footer.png)")
# ```
