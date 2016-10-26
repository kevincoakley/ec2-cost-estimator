#!/usr/bin/env python

import argparse
from ec2costestimator.cost.get_cost import GetCost


def current():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i",
                        metavar="instance_type",
                        dest="instance_type",
                        required=True)

    parser.add_argument("-a",
                        metavar="availability_zone",
                        dest="availability_zone",
                        default="us-east-1a",
                        required=False)

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

    parser.add_argument("--spot",
                        dest="spot",
                        action='store_true')

    args = vars(parser.parse_args())

    cost = GetCost(args["aws_key"], args["aws_secret"], args["region"])

    print(cost.get_current_cost(args["instance_type"],
                                availability_zone=args["availability_zone"],
                                spot=args["spot"]))


def instances():

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

    cost = GetCost(args["aws_key"], args["aws_secret"], args["region"])

    print(cost.get_instances_cost(args["instances"].split(",")))
