#!/usr/bin/env python

import re
import requests
import yaml

INSTANCES_ON_DEMAND_LINUX_URL = "http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js"


class OnDemand:

    def __init__(self):
        pass

    def get_current_cost(self, region, instance_size):

        js = self.get_js_file()

        # strip initial comment (with newline)
        js = re.sub(re.compile(r'/\*.*\*/\n', re.DOTALL), '', js)
        # strip from front of request
        js = re.sub(r'^callback\(', '', js)
        # strip from end of request
        js = re.sub(r'\);*$', '', js)

        js = js.replace(":", ": ")
        js = yaml.load(js)

        for js_region in js["config"]["regions"]:

            # Find the matching region
            if js_region["region"] == region:

                # Loop through all of the instances types
                for instance_types in js_region["instanceTypes"]:

                    # Loop though all of the instance sizes
                    for sizes in instance_types["sizes"]:

                        # If the size matches the requested size then return the price
                        if sizes["size"] == instance_size:

                            return sizes["valueColumns"][0]["prices"]["USD"]

        return None

    @staticmethod
    def get_js_file():
        r = requests.get(INSTANCES_ON_DEMAND_LINUX_URL)
        return r.text
