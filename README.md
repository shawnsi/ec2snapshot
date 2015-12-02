# ec2snapshot

AWS Lambda function to snapshot EBS devices attached to EC2 instances

## Requirements

The script depends on [boto3](http://boto3.readthedocs.org/en/latest/).  It is provided by AWS lambda at runtime but the library is needed to execute the `upload.py` script locally.

## Installation

Set your AWS token via environment variables:

```bash
$ export AWS_ACCESS_KEY_ID=<XXXXXXXXXXXXXXXX>
$ export AWS_SECRET_ACCESS_KEY=<XXXXXXXXXXXXXXXX>
```

Run the `upload.py` script to setup IAM roles, policies, and lambda function for execution.

```bash
$ python upload.py
```

## Usage

### Filters

The lambda function can be passed filters as runtime to restrict which EC2 instances snapshotted:

```json
{
  "Filters": [
        {
            "Name": "tag:Name",
            "Values": [
                "*NFS*"
            ]
        },
        {
            "Name": "tag:Environment",
            "Values": [
                "Production"
            ]
        }
    ]
}
```

See [boto3 EC2 service resources](http://boto3.readthedocs.org/en/latest/reference/services/ec2.html#service-resource) for full documentation of the supported filters.

### Scheduling

Scheduled execution must be set up manually in the lambda console until boto3 adds support.

## Known Issues

### Trimming

The builtin [boto.ec2.trim_snapshots](http://boto.readthedocs.org/en/latest/ref/ec2.html?highlight=trim_snapshot#boto.ec2.connection.EC2Connection.trim_snapshots) method was not carried over to boto3.  I've opened an [issue](https://github.com/boto/boto3/issues/298) on the boto3 project to track this.  In the meantime we embed boto in this project to utilize the method.

