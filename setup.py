#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="csvtool",
    version="1.3.0",
    author="Sourena MAROOFI",
    author_email="maroofi@example.com",
    description="A command-line tool for working with CSV files with enhanced pipe support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maroofi/csvtool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "csvtool=csvtool.__main__:main",
        ],
    },
    keywords="csv, command-line, data-processing, pipe, stdin",
    project_urls={
        "Bug Reports": "https://github.com/maroofi/csvtool/issues",
        "Source": "https://github.com/maroofi/csvtool",
    },
)
