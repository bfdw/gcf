#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from setuptools import setup, find_packages
from setuptools import setup, find_packages
from codecs import open
from os import path

readme = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(readme, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

description = 'A Gadio infomation mining tool for fans of g-cores.com.'

params = dict(name='gcf',
              version='0.0.3.dev2',
              description=description,
              long_description=long_description,
              long_description_content_type='text/markdown',
              author='riceknight',
              author_email='riceknight@outlook.com',
              packages=find_packages(),
              include_package_data=True,
              url='https://github.com/bfdw/gcf',
              license='MIT',
              download_url='https://github.com/bfdw/gcf',
              python_requires='>=2.7',
              install_requires=[
                  'Click',
                  'bs4',
                  'requests',
                  'wcwidth',
                  'pandas',
                  'tabulate',
              ],
              entry_points='''
                    [console_scripts]
                    gcf=gcf.gcf:main
              ''',)

if __name__ == '__main__':
    setup(**params)
