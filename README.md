ec2snapshot
===========

[![Build Status](https://travis-ci.org/shawnsi/ec2snapshot.png)](https://travis-ci.org/shawnsi/ec2snapshot)

Snapshot EBS Devices Attached to EC2 Instances

Requirements
------------

The script depends on [boto](http://boto.readthedocs.org/en/latest/).  It has been tested on RHEL 6.5 on AWS successfully.

Installation
------------

Install via pip:

```bash
$ git clone https://github.com/shawnsi/ec2snapshot.git
$ cd ec2snapshot
$ pip install .
```

Usage
-----

This script is dead simple.  It expects to lookup the local instance information via [boto.utils.get_instance_metadata](http://boto.readthedocs.org/en/latest/ref/boto.html?highlight=get_instance_metadata#boto.utils.get_instance_metadata).  The AWS credentials should be provided by [IAM roles for EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html).

Run the script to snapshot all attached EBS volumes.

```bash
$ ec2snapshot
```

Trimming
--------

The builtin [boto.ec2.trip_snapshots](http://boto.readthedocs.org/en/latest/ref/ec2.html?highlight=trim_snapshot#boto.ec2.connection.EC2Connection.trim_snapshots) method is used to cleanup snapshots.  This is executed at the end of each run and will affect all snapshots associated with the AWS account.

IAM Role
--------

Assign an IAM Role to the EC2 instance with these permissions at a minimum.

```json
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
"Resource": [
  "*"
]
```
