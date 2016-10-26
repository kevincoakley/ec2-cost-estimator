# ec2-cost-estimator

[![Build Status](https://travis-ci.org/kevincoakley/ec2-cost-estimator.svg?branch=master)](https://travis-ci.org/kevincoakley/ec2-cost-estimator)

## Installation

Install via pip:

    $ pip install git+https://github.com/kevincoakley/ec2-cost-estimator.git

Install from source:

    $ git clone https://github.com/kevincoakley/ec2-cost-estimator.git
    $ cd ec2-cost-estimator
    $ python setup.py install

## Removal

Remove via pip:

    $ pip uninstall ec2-cost-estimator -y


## Commands

Get current EC2 hourly cost (on demand and spot):

    $ ec2_cost_current -k aws_key -s aws_secret -r region -i instance_type [-a availability_zone] [--spot]

Get estimated cost for running instances (on demand and spot), use a comma separated list of instance ids for multiple instances:

    $ ec2_cost_instances -k aws_key -s aws_secret -r region -i instance_id1,instance_id2
