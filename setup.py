#!/usr/bin/env python3
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='Omission',
    version='1.0.0',
    description='A deceptively simple word puzzle.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MousePaw Games',
    author_email='info@mousepawmedia.com',
    url='https://www.mousepawgames.com/omission',

    project_urls={
        'Bug Reports': 'https://phabricator.mousepawmedia.net',
        'Source': 'https://github.com/mousepawmedia/omission',
    },
    keywords='game, words',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment :: Puzzle Games'
        ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),

    include_package_data=True,

    python_requires='>=3.7, <4',
    install_requires=[
        'kivy >= 2.0.0',
        'appdirs >= 1.4.3'
        ],

    entry_points={
        'gui_scripts': [
            'omission = omission.__main__:main'
        ]
    }
)
