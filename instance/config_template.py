# coding: utf-8
"""
    :date: 2023-11-12
    :author: linshukai
    :description: About Flask Template Config PYFile(config.py)
"""

import os

DEBUG = True
SECRET_KEY = ""
DATABASE = os.path.join(os.getcwd(), "instance", "flasker.sqlite")
SQLALCHEMY_DATABASE_URI = ''
