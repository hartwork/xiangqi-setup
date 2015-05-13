#! /usr/bin/env python2
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import os
from distutils.core import setup

from xiangqi_setup.version import VERSION_STR


def _find_all_files_below(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            yield os.path.join(root, f)


def _fill_data_files(data_files_tuples, source_dir, dest_prefix):
    for source in _find_all_files_below(source_dir):
        dest = os.path.join(dest_prefix, os.path.dirname(os.path.relpath(source, source_dir)))
        data_files_tuples.append((dest, [source]))


if __name__ == '__main__':
    data_files_tuples = []
    _fill_data_files(data_files_tuples, 'themes', 'share/xiangqi-setup/themes/')

    setup(
            name='xiangqi-setup',
            description='Command line tool to generate razor-sharp Xiangqi (Chinese chess) setup graphics',
            license='GNU Affero General Public License version 3.0 or later',
            version=VERSION_STR,
            author='Sebastian Pipping',
            author_email='sebastian@pipping.org',
            url='https://github.com/hartwork/xiangqi-setup',
            download_url='https://github.com/hartwork/xiangqi-setup/archive/%s.tar.gz' % VERSION_STR,
            packages=[
                'xiangqi_board',
                'xiangqi_setup',
            ],
            scripts=[
                'xiangqi-board',
                'xiangqi-setup',
            ],
            data_files=data_files_tuples,
            classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: Education',
                'Intended Audience :: Other Audience',
                'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                'Natural Language :: English',
                'Programming Language :: Python',
                'Topic :: Artistic Software',
                'Topic :: Games/Entertainment :: Board Games',
                'Topic :: Multimedia :: Graphics',
                'Topic :: Printing',
                'Topic :: Other/Nonlisted Topic',
                'Topic :: Utilities',
            ],
    )
