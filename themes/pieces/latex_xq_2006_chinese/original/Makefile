FONTS_DIR = $(HOME)/.fonts

all: chinese-path.svg

xqlarge.mf: /usr/share/texmf-dist/fonts/source/public/xq/xqlarge.mf
	ln -s $< $@

xqlarge.ttf: xqlarge.mf
	mftrace -f TTF $<

$(FONTS_DIR)/xqlarge.ttf: xqlarge.ttf
	ln -s "$(PWD)/$<" "$@"

chinese-path.pdf: chinese-text.svg xqlarge.ttf | $(FONTS_DIR)/xqlarge.ttf
	inkscape --export-text-to-path --export-pdf=$@ $<

chinese-path.svg: chinese-path.pdf
	inkscape --export-plain-svg=$@ $<

clean:
	rm -f xqlarge.mf xqlarge.ttf chinese-path.pdf chinese-path.svg

.PHONY: all clean
