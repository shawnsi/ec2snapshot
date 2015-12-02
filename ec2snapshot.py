#!/usr/bin/python

from __future__ import print_function

import boto3

def get_volumes_by_instance(ec2, instance):
    """
    Generator that returns pairs of device name and volume objects for all non
    root EBS volumes on an instance.
    """
    for mapping in instance.block_device_mappings:
        if 'Ebs' in mapping:
            if mapping['DeviceName'] != instance.root_device_name:
                yield mapping['DeviceName'], ec2.Volume(mapping['Ebs']['VolumeId'])

def instance_name(instance):
    """
    Returns the value of the "Name" tag for an instance if present.
    """
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return "(%s)" % tag['Value']

def lambda_handler(event, context):
    # Load the runtime filters
    if not 'Filters' in event:
        event['Filters'] = []

    ec2 = boto3.resource('ec2')

    # Iterate over filtered instances and snapshot volumes
    for instance in ec2.instances.filter(Filters=event['Filters']):
        for device, volume in get_volumes_by_instance(ec2, instance):
            # Minimum description is instance id and device name
            description = '%s:%s' % (instance.id, device)

            # If available append the EC2 instance name
            name = instance_name(instance)
            if name:
                description += " %s" % name

            # Take the snapshots
            volume.create_snapshot(
                Description=description
            )

    trim_snapshots()

# boto legacy import to preserve trim_snapshots() behavior
def local_instance():
    """
    Convenience wrapper for getting boto.ec2.Instance object that represents localhost.
    """
    metadata = boto.utils.get_instance_identity()['document']
    return get_instance_by_id(metadata['instanceId'], metadata['region'])

def trim_snapshots():
    import boto.ec2
    import boto.utils

    metadata = boto.utils.get_instance_identity()['document']
    connection = boto.ec2.connect_to_region(metadata['region'])

    connection.trim_snapshots()
