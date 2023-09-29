"""
Build and installation script for the `logparser` package.

This script facilitates the packaging and distribution of the `logparser` project. By defining the project's
metadata and configuration, the `setuptools` library can use this script to create distributable packages,
install the project, declare its dependencies, and even make it executable from the command line.

Features:
- Package Information: Defines the name, version, and other core details of the package.
- Discovery: Utilizes `find_packages()` to automatically discover and include all packages in the distribution.
- Dependencies: Declares any third-party library dependencies. Currently, this project doesn't rely on any non-standard libraries.
- Entry Points: Configures the console script that lets users run the log parser directly from the command line using `run-logparser`.
- Metadata: Provides additional metadata like the author's name, email, project's description, license details, keywords, and project URL.

Usage:
    To install the package in the local environment:
    $ python setup.py install

    To create a source distribution:
    $ python setup.py sdist

Note:
    If in the future the project starts relying on third-party libraries, they should be added to the `install_requires` list.

Author:
    Orestis Nikolas (OrestisDrow@gmail.com)
"""
from setuptools import setup, find_packages

setup(
    name="logparser",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Zero non-standard python library dependencies
    ],
    entry_points={
    'console_scripts': [
        'run-logparser=logparser.run_parser:main', # Give the option to do run-logparser from bash
        ],
    },

    author="Orestis Nikolas",
    author_email="OrestisDrow@gmail.com",
    description="A specialized log parser for extracting specific metrics.",
    license="MIT",
    keywords="log parser",
    url="https://github.com/OrestisDrow/AAParserProject",
)