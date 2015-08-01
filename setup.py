import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

exec(open('version.py').read()) # loads __version__

setup(name='runm',
      version=__version__,
      author='$AUTHOR',
    description='',
    long_description=open('README.md').read(),
    license='MIT',
    keywords="",
    packages= find_packages(exclude='docs'))
