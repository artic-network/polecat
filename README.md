# polecat

Phylogenetic Overview & Local Epidemiological Cluster Analysis Tool


<img src="./docs/doc_figures/polecat_logo.png" width=350>

<strong>polecat</strong> is a tool developed with 'real-time' genomics in mind. 

Using a background phylogeny, such as the large phylogeny available through the COG-UK infrastructure on CLIMB, <strong>polecat</strong> will identify and flag clusters based on various configurable statistics. 


A fully customisable report is generated, summarising information about the clusters of interest.


### polecat documentation

Full documentation can be found at https://cog-uk.github.io/polecat/


<strong>Quick Links:</strong>

  * [Polecat clusters](https://rambaut.github.io/polecat/clusters.html)
  * [Install and update polecat](./docs/installation.md)
  * [Usage](./docs/usage.md)
  * [Statistics options](./docs/statistics.md)
  * [Background data](./docs/background_data.md)
  * [Contributors & acknowledgements](./docs/acknowledgements.md)



<strong>polecat</strong> was created by the Rambaut Group, Edinburgh University




### Full usage

```
usage: polecat -i <config.yaml> [options]

polecat: Phylogenetic Overview & Local Epidemiological Cluster Analysis Tool

optional arguments:
  -h, --help            show this help message and exit

input output options:
  -c CONFIG, --config CONFIG
                        Input config file
  --outdir OUTDIR       Output directory. Default: current working directory
  -o OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX
                        Output prefix. Default: polecat

data source options:
  -d DATADIR, --datadir DATADIR
                        Local directory that contains the data files. Default: civet-cat
  -m BACKGROUND_METADATA, --background-metadata BACKGROUND_METADATA
                        Custom metadata file that corresponds to the large global tree/ alignment.
                        Should have a column `sequence_name`.
  --CLIMB               Indicates you're running CIVET from within CLIMB, uses default paths in CLIMB to
                        access data
  -r, --remote          Remotely access lineage trees from CLIMB
  -uun UUN, --your-user-name UUN
                        Your CLIMB COG-UK username. Required if running with --remote flag
  --data-column DATA_COLUMN
                        Option to search COG database for a different id type. Default: COG-UK ID

cluster options:
  --max-age MAX_AGE     Maximum age of a cluster. Default: none
  --max-count MAX_COUNT
                        Maximum number of clusters to report. Default: all
  --max-recency MAX_RECENCY
                        Maximum recency of a cluster. Default: none
  --max-size MAX_SIZE   Maximum number of tips in a subcluster. Default: none
  --min-size MIN_SIZE   Minimum cluster size. Default: 10
  --min-UK MIN_UK       Minimum proportion of UK tips. Default: none
  --optimize-by OPTIMIZE_BY
                        Citerion to use to find optimal cluster. Default: none
  --rank-by RANK_BY     Statistic to rank clusters by. Default: rate

report options:
  --summary-fields SUMMARY_FIELDS
                        Comma-separated string of which statistics to include in the report. Default:
                        node_name,most_recent_tip,tip_count,admin0_count,admin1_count
  --cluster-fields CLUSTER_FIELDS
                        Comma-separated string of which columns to include in the cluster tables.
                        Default: sequence_name,lineage,country
  --display-name DISPLAY_NAME
                        Column in input csv file with display names for seqs. Default: same as input
                        column
  --colour-by COLOUR_BY
                        Comma separated string of fields to display as coloured dots rather than text in
                        report trees. Optionally add colour scheme eg adm1=viridis
  --tree-fields TREE_FIELDS
                        Comma separated string of fields to display in the trees in the report. Default:
                        country
  --label-fields LABEL_FIELDS
                        Comma separated string of fields to add to tree report labels.
  --date-fields DATE_FIELDS
                        Comma separated string of metadata headers containing date information.
  --node-summary NODE_SUMMARY
                        Column to summarise collapsed nodes by. Default = Global lineage
  --table-fields TABLE_FIELDS
                        Fields to include in the table produced in the report. Query ID, name of
                        sequence in tree and the local tree it's found in will always be shown

misc options:
  -b, --launch-browser  Optionally launch md viewer in the browser using grip
  --tempdir TEMPDIR     Specify where you want the temporary stuff to go Default: $TMPDIR
  --no-temp             Output all intermediate files
  --verbose             Print lots of stuff to screen
  --threads THREADS     Number of threads
  -v, --version         show program's version number and exit
```
<img src="./docs/doc_figures/website_header.png">