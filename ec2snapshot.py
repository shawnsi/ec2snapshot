#!/usr/bin/python

import boto.ec2


def get_instance_by_id(instance_id, region):
	"""
	Returns the boto.ec2.Instance object with id `instance_id`.
	"""
	ec2 = boto.ec2.connect_to_region(region)
	reservations = ec2.get_all_instances(instance_ids=[instance_id])
	return reservations[0].instances[0]


def get_volumes_by_instance(instance):
	"""
	Returns a list of volumes attached to `instance`.
	"""
	def attached(volume):
		return volume.attach_data.instance_id == instance.id

	return [v for v in instance.connection.get_all_volumes() if attached(v)]


def instance_id():
	# Replace this with the appropriate instance from local instance metadata
	metadata = boto.utils.get_instance_identity()['document']
	return get_instance_by_id(metadata['instanceId'], metadata['region'])


if __name__ == '__main__':
	instance = local_instance()
	for volume in get_volumes_by_instance(instance):
		volume.create_snapshot()

	instance.connection.trim_snapshots()
