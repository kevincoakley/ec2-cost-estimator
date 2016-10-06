#!/usr/bin/env python

import fakes
import unittest
from mock import patch
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
