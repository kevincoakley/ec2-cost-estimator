#!/usr/bin/env python

import unittest

from ec2costestimator.cost.on_demand import OnDemand


class OnDemandTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_find_on_demand_size_cost(self):

        with open("tests/cost/linux-od.min.js") as js_file:
            js = js_file.read()

        on_demand = OnDemand()

        output = on_demand.get_size_cost(js, "us-east-1", "m3.medium")
        self.assertEqual(output, "0.067")
