#!/usr/bin/env python

import argparse
from ec2costestimator.cost.on_demand import OnDemand
from ec2costestimator.cost.spot import Spot


def on_demand_current():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i",
                        metavar="instance_type",
                        dest="instance_type",
                        required=True)

    parser.add_argument("-r",
                        metavar="region",
                        dest="region",
                        required=True)

    parser.add_argument("-k",
                        metavar="aws_key",
                        dest="aws_key",
                        required=True)

    parser.add_argument("-s",
                        metavar="aws_secret",
                        dest="aws_secret",
                        required=True)

    args = vars(parser.parse_args())

    on_demand = OnDemand(args["aws_key"], args["aws_secret"], args["region"])

    print(on_demand.get_current_cost(args["instance_type"]))


def on_demand_instances():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i",
                        metavar="instances",
                        dest="instances",
                        required=True)

    parser.add_argument("-r",
                        metavar="region",
                        dest="region",
                        required=True)

    parser.add_argument("-k",
                        metavar="aws_key",
                        dest="aws_key",
                        required=True)

    parser.add_argument("-s",
                        metavar="aws_secret",
                        dest="aws_secret",
                        required=True)

    args = vars(parser.parse_args())

    on_demand = OnDemand(args["aws_key"], args["aws_secret"], args["region"])

    print(on_demand.get_instances_cost(args["instances"].split(",")))


def spot_current():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i",
                        metavar="instance_type",
                        dest="instance_type",
                        required=True)

    parser.add_argument("-a",
                        metavar="availability_zone",
                        dest="availability_zone",
                        required=True)

    parser.add_argument("-k",
                        metavar="aws_key",
                        dest="aws_key",
                        required=True)

    parser.add_argument("-s",
                        metavar="aws_secret",
                        dest="aws_secret",
                        required=True)

    parser.add_argument("-r",
                        metavar="region",
                        dest="region",
                        required=True)

    args = vars(parser.parse_args())

    spot = Spot(args["aws_key"], args["aws_secret"], args["region"])

    print(spot.get_current_cost(args["availability_zone"], args["instance_type"]))
