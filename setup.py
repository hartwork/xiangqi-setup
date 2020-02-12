#! /usr/bin/env python
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
            long_description=open('README.md').read(),
            long_description_content_type='text/markdown',
            license='GNU Affero General Public License version 3.0 or later',
            version=VERSION_STR,
            author='Sebastian Pipping',
            author_email='sebastian@pipping.org',
            url='https://github.com/hartwork/xiangqi-setup',
            download_url='https://github.com/hartwork/xiangqi-setup/archive/%s.tar.gz' % VERSION_STR,
            packages=find_packages(),
            package_data=_generate_package_data(),
            entry_points={
                'console_scripts': [
                    'xiangqi-board = xiangqi_board.__main__:main',
                    'xiangqi-setup = xiangqi_setup.__main__:main',
                ],
            },
            setup_requires=[
                'setuptools>=38.6.0',  # for long_description_content_type
            ],
            install_requires=[
                'six',
                'svgutils==0.3.1',  # unreleased svgutils Git master breaks
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
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Topic :: Artistic Software',
                'Topic :: Games/Entertainment :: Board Games',
                'Topic :: Multimedia :: Graphics',
                'Topic :: Printing',
                'Topic :: Utilities',
            ],
    )
