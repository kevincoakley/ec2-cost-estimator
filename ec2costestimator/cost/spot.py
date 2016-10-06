#!/usr/bin/env python

import boto3


class Spot:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region):

        self.client = boto3.client('ec2',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name=region)

    def get_current_cost(self, availability_zone, instance_type, product_descriptions="Linux/UNIX"):
        cost = self.describe_spot_price_history(availability_zone,
                                                instance_type,
                                                product_descriptions=product_descriptions,
                                                max_results=1)

        return cost["SpotPriceHistory"][0]["SpotPrice"]

    def describe_spot_price_history(self, availability_zone, instance_type,
                                    product_descriptions="Linux/UNIX", max_results=1):
        return self.client.describe_spot_price_history(InstanceTypes=[instance_type],
                                                       AvailabilityZone=availability_zone,
                                                       ProductDescriptions=[product_descriptions],
                                                       MaxResults=max_results)
