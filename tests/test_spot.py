#!/usr/bin/env python

import unittest

from ec2costestimator.cost.spot import Spot


class SpotTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_find_spot_size_cost(self):

        with open("tests/cost/spot.js") as js_file:
            js = js_file.read()

        spot = Spot()

        output = spot.get_size_cost(js, "us-east-1", "m3.medium")
        self.assertEqual(output, "0.0113")
