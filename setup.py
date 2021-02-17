#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='vdnetcdf',
    version='0.2.0.dev',
    description='A VisiData plugin for reading NetCDF files.',
    maintainer='Tim Tröndle',
    maintainer_email='tim.troendle@usys.ethz.ch',
    url='https://www.github.com/timtroendle/vdnetcdf',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=['visidata', 'xarray', 'netcdf4', 'numpy>=1.16.5'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering'
    ]
)
