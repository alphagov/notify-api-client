"""
Common utils for Digital Marketplace apps.
"""
import re
import ast
import pip.download
from pip.req import parse_requirements
from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('notify_client/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = list(parse_requirements('requirements.txt',
                                       session=pip.download.PipSession()))

install_requires = [str(r.req) for r in requirements]

setup(
    name='notify-api-client',
    version=version,
    url='https://github.com/alphagov/notify-api-client',
    license='MIT',
    author='GDS Developers',
    description='API Client for notify API.',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires
)
