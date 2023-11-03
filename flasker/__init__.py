# coding: utf-8

"""
    :date: 20203-10-31
    :author:L linshukai
"""

import os
from flask import Flask, session, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__, instance_relative_config=True)
db = SQLAlchemy()


def create_app(test_config=None):
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

    # 初始化SQL配置
    db.init_app(app)

    # 注册路由
    from .auth import bp as auth
    app.register_blueprint(auth)

    from .blog import bp as blog
    app.register_blueprint(blog)
    return app


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        sql_str = text("Select * from user where id = :id")
        user = db.session.execute(sql_str, params={"id": user_id}).first()
        if user is None:
            session.clear()
            return redirect(url_for("auth.index"))
        g.user = user


@app.errorhandler(400)
def handle_exception(d):
    return f"<h1 style='color: red;'> 用户未登录，无权访问....</h1>\n<a href='{url_for('auth.login')}'>请重新登录</a>"
