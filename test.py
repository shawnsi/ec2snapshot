import unittest
import boto
from ec2snapshot import get_instance_by_id
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

    def tearDown(self):
        # Cleanup moto environment
        self.mock.stop()

    def test_get_instance_by_id(self):
        instance_id = self.instance_ids[0]
        instance = get_instance_by_id(instance_id)
        self.assertEqual(instance.id, instance_id)
