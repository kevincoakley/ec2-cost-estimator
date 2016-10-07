#!/usr/bin/env python

try:
    from setuptools import setup
    extra = dict(install_requires=[
    ],
        include_package_data=True,
        test_suite="tests.suite.load_tests",
    )
except ImportError:
    from distutils.core import setup
    extra = {}


def readme():
    with open("README.md") as f:
        return f.read()


setup(name="ec2-cost-estimator",
      version="0.0.1",
      description="Estimate EC2 Costs for on-demand and spot instances",
      long_description=readme(),
      author="Kevin Coakley",
      author_email="kcoakley@sdsc.edu",
      scripts=[
          "bin/on_demand_current",
          "bin/spot_current",
      ],
      url="",
      packages=[
          "ec2costestimator",
          "ec2costestimator/cost",
      ],
      platforms="Posix; MacOS X",
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
      ],
      **extra
      )
