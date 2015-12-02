#!/usr/bin/env python

from __future__ import print_function

import sys
from tempfile import TemporaryFile
from zipfile import PyZipFile

import boto3
from botocore.exceptions import ClientError

assume_role_policy_document = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}"""

policy_document = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateSnapshot",
        "ec2:CreateTags",
        "ec2:DeleteSnapshot",
        "ec2:DescribeInstances",
        "ec2:DescribeSnapshots",
        "ec2:DescribeTags",
        "ec2:DescribeVolumes"
      ],
      "Resource": "*"
    }
  ]
}"""

function_name = 'ec2snapshot'
policy_name = 'LambdaSnapshotPolicy'
role_name = 'LambdaSnapshot'

def already_exists(e):
    return 'already exist' in str(e)

iam = boto3.resource('iam')

try:
    role = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=assume_role_policy_document
    )
except ClientError as e:
    if already_exists(e):
        role = iam.Role(role_name)

try:
    policy = iam.create_policy(
        PolicyName=policy_name,
        PolicyDocument=policy_document
    )
except ClientError as e:
    if already_exists(e):
        policy = role.Policy(policy_name)
        policy.put(
            PolicyDocument=policy_document
        )

lambda_client = boto3.client('lambda', region_name='us-east-1')

with TemporaryFile() as f:
    with PyZipFile(f, 'w') as z:
        z.write('ec2snapshot.py')
        z.write('boto')

    f.seek(0)

    zipped_bytes = f.read()

    def create():
        lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python2.7',
            Role=role.arn,
            Handler='ec2snapshot.lambda_handler',
            Description='Snapshot EBS volumes on all EC2 instances',
            Timeout=60,
            MemorySize=256,
            Code={
                'ZipFile': zipped_bytes
            }
        )

    try:
        create()

    except ClientError as e:
        if already_exists(e):
            lambda_client.delete_function(
                FunctionName=function_name
            )
            create()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

