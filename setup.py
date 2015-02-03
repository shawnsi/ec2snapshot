#!/usr/bin/env python

from setuptools import setup

setup(
    name='ec2snapshot',
    version='0.0.2',
    author='Shawn Siefkas',
    author_email='shawn.siefkas@meredith.com',
    description='EBS Snapshots for EC2 Instances',
    install_requires=[
        'boto>=2.34.0',
    ],
    test_suite = 'test',
    scripts = ['ec2snapshot']
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
