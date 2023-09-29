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