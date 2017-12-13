#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

version_string = '0.7'

with open("requirements.txt", 'r') as f:
    required_packages = f.read().splitlines()


setuptools.setup(
    name="spss-sav-pseudonymization",
    version=version_string,
    url="https://github.com/thehyve/spss-sav-pseudonymization",

    author="Jochem Bijlard",
    author_email="jochem@thehyve.nl",

    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,

    download_url='https://github.com/thehyve/spss-sav-pseudonymization/tarball/{}/'.format(version_string),

    install_requires=required_packages,

    entry_points={
        'console_scripts': [
            'pseudonymise = spss_sav_pseudonymization.pseudonymise:pseudonymise'
        ]
    },

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)