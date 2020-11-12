![](./doc_figures/website_header.png)

# Input background data

<strong>polecat</strong> relies on the user providing a background tree, alignment and metadata file. 

The data files <strong>polecat</strong>  looks for are:
```
cog_global_2020-XX-YY_alignment.fasta
cog_global_2020-XX-YY_metadata.csv
cog_global_2020-XX-YY_tree.nexus
```

### --CLIMB

For SARS-CoV-2, this data is hosted on CLIMB as part of COG-UK. To run <strong>polecat</strong>  on CLIMB with the latest data, either
1) Use the ``--CLIMB`` flag 
or
2) Specify ``CLIMB: True`` in the config.yaml file 

This provides <strong>polecat</strong>  with the path to the latest data on CLIMB and allows the user to access adm2 information. 

### -r / --remote

Alternatively, run <strong>polecat</strong>  remotely from CLIMB with 
1) The ``-r / --remote`` flag 
or
2) By adding ``remote: True`` to the config file. 

If SSH keys are configured, simply run:

```
polecat -i input.csv -r 
```
Otherwise, provide a climb username with ``-uun / --username``:
```
polecat -i input.csv -r -uun climb-covid19-smithj
```

Notes:
- This data will access a version of the COG-UK data that is publically available (does not contain adm2 information)
- To access CLIMB in this way, you must have a valid COG-UK CLIMB username and be in the UK

By default, the data will be pulled down to a directory called ``polecat-cat`` in the current working directory. 

### -d / --datadir

The user can specify a custom background data directory with the ``-d / --datadir`` flag. 

This can be used with the `remote` option to rsync to an alternative location or without the without the remote flag, <strong>polecat</strong>  can just accept the data in that directory as input background data. 

This can also be run on CLIMB without the --CLIMB flag to specify an older version of the dataset. 

```
polecat -i input.csv -d path/to/data_directory 
```
### --background-metadata

By default, polecat will look for a csv containing background data in the data directory. However, to provide custom background data, use 
1) the ``--background-metadata`` flag
or
2) add `background_metadata: path/to/metadata.csv` to the config file


### Background metadata requirements


The following fields must be **always** present in this background metadata, or polecat will not run:

- **sequence_name** containing names of every sequence
- **country** containing the country of sampling
- A field to match the input data with containing COG IDs. The default header for this column is set to **central_sample_id**, but this can be changed by altering the ``--data-column`` argument
- A date column containing the date of sampling. The default header for this column is set to **sample_date**
- **adm2:** 


### [Next: Example report](./example_report.md)
