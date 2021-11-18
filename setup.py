# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(path.join(here, 'CJ', 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

with open(path.join(here, 'requirements.txt')) as f:
    requirements = []
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name='cjds-api',
    version=version,
    description='CJDropshipping api client.',
    long_description=long_description,
    url='https://github.com/FG-IT/python-cjdropshipping-api',
    author='TPT',
    author_email='neal.wkacc@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    keywords='cjdropshipping api',
    packages=find_packages(exclude=('tests')),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
        ]
    }
)