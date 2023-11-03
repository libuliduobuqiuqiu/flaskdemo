# coding: utf-8

"""
    :date: 2023-11-3
    :author: linshukai
    :description: ABout Auth Routes
"""

from flask import (
    Blueprint, redirect, render_template, request, url_for, flash, session, abort, g
)
from .auth import verify_user, create_user

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("auth.index"))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # 登陆视图处理函数
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        err = verify_user(username, password)

        if err is None:
            return redirect(url_for("auth.index"))

        flash(err)

    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        err = None

        if not username:
            err = 'Username is required.'
        elif not password:
            err = 'Password is required.'

        if err is None:
            err = create_user(username, password)

        flash(err)

    return render_template('auth/register.html')


@bp.route("/index", methods=["GET"])
def index():
    if g.get("user") is None:
        abort(400)

    username = g.user.name
    return f"<p>Hello, {username}, Welcome to my Website."
