#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def readme():
    try:
        os.system("pandoc --from=markdown --to=rst README.md -o README.rst")
        with open("README.rst", "r") as f:
            return f.read()
    except:
        return ""


def requirements():
    try:
        return [pkg.strip() for pkg in open('requirements.txt', 'r').readlines()]
    except:
        return []


def packages():
    return find_packages(exclude=['*test*', '*.egg-info'])


setup(
    name='auto-encoder',
    version='0.0.1',
    description='Frontend encode tool with avconv.',
    long_description=readme(),
    author='Takashi Ando',
    url='',
    packages=packages(),
    install_requires=requirements(),
    entry_points={
        'console_scripts': [
            'auto_encoder = auto_encoder.__main__:main'
        ]
    },
    test_suite='nose.collector'
)
