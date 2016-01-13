#!/usr/bin/env python
import os
from setuptools import setup


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


setup(
    name='auto-encoder',
    version='0.0.1',
    description='Frontend encode tool with avconv.',
    long_description=readme(),
    author='Takashi Ando',
    url='',
    packages=[
        'auto_encoder'],
    install_requires=requirements(),
    entry_points={
        'console_scripts': [
            'auto_encoder = auto_encoder.__main__:main'
            ]
        }
    )
