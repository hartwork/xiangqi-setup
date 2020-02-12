# xiangqi-setup (and xiangqi-board)

**xiangqi-setup** is a command line tool using [svgutils](https://pypi.org/project/svgutils/) 0.3.1 to
render [Xiangqi](https://en.wikipedia.org/wiki/Xiangqi) (Chinese chess) board setups from WXF files to SVG images.

The most simple way to render a given setup is:

```
# xiangqi-setup input.wxf output.svg
```

For [demo.wxf](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo.wxf), the result is:

[![](https://raw.githubusercontent.com/hartwork/xiangqi-setup/master/doc/demo_retro_simple.png "demo_retro_simple.{png,svg}, CC0 1.0 Universal: Public Domain Dedication")](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo_retro_simple.svg)
[![](https://raw.githubusercontent.com/hartwork/xiangqi-setup/master/doc/demo_euro_xiangqi_js.png "demo_euro_xiangqi_js.{png,svg}, Creative Commons Attribution 4.0: Jasmin Scharrer, Sebastian Pipping")](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo_euro_xiangqi_js.svg)

(left: default board, default pieces — right: default board, `euro_xiangqi_js` pieces)

There are a number of themes to pick from for board and pieces (independently).
The `--help` listing below also includes the list of all themes
and their license information.

The [default board theme `clean_alpha`](https://github.com/hartwork/xiangqi-setup/blob/master/xiangqi_setup/themes/board/clean_alpha/board.svg)
has been generated with command line tool `xiangqi-board`
that is included with the **xiangqi-setup** package.  It can be used to create
variations of the detault theme, e.g. to create a version with reduced spacing
in crosses you would run:

```
# xiangqi-board --cross-gap-px 2 board.{svg,ini}
```


# Usage

## `xiangqi-setup` — render WXF files to SVG images

```
# xiangqi-setup --help
usage: xiangqi-setup [-h] [--board THEME] [--pieces THEME]
                     [--width-px PIXEL | --width-cm CENTIMETER] [--dpi FLOAT]
                     [--scale-pieces FACTOR] [--debug] [--version]
                     INPUT_FILE OUTPUT_FILE

positional arguments:
  INPUT_FILE            location of WXF file to render
  OUTPUT_FILE           location of SVG output file to write

optional arguments:
  -h, --help            show this help message and exit
  --debug               enable debugging (e.g. mark corners of the board)
  --version             show program's version number and exit

theme selection:
  --board THEME         name of board theme to use (default: "clean_alpha";
                        please check the list of available themes below
  --pieces THEME        name of pieces theme to use (default: "retro_simple";
                        please check the list of available themes below

scaling:
  --width-px PIXEL      width of the output in pixels
  --width-cm CENTIMETER
                        width of the output in centimeters
  --dpi FLOAT           resolution of the output in dots per inch
  --scale-pieces FACTOR
                        factor to scale pieces by (0.0 to 1.2, default: 0.9)

available board themes (in alphabetic order):
  a4_blank_2cm_margin                        (license: CC0-1.0)
  cambaluc_remake_nolegend                   (license: CC0-1.0)
  cambaluc_remake_nolegend_nogap             (license: CC0-1.0)
  ccbridge_3_0_beta4_default_preview_remake  (license: CC0-1.0)
  clean_alpha                                (license: CC0-1.0)
  clean_beta                                 (license: CC0-1.0)
  commons_xiangqi_board_2008                 (license: public-domain)
  commons_xiangqi_board_2008_bw_thin         (license: public-domain)
  dhtmlxq_2014_remake                        (license: CC0-1.0)
  latex_xq_remake                            (license: CC0-1.0)
  minimal                                    (license: CC0-1.0)
  minimal_chinese                            (license: CC0-1.0)
  minimal_chinese_arabic                     (license: CC0-1.0)
  playok_2014_remake                         (license: CC0-1.0)
  western_red_wine                           (license: CC0-1.0)
  xiexie_2_5_0_remake_minimal                (license: CC0-1.0)

available pieces themes (in alphabetic order):
  ccbridge_3_0_beta4_default_preview_remake  (license: CC0-1.0)
  commons_xiangqi_pieces_print_2010          (license: FDL-1.2+ / CC-BY-SA-4.0)
  commons_xiangqi_pieces_print_2010_bw_heavy (license: FDL-1.2+ / CC-BY-SA-4.0)
  euro_xiangqi_js                            (license: CC-BY-4.0)
  latex_xqlarge_2006_chinese_autotrace       (license: non-commercial)
  latex_xqlarge_2006_chinese_potrace         (license: non-commercial)
  playok_2014_chinese                        (license: CC0-1.0)
  playok_2014_chinese_noshadow               (license: CC0-1.0)
  retro_simple                               (license: CC0-1.0)
```


## `xiangqi-board` — create custom board themes

```
# xiangqi-board --help
usage: xiangqi-board [-h] [--line-thickness-px FLOAT] [--field-width-px FLOAT]
                     [--field-height-px FLOAT] [--border-thickness-px FLOAT]
                     [--border-gap-width-px FLOAT]
                     [--border-gap-height-px FLOAT] [--cross-width-px FLOAT]
                     [--cross-thickness-px FLOAT] [--cross-gap-px FLOAT]
                     SVG_FILE INI_FILE

positional arguments:
  SVG_FILE
  INI_FILE

optional arguments:
  -h, --help            show this help message and exit
  --line-thickness-px FLOAT
                        Line thickness of square fields in pixel (default: 1)
  --field-width-px FLOAT
                        Width of fields in pixel (default: 53)
  --field-height-px FLOAT
                        Height of fields in pixel (default: 53)
  --border-thickness-px FLOAT
                        Line thickness of border in pixel (default: 2)
  --border-gap-width-px FLOAT
                        Widtn of gap to border in pixel (default: 40)
  --border-gap-height-px FLOAT
                        Height of gap to border in pixel (default: 40)
  --cross-width-px FLOAT
                        Width of starting position cross segments in pixel
                        (default: 10)
  --cross-thickness-px FLOAT
                        Line thickness of starting position cross in pixel
                        (default: 1)
  --cross-gap-px FLOAT  Gap to starting position cross in pixel (default: 4)
```
