FONTS_DIR = $(HOME)/.fonts

all: chinese-potrace-path.svg

xqlarge-potrace.mf: /usr/share/texmf-dist/fonts/source/public/xq/xqlarge.mf
	ln -f -s $< $@

xqlarge-potrace.ttf: xqlarge-potrace.mf
	mftrace --verbose --potrace -f TTF -DFontName=$< -DFamilyName=$< -DFullName=$< $<

$(FONTS_DIR)/xqlarge-potrace.ttf: xqlarge-potrace.ttf
	ln -f -s "$(PWD)/$<" "$@"

chinese-potrace-path.pdf: chinese-potrace-text.svg xqlarge-potrace.ttf | $(FONTS_DIR)/xqlarge-potrace.ttf
	inkscape --export-text-to-path --export-pdf=$@ $<

chinese-potrace-path.svg: chinese-potrace-path.pdf
	inkscape --export-plain-svg=$@ $<

clean:
	rm -f xqlarge-potrace.mf xqlarge-potrace.ttf chinese-potrace-path.pdf chinese-potrace-path.svg

.PHONY: all clean
