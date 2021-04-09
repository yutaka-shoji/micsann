# -*- coding: utf-8 -*-

import os, sys
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setup(
    name='micsann',
    version='0.1.0',
    description='Calculate temperature response function of the MICS-ANN model',
    long_description=readme,
    author='Yutaka Shoji',
    author_email='yshoji@eng.hokudai.ac.jp',
    url='https://github.com/yutaka-shoji/micsann',
    license=license,
    packages=['micsann'],
    package_data={'micsann': ['*.pth']},
    install_requires=read_requirements()
)

