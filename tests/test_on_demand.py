#!/usr/bin/env python

import fakes
import unittest
from mock import patch
from ec2costestimator.cost.on_demand import OnDemand


class OnDemandTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('ec2costestimator.cost.on_demand', fakes.FakeOnDemand)
    @patch.object(fakes.FakeOnDemand, 'get_js_file')
    def test_on_demand_current_cost(self, mock_get_js_file):

        on_demand = OnDemand()

        output = on_demand.get_current_cost("us-east-1", "m3.medium")
        self.assertEqual(output, "0.067")
