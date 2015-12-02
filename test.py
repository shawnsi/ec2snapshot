import os
import unittest
import boto
import boto3
from ec2snapshot import get_volumes_by_instance
from moto import mock_ec2


class Ec2SnapshotTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

        # Start moto environment
        self.mock = mock_ec2()
        self.mock.start()

        # Create mocked ec2 boto client
        self.ec2 = boto3.resource('ec2')

        # Create 10 random instances for testing
        self.instances = self.ec2.create_instances(ImageId='ami-mock', MinCount=5, MaxCount=5)

        # Create 3 random volumes for testing
        self.volumes = []
        for i in range(3):
            volume = self.ec2.create_volume(Size=10, AvailabilityZone='zone-mock')
            self.volumes.append(volume)


    def tearDown(self):
        # Cleanup moto environment
        self.mock.stop()


    def test_get_volumes_by_instance(self):
        instance = self.instances[0]
        expected = []

        for volume, suffix in zip(self.volumes, ['f', 'g', 'h']):
            device = '/dev/sd%s' % suffix
            instance.attach_volume(VolumeId=volume.id, Device=device)
            expected.append((device, volume))

        volumes = get_volumes_by_instance(self.ec2, instance)
        self.assertListEqual(expected, list(volumes))
