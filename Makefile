MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)
version := $(shell python setup.py --version)
platform := $(shell python -c "import sysconfig as sc; print('py{}-{}'.format(sc.get_python_version().replace('.', ''), sc.get_platform()))")
sha := $(shell git rev-parse HEAD)
sitePackages := $(shell python -c 'import site; print(site.getsitepackages()[0])')

%.txt: %.in
	pip-compile --verbose --output-file $@ $<

.PHONY: setup
setup: $(outputs)

check:
	@which pip-compile > /dev/null

clean: check
	- rm requirements.txt
	- rm -rf ./klsi.egg-info
	
.PHONY: install
install:
	pip install pip-tools
	pip-sync requirements.txt	
	
.PHONY: all
all: setup install	