import unittest
import boto
from ec2snapshot import get_instance_by_id, get_volumes_by_instance
from moto import mock_ec2


class Ec2SnapshotTestCase(unittest.TestCase):

    def setUp(self):
        # Start moto environment
        self.mock = mock_ec2()
        self.mock.start()

        # Create mocked ec2 boto client
        self.conn = boto.connect_ec2()

        # Create 10 random instances for testing
        self.reservation = self.conn.run_instances('ami-mock', 10)
        self.instance_ids = [i.id for i in self.reservation.instances]

        # Create 3 random volumes for testing
        self.volumes = []
        for i in range(3):
            volume = self.conn.create_volume(10, 'zone-mock')
            self.volumes.append(volume)
        self.volume_ids = sorted([v.id for v in self.volumes])


    def tearDown(self):
        # Cleanup moto environment
        self.mock.stop()

    def test_get_instance_by_id(self):
        instance_id = self.instance_ids[0]
        instance = get_instance_by_id(instance_id, 'us-east-1')
        self.assertEqual(instance.id, instance_id)

    def test_get_volumes_by_instance(self):
        instance_id = self.instance_ids[0]
        instance = get_instance_by_id(instance_id, 'us-east-1')

        # Attach volumes to each instance
        for volume in self.volumes:
            for device in ('f', 'g', 'h'):
                    self.conn.attach_volume(volume.id, instance.id, '/dev/sd%s' % device)

        volumes = get_volumes_by_instance(instance)
        self.assertListEqual(self.volume_ids, sorted([v.id for v in volumes]))
