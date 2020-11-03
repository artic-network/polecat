
![](./doc_figures/website_header.png)

# Installation

Instructions for installing polecat locally

### Requirements

<strong>polecat</strong> runs on MacOS and Linux. The conda environment recipe may not build on Windows (and is not supported) but <strong>polecat</strong> can be run using the Windows subsystem for Linux.

1. Some version of conda, we use Miniconda3. Can be downloaded from [here](https://docs.conda.io/en/latest/miniconda.html)
2. Access to CLIMB or to a local data directory. More information about this data [here](./background_data.md)

### Install polecat

1. ``git clone https://github.com/COG-UK/polecat.git`` and ``cd polecat``
2. ``conda env create -f environment.yml``
3. ``conda activate polecat``
4. ``python setup.py install``

> Note: we recommend using polecat in the conda environment specified in the ``environment.yml`` file as per the instructions above. If you can't use conda for some reason, dependency details can be found in the ``environment.yml`` file. 


### Check the install worked

Type (in the polecat environment):

```
polecat
```
and you should see the help menu of polecat printed



### Updating polecat

> Note: Even if you have previously installed ``polecat``, as it is being worked on intensively, we recommend you check for updates before running.

To update:

1. ``conda activate polecat``
2. ``git pull`` \
pulls the latest changes from github
3. ``python setup.py install`` \
re-installs polecat
4. ``conda env update -f environment.yml`` \
updates the conda environment 

### Troubleshooting update
- If you have previously installed polecat using ``pip``, you will need to update polecat in the same way (``pip install .``)
- Try ``pip uninstall polecat`` and then re-install with `python setup.py install`


### [Next: Input options](./usage.md)