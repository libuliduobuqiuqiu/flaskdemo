# coding: utf-8
"""
    :date: 2023-11-3
    :author: linshukai
    :description: About Blog Page
"""
from flasker.auth import login_required
from flask import Blueprint, g


bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/person-info", methods=["GET"])
@login_required
def person_blog_info():
    return f"<h1>This is {g.user.name} personal page.</h1>"