# xiangqi-setup File Formats

When introducing the annotation feature to **xiangqi-setup**,
it became clear that it was practical
to have both the board setup and annotations in one single file.
In that context, two new file formats were born:

- [annoFEN](#annofen) — a format very close to plain FEN but with support for annotations added — and
- [XAY](#xay) — short for "**x**iangqi-setup **a**nnotated **Y**AML".

For the support for [annotations](#annotations) and their code names ()that are common to both file formats [annoFEN](#annofen) and [XAY](#xay)),
please see the dedicated section [Annotations](#annotations) below.


## <a name="annofen"></a>annoFEN File Format

### Overview

You are probably already familiar with FEN (as easily editable on [pychess.org](https://www.pychess.org/editor/xiangqi)).  With plain FEN, the default setup looks like this:

```
rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1
```

annoFEN version 1 does four things differently:

- It adds a prefix "v1 " (to distinguish version 1 from other versions in the future)
- It drops the "w - - 0 1" game stat part as unnecessary
- It adds support for [annotations](#annotations)
  using `<code>` angle bracket syntax
- It adds support for more than one piece/annotation per field
  using `[..]` square bracket syntax

With annoFEN, the default setup looks like this:

```
v1 rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR
```

Now let's have Red/White play the most common move, have Black reply
and highlight these last two moves — this situation:

![tests/expected-annotations-colors_alpha-last-two-moves.png](https://raw.githubusercontent.com/hartwork/xiangqi-setup/master/tests/expected-annotations-colors_alpha-last-two-moves.png)

Using the new `<code>` and `[..]` syntax and three [annotations](#annotations)
we end up with [this annoFEN content](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-last-two-moves.annofen):

```
v1 r[<bm><a+1-2>]bakabnr/9/1c[<pm>n]4c1/p1p1p1p1p/9/9/P1P1P1P1P/1C2[<pm>C]2[<bm><a-3+0>]1/9/RNBAKABNR
```


### Examples

There are two example annoFEN files that come with **xiangqi-setup**:

- [`doc/demo-last-two-moves.annofen`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-last-two-moves.annofen)
- [`doc/initial.annofen`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/initial.annofen)


## <a name="xay"></a>XAY File Format

### Overview

A XAY file — an "**x**iangqi-setup **a**nnotated **Y**AML" file — is a YAML file with a few simple constraints.  At the document root, there are two keys — string `version` and `setup`, a list of lists of lists.  The nested list part will make sense in a minute.  Here's (a rather verbose version) of the empty board:

```yaml
version: '1'
setup: [
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
  # river
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
  [[], [], [], [], [], [], [], [], []],
]
```

In this example `setup` is list if 10 lists ("rows") each holding 9 lists ("columns") of the pieces and annotations present at that location on the board.

Let's continue with putting the default setup on the board:

```yaml
version: '1'
setup: [
  [[r], [h], [e], [a], [k], [a], [e], [h], [r]],
  [],
  [[], [c], [], [], [], [], [], [c]],
  [[p], [], [p], [], [p], [], [p], [], [p]],
  [],
  # river
  [],
  [[P], [], [P], [], [P], [], [P], [], [P]],
  [[], [C], [], [], [], [], [], [C]],
  [],
  [[R], [H], [E], [A], [K], [A], [E], [H], [R]],
]
```

Lower letters represent the pieces of Black,
upper letters represent the pieces of Red/White.

Most empty fields have been omitted since XAY supports sparse notation.


### Examples

There are six example XAY files that come with **xiangqi-setup**:

- [`doc/demo-arrows-horse-elephant-advisor.xay`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-arrows-horse-elephant-advisor.xay)
- [`doc/demo-arrows-rook-downwards.xay`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-arrows-rook-downwards.xay)
- [`doc/demo-arrows-rook-leftwards-rightwards.xay`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-arrows-rook-leftwards-rightwards.xay)
- [`doc/demo-arrows-rook-upwards.xay`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-arrows-rook-upwards.xay)
- [`doc/demo-movement-horse.xay`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-movement-horse.xay)
- [`doc/initial.xay`](https://github.com/hartwork/xiangqi-setup/blob/master/doc/initial.xay)


## <a name="annotations"></a>Annotations

### Overview

**xiangqi-setup** supports seven different annotations for a field.
A field can have multiple annotations (and a piece or be blank).
The available annotations are:

- *name* (code *`code`*) — *description*
- `arrow_*` (code `a????`, see further down) — adds an arrow starting at that very field
- `blank_bad` (code `bb`) — adds a marker to indicate that a blank field is "bad"
- `blank_good` (code `bg`) — adds a marker to indicate that a blank field is "bad"
- `blank_move` (code `bm`) — adds a marker to indicate that a blank field is involved with a move
- `piece_bad` (code `pb`) — adds a marker to indicate that a field occupied by a piece is "bad"
- `piece_good` (code `pg`) — adds a marker to indicate that a field occupied by a piece is "good"
- `piece_move` (code `pm`) — adds a marker to indicate that a field occupied by a piece is involved with a move


### Example

With those codes, we can now e.g. visualize how the horse/knight moves:

![expected-annotations-colors_alpha-movement-horse.png](https://raw.githubusercontent.com/hartwork/xiangqi-setup/master/tests/expected-annotations-colors_alpha-movement-horse.png)

The [related XAY content](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-movement-horse.xay) looks like this:

```yaml
version: '1'
setup: [
  [],
  [],
  [],
  [[], [], [], [bg], [], [R, pg]],
  [[], [], [bg], [], [], [], [bb]],
  # river
  [[], [], [], [], [n], [c, pb]],
  [[], [], [bg], [], [], [], [bb]],
  [[], [], [], [bg], [], [bg]],
]
```

### <a name="arrows"></a>Arrows

Adding arrows works quite the same: The arrow name codes follow format `a(+|-)<dx>(+|-)<dy>`
where `(+|-)` means either a `+` (plus) or a `-` (minus)
and `<dx>` and `<dy>` are the distance in columns (dx) and rows (dy).
So `a+8+0` is a arrow for a move that travels 8 columns to the right and remains on the same row, likely by a rook or a cannon.
For another example, code `a+2-1` would be one of 8 possible arrows to indicate a knight-like move.

This example demonstrates all available downwards arrows common to rooks, cannons, pawns and kings:

![expected-annotations-colors_alpha-arrows-rook-downwards.png](https://raw.githubusercontent.com/hartwork/xiangqi-setup/master/tests/expected-annotations-colors_alpha-arrows-rook-downwards.png)

The [related XAY content](https://github.com/hartwork/xiangqi-setup/blob/master/doc/demo-arrows-rook-downwards.xay) looks like this:

```yaml
version: '1'
setup: [
  [[a+0-1, bm], [a+0-2], [a+0-3], [a+0-4], [a+0-5], [a+0-6], [a+0-7], [a+0-8], [a+0-9]],
  [[r, pm]],
  [[], [r]],
  [[], [], [r]],
  [[], [], [], [r]],
  # river
  [[], [], [], [], [r]],
  [[], [], [], [], [], [r]],
  [[], [], [], [], [], [], [r]],
  [[], [], [], [], [], [], [], [r]],
  [[], [], [], [], [], [], [], [], [r]],
]
```
