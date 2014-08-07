FONTS_DIR = $(HOME)/.fonts

all: chinese-autotrace-path.svg chinese-potrace-path.svg

xqlarge-autotrace.mf xqlarge-potrace.mf: /usr/share/texmf-dist/fonts/source/public/xq/xqlarge.mf
	ln -f -s $< $@

xqlarge-autotrace.ttf: xqlarge-autotrace.mf
	mftrace --verbose --autotrace -f TTF -DFontName=$< -DFamilyName=$< -DFullName=$< $<

xqlarge-potrace.ttf: xqlarge-potrace.mf
	mftrace --verbose --potrace -f TTF -DFontName=$< -DFamilyName=$< -DFullName=$< $<

$(FONTS_DIR)/xqlarge-autotrace.ttf: xqlarge-autotrace.ttf
	ln -f -s "$(PWD)/$<" "$@"

$(FONTS_DIR)/xqlarge-potrace.ttf: xqlarge-potrace.ttf
	ln -f -s "$(PWD)/$<" "$@"

chinese-autotrace-path.pdf: chinese-autotrace-text.svg xqlarge-autotrace.ttf | $(FONTS_DIR)/xqlarge-autotrace.ttf
	inkscape --export-text-to-path --export-pdf=$@ $<

chinese-potrace-path.pdf: chinese-potrace-text.svg xqlarge-potrace.ttf | $(FONTS_DIR)/xqlarge-potrace.ttf
	inkscape --export-text-to-path --export-pdf=$@ $<

%.svg: %.pdf
	inkscape --export-plain-svg=$@ $<

clean:
	rm -f *.mf *.ttf *.pdf *-path.svg

.PHONY: all clean
