import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('version.py').read()) # loads __version__

setup(name='extern',
      version=__version__,
      author='Ben Woodcroft',
      author_email='donttrustben@gmail.com',
    description='',
    long_description=open('README.md').read(),
    license='MIT',
    keywords="",
    packages= find_packages(exclude='docs'))
