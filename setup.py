from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='twiliosms_wampservice',
      version=version,
      description="Twilio SMS service for Crossbar WAMP router",
      long_description="",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wamp, crossbar, autobahn',
      author='Petri Savolainen',
      author_email='petri.savolainen@koodaamo.fi',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
	        'autobahn.twisted.wamplet': [
	            'twiliosms = twiliosms_wampservice:app'
	        ],
      },
      test_suite = "tests",
)
