#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from setuptools import setup, find_packages
import setuptools

description = 'A Gadio infomation mining tool for fans of g-cores.com.'

params = dict(name='gcf',
              version='0.0.4',
              description=description,
              author='riceknight',
              author_email='riceknight@outlook.com',
              packages=setuptools.find_packages(),
              include_package_data=True,
              url='https://github.com/bfdw',
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
    setuptools.setup(**params)
