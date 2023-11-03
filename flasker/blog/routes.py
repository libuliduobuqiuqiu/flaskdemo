# coding: utf-8
"""
    :date: 2023-11-3
    :author: linshukai
    :description: About Blog Page
"""
from flasker.auth import login_required
from flask import Blueprint, g, url_for


bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.errorhandler(400)
def login_failed(d):
    return f"<h1 style='color: red;'> 用户未登录，无权访问博客个人页面。</h1>\n<a href='{url_for('auth.login')}'>请重新登录</a>"

@bp.route("/person-info", methods=["GET"])
@login_required
def person_blog_info():
    return f"<h1>This is {g.user.name} personal page.</h1>"