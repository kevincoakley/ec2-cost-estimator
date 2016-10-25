#!/usr/bin/env python

import fakes
import unittest
from mock import patch
from mock import MagicMock
import datetime
from dateutil.tz import tzutc
from ec2costestimator.cost.spot import Spot


class SpotTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('boto3.client', fakes.FakeBoto3)
    @patch.object(fakes.FakeBoto3, 'describe_spot_price_history')
    def test_spot_current_cost(self, mock_describe_spot_price_history):

        mock_describe_spot_price_history.return_value = {
            'NextToken': 'abc123',
            'SpotPriceHistory': [
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 10, 6, 0, 7, 59, tzinfo=tzutc()),
                    'SpotPrice': '0.012200',
                    'InstanceType': 'm3.medium'
                }
            ]
        }

        spot = Spot("ABC", "123", "us-east-1")

        spot_history = spot.get_current_cost("us-east-1b", "m3.medium")

        self.assertEqual(spot_history, "0.012200")

    @patch('boto3.resource', fakes.FakeBoto3)
    @patch.object(fakes.FakeBoto3, 'Instance')
    @patch('boto3.client', fakes.FakeBoto3)
    @patch.object(fakes.FakeBoto3, 'describe_spot_price_history')
    def test_spot_get_instance_cost(self, mock_describe_spot_price_history, mock_instance):

        instance = MagicMock()
        instance.launch_time = datetime.datetime(2016, 1, 1, 1, 0, 0, tzinfo=tzutc())
        instance.instance_type = "m3.medium"
        instance.placement = {"AvailabilityZone": "us-east-1b"}

        mock_instance.return_value = instance

        mock_describe_spot_price_history.return_value = {
            'NextToken': 'abc123',
            'SpotPriceHistory': [
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 10, 0, tzinfo=tzutc()),
                    'SpotPrice': '0.012200',
                    'InstanceType': 'm3.medium'
                },
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 5, 0, tzinfo=tzutc()),
                    'SpotPrice': '0.013200',
                    'InstanceType': 'm3.medium'
                },
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 2, 30, tzinfo=tzutc()),
                    'SpotPrice': '0.012200',
                    'InstanceType': 'm3.medium'
                },
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 0, 0, tzinfo=tzutc()),
                    'SpotPrice': '0.013200',
                    'InstanceType': 'm3.medium'
                }
            ]
        }

        # Compute the spot price for the instances
        spot_instance_cost = .0122 * (1200 / 3600)
        spot_instance_cost += .0132 * (300 / 3600)
        spot_instance_cost += .0122 * (150 / 3600)
        spot_instance_cost += .0132 * (150 / 3600)
        spot_instance_cost = round(spot_instance_cost, 4)

        spot = Spot("ABC", "123", "us-east-1")

        strptime = datetime.datetime.strptime

        # Test a 30 minute running time
        dt = datetime.datetime(2016, 1, 1, 1, 30, 0)
        with patch('datetime.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = dt
            datetime_mock.strptime = strptime

            output = spot.get_instance_cost("i-12345678")
            self.assertEqual(output, spot_instance_cost)

    @patch('boto3.resource', fakes.FakeBoto3)
    @patch.object(fakes.FakeBoto3, 'Instance')
    @patch('boto3.client', fakes.FakeBoto3)
    @patch.object(fakes.FakeBoto3, 'describe_spot_price_history')
    def test_spot_get_instances_cost(self, mock_describe_spot_price_history, mock_instance):

        instance = MagicMock()
        instance.launch_time = datetime.datetime(2016, 1, 1, 1, 0, 0, tzinfo=tzutc())
        instance.instance_type = "m3.medium"
        instance.placement = {"AvailabilityZone": "us-east-1b"}

        mock_instance.return_value = instance

        mock_describe_spot_price_history.return_value = {
            'NextToken': 'abc123',
            'SpotPriceHistory': [
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 10, 0, tzinfo=tzutc()),
                    'SpotPrice': '0.012200',
                    'InstanceType': 'm3.medium'
                },
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 5, 0, tzinfo=tzutc()),
                    'SpotPrice': '0.013200',
                    'InstanceType': 'm3.medium'
                },
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 2, 30, tzinfo=tzutc()),
                    'SpotPrice': '0.012200',
                    'InstanceType': 'm3.medium'
                },
                {
                    'AvailabilityZone': 'us-east-1b',
                    'ProductDescription': 'Linux/UNIX',
                    'Timestamp': datetime.datetime(2016, 1, 1, 1, 0, 0, tzinfo=tzutc()),
                    'SpotPrice': '0.013200',
                    'InstanceType': 'm3.medium'
                }
            ]
        }

        # Compute the spot price for the instances
        spot_instance_cost = .0122 * (1200 / 3600)
        spot_instance_cost += .0132 * (300 / 3600)
        spot_instance_cost += .0122 * (150 / 3600)
        spot_instance_cost += .0132 * (150 / 3600)
        spot_instance_cost = round(spot_instance_cost, 4)

        spot = Spot("ABC", "123", "us-east-1")

        strptime = datetime.datetime.strptime

        # Test 1 instance with 30 minute running time
        dt = datetime.datetime(2016, 1, 1, 1, 30, 0)
        with patch('datetime.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = dt
            datetime_mock.strptime = strptime

            output = spot.get_instances_cost(["i-12345678"])
            self.assertEqual(output, spot_instance_cost)

        # Test 5 instance with 30 minute running time
        dt = datetime.datetime(2016, 1, 1, 1, 30, 0)
        with patch('datetime.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = dt
            datetime_mock.strptime = strptime

            output = spot.get_instances_cost(["i-12345678", "i-23456789", "i-345678901",
                                              "i-456789012", "i-567890123"])
            self.assertEqual(output, spot_instance_cost * 5)
