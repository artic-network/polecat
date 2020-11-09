from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import glob
import os
import pkg_resources


from polecat import __version__, _program


setup(name='polecat',
      version=__version__,
      packages=find_packages(),
      scripts=["polecat/scripts/Snakefile",
      "polecat/scripts/polecat_pipeline.smk",
      "polecat/scripts/render_report.py",
      "polecat/scripts/polecatfunks.py"],
      package_data={"polecat":["data/*"]},
      install_requires=[
            "biopython>=1.70",
            "mako>=1.1.3"
        ],
      description='',
      url='https://github.com/COG-UK/polecat',
      author='Aine OToole, JT McCrone, Verity Hill, Andrew Rambaut',
      author_email='aine.otoole@ed.ac.uk',
      entry_points="""
      [console_scripts]
      {program} = polecat.command:main
      """.format(program = _program),
      include_package_data=True,
      keywords=[],
      zip_safe=False)
