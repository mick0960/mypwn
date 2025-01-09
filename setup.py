# setup.py

from setuptools import setup, find_packages

setup(
    name='mypwn',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pwntools',
    ],
    entry_points={},
)