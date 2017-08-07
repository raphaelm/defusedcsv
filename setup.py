from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
try:
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''

try:
    from defusedcsv import version
except ImportError:
    version = '?'

setup(
    name='defusedcsv',
    version=version,
    description='Drop-in replacement for Python\'s CSV library that tries to mitigate CSV injection attacks',
    long_description=long_description,
    url='https://github.com/raphaelm/defusedcsv',
    author='Raphael Michel',
    author_email='mail@raphaelmichel.de',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='csv injection defuse save',
    install_requires=[
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
)
