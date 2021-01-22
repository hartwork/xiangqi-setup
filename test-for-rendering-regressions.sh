#! /usr/bin/env bash
# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

set -e
set -x

convert -version

assert_images_identical() {
    local a="${1}"
    local b="${2}"
    local diff_output="${3}"
    compare -metric AE "${a}" "${b}" "${diff_output}"
}

render_and_compare() {
    local theme_type="${1}"
    local theme_name="${2}"
    local prefix_actual="tests/actual-${theme_type}-${theme_name}"
    local prefix_expected="tests/expected-${theme_type}-${theme_name}"
    local prefix_difference="tests/difference-${theme_type}-${theme_name}"
    local colorspace='-define png:color-type=6 -define png:bit-depth=8'  # i.e. 32bit RGBA

    xiangqi-setup "--${theme_type}" "${theme_name}" doc/demo.wxf "${prefix_actual}".svg > /dev/null
    # NOTE: We normalize both images to the same color space and depth before comparison
    #       so that only a "true difference in color value" can cause a diff here.
    convert ${colorspace} -verbose -background none "${prefix_actual}".{svg,png}
    convert ${colorspace} "${prefix_expected}".png{,}  # in-place
    assert_images_identical {"${prefix_expected}","${prefix_actual}","${prefix_difference}"}.png

    rm "${prefix_actual}".{png,svg}
    rm "${prefix_difference}".png
}

# Board themes
for theme_name in xiangqi_setup/themes/board/* ; do
    theme_name="${theme_name##xiangqi_setup/themes/board/}"
    [[ "${theme_name}" = __init__.py ]] && continue
    [[ "${theme_name}" = __pycache__ ]] && continue

    render_and_compare board "${theme_name}"
done

# Piece themes
for theme_name in xiangqi_setup/themes/pieces/* ; do
    theme_name="${theme_name##xiangqi_setup/themes/pieces/}"
    [[ "${theme_name}" = __init__.py ]] && continue
    [[ "${theme_name}" = __pycache__ ]] && continue
    [[ "${theme_name}" = diamond.svg ]] && continue

    render_and_compare pieces "${theme_name}"
done
