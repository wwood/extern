import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('version.py').read()) # loads __version__

import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite

setup(name='extern',
      version=__version__,
      author='Ben Woodcroft',
      author_email='donttrustben@gmail.com',
      description='',
      long_description=open('README.md').read(),
      license='MIT',
      keywords="",
      test_suite='setup.my_test_suite',
      packages= find_packages(exclude='docs'))
