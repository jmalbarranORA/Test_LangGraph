#!/usr/bin/env bash
# Author: Jose M. Albarran (Oracle)

# Load environment variables
source .env

# Install python 3.12
echo "Checking python 3.12 installation and install if needed"
pyenv versions --bare | grep '^3\.12' || pyenv install 3.12

# Set python 3.12 as default (use last available version)
PYTHON_VERSION=$(pyenv versions --bare | grep '^3\.12' | sort -V | tail -n 1)
rm .python-version
pyenv local $PYTHON_VERSION
echo "Using Python version: $PYTHON_VERSION"


# Create venv environment. We copy the files for avoiding problems with Onedrive (it does not allow to create symlinks)
# python -m venv .venv --copies
echo "Creating environment"
rm -rf .venv.nosync
python -m venv .venv.nosync


# Activate venv environment
source .venv.nosync/bin/activate

# Install requirements
echo "Installing requirements in environment"
pip install --upgrade pip
pip install -r requirements.txt



