#!/usr/bin/env python

import boto3
import datetime
import pytz
from ec2costestimator.ec2.instance_information import InstanceInformation


class Spot:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

        self.client = boto3.client('ec2',
                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key,
                                   region_name=self.region)

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

    def get_instance_cost(self, instance_id):

        instance_information = InstanceInformation(self.aws_access_key_id,
                                                   self.aws_secret_access_key,
                                                   self.region)

        launch_time = instance_information.get_instance_launch_time(instance_id)
        hours = instance_information.get_instance_running_hours(instance_id)
        instance_type = instance_information.get_instance_type(instance_id)
        availability_zone = instance_information.get_availability_zone(instance_id)

        # Calculate the number of spot price history results based on the number of hours the
        # instance has been running
        max_results = hours * 100

        cost = self.describe_spot_price_history(availability_zone, instance_type,
                                                max_results=max_results)

        last_timestamp = pytz.utc.localize(datetime.datetime.utcnow())
        total_cost = float(0)

        for spot_price_history in cost["SpotPriceHistory"]:
            # Calculate how long the SpotPrice is valid (the time_delta)
            time_delta = last_timestamp - spot_price_history["Timestamp"]

            # Calculate the hourly cost of the instance for that time_delta based on the SpotPrice
            total_cost += float(float(spot_price_history["SpotPrice"]) *
                                (time_delta.seconds / 3600))

            last_timestamp = spot_price_history["Timestamp"]

            # Stop looping through the SpotPriceHistory once the SpotPriceHistory Timestamp is
            # older than the instance launch time
            if launch_time > spot_price_history["Timestamp"]:
                break

        return round(total_cost, 4)

    def get_instances_cost(self, instance_ids):

        total = 0

        if type(instance_ids) is list:
            for instance_id in instance_ids:
                total += float(self.get_instance_cost(instance_id))

        return round(total, 4)
