# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import json
import os


def get_license_choices_of_theme(single_theme_dir):
    license_json_path = os.path.join(single_theme_dir, 'LICENSE.json')
    f = open(license_json_path, 'r')
    content = f.read()
    try:
        doc = json.loads(content)
    except ValueError as e:
        raise ValueError('%s (file "%s")' % (e, license_json_path))
    f.close()

    top_work = doc['work']
    try:
        return [top_work['license_id']]
    except KeyError:
        try:
            return top_work['license_ids_any_of']
        except KeyError:
            raise ValueError('Malformed license file "%s"' % license_json_path)
