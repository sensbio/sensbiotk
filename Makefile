# Automating common tasks for SENSBIOTK development

PYTHON = python
NOSETESTS = nosetests
PYCHECKER = pychecker.sh

#
# Building
#

all: build

build:
	$(PYTHON) setup.py build

#
# Cleaning
#

clean-pyc:
	find . -regex ".*\.pyc" -exec rm -rf "{}" \;

clean: clean-pyc
	find . -regex ".*\.so" -exec rm -rf "{}" \;
	find . -regex ".*\.pyd" -exec rm -rf "{}" \;
	find . -regex ".*~" -exec rm -rf "{}" \;
	find . -regex ".*#" -exec rm -rf "{}" \;
	rm -rf build
	rm -f sensbiotk/tests/tmpdata/*.*
	$(MAKE) -C doc clean

#
# Tests
#

test: build
	cd sensbiotk/tests && $(NOSETESTS) 
#
# Code checker
#

check: 
	$(PYCHECKER) 'sensbiotk/algorithms/*.py'
	$(PYCHECKER) 'sensbiotk/algorithms/stride_length/*.py'
	$(PYCHECKER) 'sensbiotk/calib/*.py'
	$(PYCHECKER) 'sensbiotk/driver/*.py'
	$(PYCHECKER) 'sensbiotk/io/*.py'
	$(PYCHECKER) 'sensbiotk/tests/*.py'
	$(PYCHECKER) 'examples/*/*.py'

#
# Documentation
#

doc: build
	cd doc && make html

#
# Installation
#

install:
	$(PYTHON) setup.py install
