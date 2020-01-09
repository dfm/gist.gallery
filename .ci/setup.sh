#!/bin/bash
set -e

# Display machine info
lscpu

# Set up conda
sudo chown -R $USER $CONDA
. $CONDA/etc/profile.d/conda.sh
conda env create --quiet --prefix ./env -f environment.yml

# Activate conda & install base dependencies
. $CONDA/etc/profile.d/conda.sh
conda activate ./env
