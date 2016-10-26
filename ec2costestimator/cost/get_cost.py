#!/usr/bin/env python

from ec2costestimator.cost.on_demand import OnDemand
from ec2costestimator.cost.spot import Spot
from ec2costestimator.ec2.instance_information import InstanceInformation


class GetCost:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    def get_current_cost(self, instance_size, spot=False, availability_zone="us-east-1a"):
        if spot:
            spot = Spot(self.aws_access_key_id, self.aws_secret_access_key, self.region)
            return spot.get_current_cost(availability_zone, instance_size)
        else:
            on_demand = OnDemand(self.aws_access_key_id, self.aws_secret_access_key, self.region)
            return on_demand.get_current_cost(instance_size)

    def get_instances_cost(self, instance_ids):
        total = 0

        if type(instance_ids) is list:
            for instance_id in instance_ids:
                instance_information = InstanceInformation(self.aws_access_key_id,
                                                           self.aws_secret_access_key,
                                                           self.region)

                lifecycle = instance_information.get_instance_lifecycle(instance_id)

                if lifecycle is "spot":
                    spot = Spot(self.aws_access_key_id, self.aws_secret_access_key, self.region)
                    total += float(spot.get_instance_cost(instance_id))
                else:
                    on_demand = OnDemand(self.aws_access_key_id, self.aws_secret_access_key,
                                         self.region)
                    total += float(on_demand.get_instance_cost(instance_id))

        return round(total, 4)
