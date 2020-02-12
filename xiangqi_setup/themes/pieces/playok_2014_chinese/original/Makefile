# Copyright (C) 2014 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

PIECE_SVG_FILES = $(wildcard 0??.svg)
PIECE_PNG_FILES = $(patsubst %.svg,%.png,$(PIECE_SVG_FILES))

all: $(PIECE_PNG_FILES)

%.png: %.svg
	convert -background none -define png:color-type=6 -depth 4 $< png:- \
		| pngquant 64 > $@

$(wildcard 00?.png): a0.svg

$(wildcard 01?.png): b0.svg

clean:
	rm -f *.png

.PHONY: all clean
