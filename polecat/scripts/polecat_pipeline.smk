import os
import csv

today = config["today"]

rule all:
    input:
        expand(os.path.join(config["clusterdir"],"{cluster}","{cluster}_subtree_1.newick"), cluster=config["clusters"]),
        os.path.join(config["tempdir"],"tree_prompt.txt")

rule split_metadata:
    input:
        filtered_metadata = config["filtered_metadata"]
    params:
        cluster = "{cluster}"
    output:
        metadata = os.path.join(config["clusterdir"],"{cluster}","{cluster}.metadata.csv")
    run:
        with open(output[0], "w") as fw:
            with open(input.filtered_metadata, "r") as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames

                writer = csv.DictWriter(fw, fieldnames=header,lineterminator='\n')
                writer.writeheader()

                for row in reader:
                    c_list = row["cluster"].split("|")
                    if params.cluster in c_list:
                        writer.writerow(row)

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

rule gather_civet:
    input:
        expand(os.path.join(config["clusterdir"],"{cluster}","{cluster}_subtree_1.newick"), cluster=config["clusters"])
    output:
        os.path.join(config["tempdir"],"tree_prompt.txt")
    shell:
        """
        touch {output[0]}
        """