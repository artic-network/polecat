import os

"""
Output csv from jclusterfunk
most_recent_tip,tip_count,admin0_count,admin1_count,admin2_count,tips
2020-01-23,2,1,0,0,Hong_Kong/HKPU2_1801/2020|Hong_Kong/VB20017970-2/2020
2020-01-25,2,1,0,0,Wuhan/0125-A137/2020|Wuhan/0125-A169/2020
2020-01-25,2,1,0,0,Wuhan/0125-A160/2020|Wuhan/0125-A148/2020
"""
rule prune_out_catchments:
    input:
        tree = config["tree"]
    output:
        csv = os.path.join(config["outdir"],"jclusterfunk","highest_parent.csv")
    shell:
        """
        jclusterfunk polecat \
        -i "{input.tree:q}" \
        -o "{output.csv}" \
        --max-parent {config[up_distance]} \
        --max-child {config[down_distance]} \
        -f newick \
        """

rule make_webpage:
    input:
        rules.prune_out_catchments.output.csv
    output:
        os.path.join(config["outdir"],"cluster.html")
    shell:
        """
        touch {output:q}
        """