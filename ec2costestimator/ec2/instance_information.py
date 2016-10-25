#!/usr/bin/env python

import boto3
import datetime
import math


class InstanceInformation:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region):

        self.ec2 = boto3.resource('ec2',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region)

    def get_instance_launch_time(self, instance_id):

        instance = self.ec2.Instance(instance_id)

        return instance.launch_time

    def get_instance_running_hours(self, instance_id):

        instance = self.ec2.Instance(instance_id)

        launch_time = datetime.datetime.strptime(str(instance.launch_time),
                                                 '%Y-%m-%d %H:%M:%S+00:00')
        running_seconds = int((datetime.datetime.utcnow() - launch_time).total_seconds())

        # Convert the running seconds into hours and round up
        return math.ceil(running_seconds / 60 / 60)

    def get_instance_type(self, instance_id):

        instance = self.ec2.Instance(instance_id)

        return instance.instance_type

    def get_availability_zone(self, instance_id):

        instance = self.ec2.Instance(instance_id)

        return instance.placement["AvailabilityZone"]

    def get_instance_lifecycle(self, instance_id):

        instance = self.ec2.Instance(instance_id)

        return instance.instance_lifecycle
