from setuptools import setup, find_packages
import sys, os

version = '0.4'

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
         "treq",
         "twilio",
         "klein"
      ],
      entry_points={
	        'autobahn.twisted.wamplet': [
	            'twilio_sms_sender = twiliosms_wampservice:sender',
	            'twilio_sms_receiver = twiliosms_wampservice:receiver'
	        ],
      },
      tests_require = ["mock",],
      test_suite = "tests",
)
