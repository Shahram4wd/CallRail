#!/usr/bin/env python3

"""
Setup script for CallRail API Python client.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="callrail-api-client",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python client for the CallRail API v3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/callrail-api-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="callrail api client call tracking phone",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/callrail-api-client/issues",
        "Source": "https://github.com/yourusername/callrail-api-client",
        "Documentation": "https://apidocs.callrail.com/",
    },
)
