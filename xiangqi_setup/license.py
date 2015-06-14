# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

from __future__ import print_function

import json
import os
from textwrap import dedent


_LICENSE_DETAILS = {
    'CC-BY-4.0': (
        'Creative Commons Attribution 4.0',
        'https://creativecommons.org/licenses/by/4.0/',
        ),
    'CC-BY-SA-4.0': (
        'Creative Commons Attribution-ShareAlike 4.0',
        'https://creativecommons.org/licenses/by-sa/4.0/',
        ),
    'CC0-1.0': (
        'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'https://creativecommons.org/publicdomain/zero/1.0/',
        ),
    'FDL-1.2+': (
        'GNU Free Documentation License 1.2 or later',
        'https://gnu.org/licenses/fdl.html',
        ),
    'non-commercial': (
        'Non-commercial use only',
        None,
        ),
    'public-domain': (
        'Public domain',
        'https://en.wikipedia.org/wiki/Public_domain',
        )
}


def _get_license_json_path(single_theme_dir):
    return os.path.join(single_theme_dir, 'LICENSE.json')


def _get_license_json(single_theme_dir):
    license_json_path = _get_license_json_path(single_theme_dir)
    f = open(license_json_path, 'r')
    content = f.read()
    try:
        doc = json.loads(content)
    except ValueError as e:
        raise ValueError('%s (file "%s")' % (e, license_json_path))
    f.close()
    return doc['work']


def get_license_choices_of_theme(single_theme_dir):
    top_work = _get_license_json(single_theme_dir)
    try:
        return [top_work['license_id']]
    except KeyError:
        try:
            return top_work['license_ids_any_of']
        except KeyError:
            raise ValueError('Malformed license file "%s"' \
                    % _get_license_json_path(single_theme_dir))


def _describe_license(license_id):
    try:
        long_name, details_url = _LICENSE_DETAILS[license_id]
    except KeyError:
        return license_id

    if details_url is None:
        return long_name
    else:
        return '%s  (%s)' % (long_name, details_url)


def inform_license(board_theme_dir, pieces_theme_dir):
    print('The license of the themes used apply to the generated image.  In detail:')
    print()

    for category, theme_dir in (
            ('Board', board_theme_dir),
            ('Pieces', pieces_theme_dir),
            ):
        top_work = _get_license_json(theme_dir)


        author_chunks = []
        for author_dict in top_work['authors']:
            for author_name, details_dict in author_dict.items():
                contact_infos = []

                if 'website' in details_dict:
                    contact_infos.append(details_dict['website'])

                if 'email' in details_dict:
                    contact_infos.append('%s@%s' % tuple(details_dict['email']))

                if contact_infos:
                    author_display = '%s (%s)' % (author_name, ', '.join(contact_infos))
                else:
                    author_display = author_name

                author_chunks.append(author_display)
        authors = '\n'.join(('    ' + e) for e in author_chunks)


        try:
            license_ids_any_of = [top_work['license_id']]
        except KeyError:
            try:
                license_ids_any_of = top_work['license_ids_any_of']
            except KeyError:
                raise ValueError('Malformed license file "%s"' % _get_license_json_path(theme_dir))

        if len(license_ids_any_of) == 1:
            license_options = '    %s' % _describe_license(license_ids_any_of[0])
        else:
            license_options = '\n'.join(
                    ('    %s) %s' % (chr(ord('a') + i), _describe_license(e))) \
                    for i, e \
                    in enumerate(license_ids_any_of))


        print(dedent("""\
            %s theme:
              Author(s):
            %s
              License options:
            %s
            """) % (category, authors, license_options))

    print('If this license does not work for you, please pick a different board theme and/or pieces theme.'
        '  '
        'Thank you!')
