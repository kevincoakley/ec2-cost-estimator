#!/usr/bin/env python

import fakes
import unittest
import datetime
from mock import patch
from mock import MagicMock
from ec2costestimator.ec2.instance_information import InstanceInformation


class InstanceInformationTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('boto3.resource', fakes.FakeBoto3)
    @patch.object(fakes.FakeBoto3, 'Instance')
    def test_instance_information(self, mock_instance):

        instance = MagicMock()
        instance.launch_time = "2016-01-01 01:00:00+00:00"
        instance.instance_type = "m3.medium"
        instance.placement = {"AvailabilityZone": "us-east-1b"}

        mock_instance.return_value = instance

        instance_information = InstanceInformation("ABC", "123", "us-east-1")

        strptime = datetime.datetime.strptime

        # Test a 10 minute running time
        dt = datetime.datetime(2016, 1, 1, 1, 10, 0)
        with patch('datetime.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = dt
            datetime_mock.strptime = strptime

            output = instance_information.get_instance_running_hours("i-12345678")
            self.assertEqual(output, 1)

        # Test a 2 hour and 10 minute running time
        dt = datetime.datetime(2016, 1, 1, 3, 10, 0)
        with patch('datetime.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = dt
            datetime_mock.strptime = strptime

            output = instance_information.get_instance_running_hours("i-12345678")
            self.assertEqual(output, 3)

        output = instance_information.get_instance_type("i-12345678")
        self.assertEqual(output, "m3.medium")

        output = instance_information.get_availability_zone("i-12345678")
        self.assertEqual(output, "us-east-1b")
