#!/usr/bin/env python

from setuptools import setup

setup(
    name='ec2snapshot',
    version='0.0.2',
    author='Shawn Siefkas',
    author_email='shawn.siefkas@meredith.com',
    description='EBS Snapshots for EC2 Instances',
    install_requires=[
        'boto>=2.11.0',
    ],
    test_suite = 'test',
    py_modules = ['ec2snapshot'],
    entry_points={
        'console_scripts': ['ec2snapshot=ec2snapshot:main']
    },
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
