#!/usr/bin/env python

import fakes
import unittest
import datetime
from mock import patch
from mock import MagicMock
from ec2costestimator.cost.on_demand import OnDemand


class OnDemandTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('ec2costestimator.cost.on_demand', fakes.FakeOnDemand)
    @patch.object(fakes.FakeOnDemand, 'get_js_file')
    def test_on_demand_current_cost(self, mock_get_js_file):

        on_demand = OnDemand("ABC", "123", "us-east-1")

        output = on_demand.get_current_cost("m3.medium")
        self.assertEqual(output, "0.067")

    @patch('boto3.resource', fakes.FakeBoto3)
    @patch.object(fakes.FakeBoto3, 'Instance')
    def test_on_demand_get_instance_cost(self, mock_instance):

        instance = MagicMock()
        instance.launch_time = "2016-01-01 01:00:00+00:00"
        instance.instance_type = "m3.medium"
        instance.placement = {"AvailabilityZone": "us-east-1b"}

        mock_instance.return_value = instance

        on_demand = OnDemand("ABC", "123", "us-east-1")

        strptime = datetime.datetime.strptime

        # Test a 10 minute running time
        dt = datetime.datetime(2016, 1, 1, 1, 10, 0)
        with patch('datetime.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = dt
            datetime_mock.strptime = strptime

            output = on_demand.get_instance_cost("i-12345678")
            self.assertEqual(output, 0.067)

        # Test a 2 hour and 10 minute running time
        dt = datetime.datetime(2016, 1, 1, 3, 10, 0)
        with patch('datetime.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = dt
            datetime_mock.strptime = strptime

            output = on_demand.get_instance_cost("i-12345678")
            self.assertEqual(output, 0.201)
