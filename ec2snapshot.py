#!/usr/bin/python

import boto
import boto.utils

def get_instance_by_id(instance_id):
    """
    Returns the boto.ec2.Instance object with id `instance_id`.
    """
    ec2 = boto.connect_ec2()
    instances = ec2.get_only_instances(instance_ids=[instance_id])
    return instances[0]


def get_volumes_by_instance(instance):
    """
    Returns a list of volumes attached to `instance`.
    """
    def attached(volume):
        return volume.attach_data.instance_id == instance.id

    return [v for v in instance.connection.get_all_volumes() if attached(v)]


def local_instance():
    """
    Convenience wrapper for getting boto.ec2.Instance object that represents localhost.
    """
    metadata = boto.utils.get_instance_metadata()
    return get_instance_by_id(metadata['instance-id'])


def main():
    instance = local_instance()

    for volume in get_volumes_by_instance(instance):
        volume.create_snapshot()

    instance.connection.trim_snapshots()
