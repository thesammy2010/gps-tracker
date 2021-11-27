#!/bin/bash

PYTHON_VERSION="3.10.0"

# install brew
which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    brew update
fi

# install pyenv
which -s pyenv
if [[ $? != 0 ]] ; then
    # Install pyenv
    brew install pyenv
fi


# install python 3.10.0 if doesn't already exist
pyenv install $PYTHON_VERSION

# create virtual environment
if [[ -z "$${VIRTUAL_ENV}" ]]; then
  $HOME/.pyenv/versions/$PYTHON_VERSION/bin/python -m venv venv
  echo "run 'source venv/bin/activate' and rerun"
  exit 1
fi

# check virtual env is using python
version="$(python --version)"
if [[ ! $version =~ "Python $PYTHON_VERSION" ]] ; then
  echo "python virtual environment version invalid"
  exit 1
fi


# install project in editable mode
pip install -e .

# install dev dependencies
pip install \
  black==21.11b1 \
  mypy==0.910

