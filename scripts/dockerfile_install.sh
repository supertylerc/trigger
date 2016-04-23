#!/bin/bash

# Originally from https://github.com/higebu/docker-tox
# Modified by: Tyler Christiansen <supertylerc@saucelabs.com>

PYTHON_VERSIONS=(2.7.11)
PYTHON_GLOBAL_VERSION=2.7.11
PYTHON_PIP_VERSION=8.1.1

apk --update add curl ca-certificates git build-base \
  libffi-dev openssl-dev libbz2 libc6-compat ncurses-dev readline-dev \
  xz-dev zlib-dev sqlite-dev patch bzip2-dev expat-dev zlib-dev \
  gdbm-dev paxmark linux-headers tcl-dev

# Install pyenv
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer -o /pyenv-installer
touch /root/.bashrc
/bin/ln -s /root/.bashrc /root/.bash_profile
/bin/bash /pyenv-installer
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install all python versions
for v in "${PYTHON_VERSIONS[@]}"; do
  pyenv install $v &
done
wait

# Set global python version
pyenv global $PYTHON_GLOBAL_VERSION "${PYTHON_VERSIONS[@]}"

# Install tox
pip install -U setuptools
pip install -U pip
pip install -U tox

# Cleanup
rm /pyenv-installer
rm -rf /var/cache/apk/*
rm -rf /tmp/python*
rm -rf /tmp/pip*
