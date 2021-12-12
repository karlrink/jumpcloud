
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name = "jumpcloud",
    packages = ["jumpcloud","jumpcloud.reports"],
    entry_points = {
        "console_scripts": ['jumpcloud = jumpcloud.jumpcloud:main']
        },
    version = '2.0.0',
    description = "jumpcloud command for jumpcloud.com",
    long_description = "Python command line tool for administration of jumpcloud.com api.",
    author = "Karl Rink",
    author_email = "karl@rink.us",
    url = "https://gitlab.com/krink/jumpcloud",
    install_requires = [ 'requests', ]
    )

