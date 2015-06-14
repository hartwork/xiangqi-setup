# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

INKSCAPE = inkscape
OPTIPNG = optipng
XIANGQI_SETUP = ../xiangqi-setup

SHARED_XIANGQI_SETUP_OPTS = --width-px 400 demo.wxf

all: setup_imitate_latex_xq.png setup_imitate_chinese_books.png setup_imitate_playok.png

clean:
	$(RM) setup_imitate_*

demo_euro_xiangqi_js.svg:
	"$(XIANGQI_SETUP)" \
		 \
		--pieces euro_xiangqi_js \
		--width-cm 7 demo.wxf \
		$@

demo_retro_simple.svg:
	"$(XIANGQI_SETUP)" \
		--pieces retro_simple \
		--width-cm 7 demo.wxf \
		$@

setup_imitate_latex_xq.svg:
	"$(XIANGQI_SETUP)" \
		--board latex_xq_remake \
		--pieces latex_xqlarge_2006_chinese_autotrace \
		$(SHARED_XIANGQI_SETUP_OPTS) \
		$@

setup_imitate_chinese_books.svg:
	"$(XIANGQI_SETUP)" \
		--board minimal_chinese \
		--pieces retro_simple \
		$(SHARED_XIANGQI_SETUP_OPTS) \
		$@

setup_imitate_playok.svg:
	"$(XIANGQI_SETUP)" \
		--board playok_2014_remake \
		--pieces playok_2014_chinese \
		--scale-pieces 1.025 \
		$(SHARED_XIANGQI_SETUP_OPTS) \
		$@

%.png: %.svg
	$(INKSCAPE) --export-png $@ $<
	$(OPTIPNG) -o7 $@


.PHONY: all clean
