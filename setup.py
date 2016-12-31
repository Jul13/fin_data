#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'h5py',
    'pandas',
    'pip',
    'tables',
    'pykalman'
]

setup(
    name='fin_data',
    version='0.1.0',
    description="Utilities for reading and analyzing financial data.",
    long_description=readme + '\n\n' + history,
    author="Gheorghe Postelnicu",
    author_email='gheorghe.postelnicu@gmail.com',
    url='https://github.com/gpostelnicu/fin_data',
    packages=[
        'fin_data',
    ],
    package_dir={'fin_data':
                 'fin_data'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='fin_data',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=requirements
)
