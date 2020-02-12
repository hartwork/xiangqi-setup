#! /usr/bin/env python2
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero General Public License version 3.0 or later

import os
from setuptools import find_packages, setup

from xiangqi_setup.version import VERSION_STR


def _generate_package_data():
    return {
        root.replace(os.sep, '.'): files
        for root, dirs, files
        in os.walk('xiangqi_setup/themes')
    }


if __name__ == '__main__':
    setup(
            name='xiangqi-setup',
            description='Command line tool to generate razor-sharp Xiangqi (Chinese chess) setup graphics',
            license='GNU Affero General Public License version 3.0 or later',
            version=VERSION_STR,
            author='Sebastian Pipping',
            author_email='sebastian@pipping.org',
            url='https://github.com/hartwork/xiangqi-setup',
            download_url='https://github.com/hartwork/xiangqi-setup/archive/%s.tar.gz' % VERSION_STR,
            packages=find_packages(),
            package_data=_generate_package_data(),
            scripts=[
                'xiangqi-board',
                'xiangqi-setup',
            ],
            install_requires=[
                'svgutils>=0.3.1',
            ],
            classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: Education',
                'Intended Audience :: Other Audience',
                'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                'Natural Language :: English',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 2 :: Only',
                'Topic :: Artistic Software',
                'Topic :: Games/Entertainment :: Board Games',
                'Topic :: Multimedia :: Graphics',
                'Topic :: Printing',
                'Topic :: Utilities',
            ],
    )
