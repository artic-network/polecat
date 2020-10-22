import os
import csv

rule all:
    input:
        expand(os.path.join(config["clusterdir"],"{cluster}","report","{cluster}.md"), cluster= config["clusters"]),
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

rule civet_instance:
    input:
        query = rules.split_metadata.output.metadata
    params:
        outdir = os.path.join(config["clusterdir"],"{cluster}"),
        cluster = "{cluster}"
    output:
        report = os.path.join(config["clusterdir"],"{cluster}","report","{cluster}.md")
    shell:
        """
        civet -i {input.query:q} \
        -o {params.cluster} \
        --outdir {params.outdir} \
        --input-column sequence_name \
        --data-column sequence_name \
        -d {config[datadir]}
        """

rule gather_civet:
    input:
        expand(os.path.join(config["clusterdir"],"{cluster}","report","{cluster}.md"), cluster=config["clusters"])
    params:
        outdir = os.path.join(config["clusterdir"],"{cluster}"),
        cluster = "{cluster}"
    output:
        os.path.join(config["outdir"],"polecat","report","figures","fig_prompt.txt")
    shell:
        """
        touch {output}
        """