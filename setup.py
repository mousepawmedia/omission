#!/usr/bin/env python

from setuptools import setup

setup(name='Omission',
      version='1.0',
      description='A deceptively simple word puzzle.',
      author='MousePaw Games',
      author_email='info@mousepawgames.com',
      url='https://www.mousepawgames.com/omission',
      license='BSD-3',
      packages=['omission',
                'omission.data',
                'omission.game',
                'omission.interface'],
      package_data={'omission': ['resources/audio/*.ogg',
                                 'resources/content/*.txt',
                                 'resources/font/open-dyslexic/*.otf',
                                 'resources/font/orbitron/*.otf',
                                 'resources/font/source-sans-pro/*.otf',
                                 'resources/icons/*.png',
                                 'interface/omission.kv'
                                ]
                   },
      entry_points={'gui_scripts': ['omission = omission.__main__:main']},
      install_requires=[
          'cython == 0.25.2',
          'kivy >= 1.10.0',
          'appdirs >= 1.4.3'
          ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Topic :: Games/Entertainment :: Puzzle Games'
          ]
     )
