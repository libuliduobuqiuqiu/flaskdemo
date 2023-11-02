# coding: utf-8

"""
    :date: 20203-10-31
    :author:L linshukai
"""

import os
from flask import g
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # 判断传入的配置是否为空，重新载入配置
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.from_mapping(test_config)

    # 用以创建实例文件夹
    try:
        os.makedirs(app.instance_path)
    except Exception as e:
        pass

    @app.route("/hello", methods=["GET"])
    def hello():
        return "Hello,World"

    from . import auth
    app.register_blueprint(auth.bp)

    # 初始化SQL配置
    db.init_app(app)

    return app
