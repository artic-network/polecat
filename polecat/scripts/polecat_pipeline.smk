import os
import csv

today = config["today"]

rule all:
    input:
        expand(os.path.join(config["clusterdir"],"{cluster}","report","civet_{cluster}_"+f"{today}.md"), cluster= config["clusters"]),
        os.path.join(config["outdir"],"polecat","report","figures","fig_prompt.txt")

rule split_metadata:
    input:
        filtered_metadata = config["filtered_metadata"]
    params:
        cluster = "{cluster}"
    output:
        metadata = os.path.join(config["clusterdir"],"{cluster}.metadata.csv")
    run:
        with open(output[0], "w") as fw:
            with open(input.filtered_metadata, "r") as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames

                writer = csv.DictWriter(fw, fieldnames=header,lineterminator='\n')
                writer.writeheader()

                for row in reader:
                    if row["cluster"] == params.cluster:
                        writer.writerow(row)

# rule run_civet:
#     input:
#         query = rules.split_metadata.output.metadata
#     params:
#         outdir = os.path.join(config["clusterdir"],"{cluster}"),
#         cluster = "civet_{cluster}"
#     output:
#         os.path.join(config["clusterdir"],"{cluster}","report","civet_{cluster}_"+f"{today}.md")
#     shell:
#         # "touch {output}"
#         """
#         civet -i {input.query:q} \
#             -o {params.cluster} \
#             --up-distance 2  \
#             --down-distance 100 \
#             --outdir {params.outdir} \
#             --input-column sequence_name \
#             --data-column sequence_name \
#             -d {config[datadir]}
#         """

rule cluster_catchment:
    input:
        tree = config["background_tree"],
        query = rules.split_metadata.output.metadata
    params:
        outdir = os.path.join(config["clusterdir"],"{cluster}"),
        cluster = "{cluster}"
    output:
        tree = os.path.join(config["clusterdir"],"{cluster}","{cluster}_subtree_1.newick")
    shell:
        """
        jclusterfunk context \
        -i "{input.tree}" \
        -o "{params.outdir}" \
        --mrca \
        -f newick \
        -p {params.cluster}_ \
        -m "{input.query}" \
        --id-column sequence_name
        """

# rule make_tree_figure:
#     input:
#         tree= os.path.join(config["tempdir"], "cluster_civet","{cluster}_subtree_1.newick"),
#         config = os.path.join(config["config"])
#     output:
#         figure = os.path.join(config["outdir"], "report","figures","{cluster}_tree.svg")
#     shell:
#         """
#         make_trees.py --tree {input.tree} --config {input.config} --output {output.figure}
#         """

rule gather_civet:
    input:
        expand(os.path.join(config["clusterdir"],"{cluster}","{cluster}_subtree_1.newick"), cluster=config["clusters"])
        # expand(os.path.join(config["clusterdir"],"{cluster}","report","civet_{cluster}_"+f"{today}.md"), cluster=config["clusters"])
    params:
        outdir = os.path.join(config["clusterdir"],"{cluster}"),
        cluster = "{cluster}"
    output:
        os.path.join(config["outdir"],"polecat","report","figures","fig_prompt.txt")
    run:
        """
        touch {output}
        """