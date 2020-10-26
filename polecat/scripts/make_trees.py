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

import reportfunk.funks.baltic as bt
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import cm

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
    parser.add_argument("--tree", required=True, help="input tree file", dest="tree") 
    parser.add_argument("--config",help="config yaml file",dest="config")
    parser.add_argument("--outfile", help="output report file", dest="outfile")
    return parser.parse_args()


    
def make_cluster_tree(My_Tree, tree_name, num_tips, taxon_dict, outfile,config):
    
    My_Tree.uncollapseSubtree()

    if num_tips < 10:
        page_height = num_tips
    else:
        page_height = num_tips/2  

    tallest_height = config["tallest_height"]
    offset = tallest_height - My_Tree.treeHeight
    space_offset = tallest_height/10
    absolute_x_axis_size = tallest_height+space_offset+space_offset + tallest_height #changed from /3 

    tipsize = 40
    c_func=lambda k: 'dimgrey' ## colour of branches
    l_func=lambda k: 'lightgrey' ## colour of dotted lines
    s_func = lambda k: tipsize*5 if k.name in taxon_dict else tipsize
    z_func=lambda k: 100
    b_func=lambda k: 2.0 #branch width
    so_func=lambda k: tipsize*5 if k.name in taxon_dict else 0
    zo_func=lambda k: 99
    zb_func=lambda k: 98
    zt_func=lambda k: 97
    font_size_func = lambda k: 25 if k.name in taxon_dict else 15
    kwargs={'ha':'left','va':'center','size':12}

    cn_func = lambda k: "#8eafa6" if k.name in taxon_dict else 'dimgrey'
    co_func=lambda k: "#8eafa6" if k.name in taxon_dict else 'dimgrey' 
    outline_colour_func = lambda k: 'dimgrey' 

    x_attr=lambda k: k.height + offset
    y_attr=lambda k: k.y

    y_values = []
    for k in My_Tree.Objects:
        y_values.append(y_attr(k))

    min_y_prep = min(y_values)
    max_y_prep = max(y_values)

    vertical_spacer = 0.5 

    full_page = page_height + vertical_spacer + vertical_spacer
    min_y,max_y = min_y_prep-vertical_spacer,max_y_prep+vertical_spacer

    x_values = []
    for k in My_Tree.Objects:
        x_values.append(x_attr(k))
    max_x = max(x_values)
    
    fig,ax = plt.subplots(figsize=(20,page_height),facecolor='w',frameon=False, dpi=200)
    
    My_Tree.plotTree(ax, colour_function=c_func, x_attr=x_attr, y_attr=y_attr, branchWidth=b_func)
    
    My_Tree.plotPoints(ax, x_attr=x_attr, colour_function=cn_func,y_attr=y_attr, size_function=s_func, outline_colour=outline_colour_func)
    My_Tree.plotPoints(ax, x_attr=x_attr, colour_function=co_func, y_attr=y_attr, size_function=so_func, outline_colour=outline_colour_func)


    for k in My_Tree.Objects:
        if k.numName in taxon_dict:
            name=k.numName

    ax.plot([0,0.00003], [-0.5,-0.5], ls='-', lw=2, color="dimgrey")
    ax.text(0.000015,-1.15,"1 SNP",size=20, ha="center", va="center")

    ax.spines['top'].set_visible(False) ## make axes invisible
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_xlim(-space_offset,absolute_x_axis_size)
    ax.set_ylim(min_y-1,max_y)


    fig.tight_layout()
    
    plt.savefig(outfile, format="svg")


            x=x_attr(k)
            y=y_attr(k)
        
            if k.node_number > 1:
                new_dot_size = tipsize*(1+math.log(k.node_number)) 
                ax.scatter(x, y, s=new_dot_size, marker="s", zorder=3, color="dimgrey")

            height = My_Tree.treeHeight+offset
            text_start = tallest_height+space_offset+space_offset

            if len(desired_fields) > 1:
                
                division = (text_start - tallest_height)/(len(desired_fields))
                tip_point = tallest_height+space_offset

                if k.name in query_dict.keys():
                    
                    count = 0
                    
                    for trait in desired_fields:
                        
                        if trait != first_trait:

                            x_value = tip_point + count
                            count += division

                            option = query_dict[k.name].attribute_dict[trait]
                            
                            if trait in graphic_dict.keys():
                                colour_dict = colour_dict_dict[trait]
                                trait_blob = ax.scatter(x_value, y, tipsize*5, color=colour_dict[option])  
                            else:
                                trait_text = ax.text(x_value, y, option, size=15, ha="left", va="center", fontweight="light")
                            
                            blob_dict[trait] = x_value

                    ax.text(text_start+division, y, name, size=font_size_func(k), ha="left", va="center", fontweight="light")
                    
                    if x != max_x:
                        ax.plot([x+space_offset,tallest_height],[y,y],ls='--',lw=1,color=l_func(k))

                else:

                    ax.text(text_start+division, y, name, size=font_size_func(k), ha="left", va="center", fontweight="light")
                    if x != max_x:
                        ax.plot([x+space_offset,tallest_height],[y,y],ls='--',lw=1,color=l_func(k))

                #This section adds a line in between each trait in the tree
                # for blob_x in blob_dict.values():
                #     line_x = blob_x - (division/2)
                #     ax.plot([line_x,line_x],[min_y,max_y],ls='--',lw=3,color=l_func(k))
            
            
            else:
                ax.text(text_start, y, name, size=font_size_func(k), ha="left", va="center", fontweight="ultralight")
                ax.plot([x+space_offset,tallest_height+space_offset],[y,y],ls='--',lw=1,color=l_func(k))

    #Adds labels to the top of the tree to indicate what each labelled trait is
    if len(desired_fields) > 1:

        blob_dict[first_trait] = tallest_height
        
        for trait, blob_x in blob_dict.items():
            y = max_y
            x = blob_x

            ax.text(x,y,trait, rotation=90, size=15,ha="center", va="bottom")
    
    ax.plot([0,0.00003], [-0.5,-0.5], ls='-', lw=2, color="dimgrey")
    ax.text(0.000015,-1.15,"1 SNP",size=20, ha="center", va="center")

    ax.spines['top'].set_visible(False) ## make axes invisible
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_xlim(-space_offset,absolute_x_axis_size)
    ax.set_ylim(min_y-1,max_y)


    fig.tight_layout()

    plt.savefig(figdir + "/" + tree_name + ".svg", format="svg")


def make_tree():
    


if __name__ == "__main__":
    make_tree()