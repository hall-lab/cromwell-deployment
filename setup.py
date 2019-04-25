# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('cromployer/version.py') as f:
    exec(f.read())

setup(
    name='cromployer',
    version=__version__,
    description='Helper to setup a cromwell server and database.',
    long_description=readme,
    author='Indraniel Das',
    author_email='idas@wustl.edu',
    license=license,
    url='https://github.com/hall-lab/cromwell-deployment',
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        cromulent=cromployer.cli:cli
    ''',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
)
