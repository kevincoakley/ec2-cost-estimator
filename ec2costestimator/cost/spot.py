#!/usr/bin/env python

from ec2costestimator.cost.static_cost import StaticCost


class Spot(StaticCost):

    def __init__(self):
        pass

    @staticmethod
    def transform_region(region):
        if region == "us-east-1":
            return "us-east"
        if region == "us-west-1":
            return "us-west"
