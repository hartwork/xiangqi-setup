# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

PYTHON = python
DESTDIR = /


all:

dist:
	$(RM) MANIFEST
	$(PYTHON) setup.py sdist

install:
	$(PYTHON) setup.py install --root "$(DESTDIR)"


.PHONY: all dist install
