#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-zendesk',
<<<<<<< HEAD
      version='2.8.0',
=======
      version='2.8.2',
>>>>>>> origin/master
      description='Singer.io tap for extracting data from the Zendesk API',
      author='Stitch',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_zendesk'],
      install_requires=[
          'singer-python==6.8.0',
          'zenpy==2.0.57',
          'backoff==2.2.1',
<<<<<<< HEAD
          'requests==2.34.2',
          'aiohttp==3.14.0'
=======
          'requests==2.33.0',
          'aiohttp==3.13.4'
>>>>>>> origin/master
      ],
      extras_require={
          'dev': [
              'ipdb',
          ],
          'test': [
              'pylint==3.0.3',
              'nose2',
              'pytest',
              'parameterized'
          ]
      },
      entry_points='''
          [console_scripts]
          tap-zendesk=tap_zendesk:main
      ''',
      packages=find_packages(),
      include_package_data=True,
)
