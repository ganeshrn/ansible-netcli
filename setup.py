#!/usr/bin/env python

# Copyright (c) 2019 Red Hat, Inc.
# All Rights Reserved.

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="ansible-netcli",
    version="2.8.0",
    author='Red Hat Ansible Network',
    url="https://github.com/ganeshrn/ansible-netcli",
    license='Apache',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    package_data={
        '': [
            'models/*/*/*.*',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'six',
    ],
    zip_safe=False,
)
