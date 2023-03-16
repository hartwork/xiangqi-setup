#! /usr/bin/env bash
# Copyright (C) 2021 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

set -e
set -x

any_file_missing=0

convert -version

assert_images_equal_enough() {
    local a="${1}"
    local b="${2}"
    local diff_output="${3}"
    local diff_pixel_count="$(compare -metric AE "${a}" "${b}" "${diff_output}" 2>&1)"
    [[ "${diff_pixel_count}" =~ [0-9]+ && "${diff_pixel_count}" -le 8 ]]
}

render_and_compare() {
    local theme_type="${1}"
    local theme_name="${2}"
    local input_file="${3:-doc/demo.wxf}"
    local suffix="${4:-}"
    local prefix_actual="tests/actual-${theme_type}-${theme_name}${suffix}"
    local prefix_expected="tests/expected-${theme_type}-${theme_name}${suffix}"
    local prefix_difference="tests/difference-${theme_type}-${theme_name}${suffix}"

    if [[ -e "${prefix_expected}".png ]]; then
        # We have an image to compare to, so let's do that
        xiangqi-setup "--${theme_type}" "${theme_name}" "${input_file}" "${prefix_actual}".svg > /dev/null
        convert -verbose -background none "${prefix_actual}".{svg,png}
        assert_images_equal_enough {"${prefix_expected}","${prefix_actual}","${prefix_difference}"}.png

        rm "${prefix_actual}".{png,svg}
        rm "${prefix_difference}".png
    else
        # We do not have an image to compare to, so let's generate it and signal failure to the outside
        any_file_missing=1
        xiangqi-setup "--${theme_type}" "${theme_name}" "${input_file}" "${prefix_expected}".svg > /dev/null
        convert -verbose -background none "${prefix_expected}".{svg,png}
        zopflipng -y "${prefix_expected}".png{,}
        rm "${prefix_expected}".svg
    fi
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

# Annotation themes
for theme_name in xiangqi_setup/themes/annotations/* ; do
    theme_name="${theme_name##xiangqi_setup/themes/annotations/}"
    [[ "${theme_name}" = __init__.py ]] && continue
    [[ "${theme_name}" = __pycache__ ]] && continue

    for input_file in \
            doc/demo-arrows-*.xay \
            doc/demo-last-two-moves.annofen \
            doc/demo-movement-horse.xay \
            ; do
        suffix="${input_file##doc/demo}"
        suffix="${suffix%%.*}"
        render_and_compare annotations "${theme_name}" "${input_file}" "${suffix}"
    done
done

exit "${any_file_missing}"
