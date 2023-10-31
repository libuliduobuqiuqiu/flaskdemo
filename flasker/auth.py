# coding: utf-8
"""
    :date: 2023-10-31
    :author: linshukai
"""

from flask import (
    Blueprint, request, render_template, url_for, redirect, flash, session, g, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from flasker.db import get_db
from functools import wraps

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.errorhandler(400)
def handle_exception(d):
    return "Login Failed...."


@bp.route("/index", methods=["GET"])
def index():
    if g.get("user") is None:
        abort(400)

    username = g.user["username"]
    return f"<p>Hello, {username}, Welcome to my Website."


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 注册视图处理函数
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # 登陆视图处理函数
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute("SELECT * FROM user where id = ?", (user_id,)).fetchone()
        print(g.user, g.get("user"))


@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("auth.index"))


# 鉴权装饰器校验登陆是否正常
def login_required(view):
    @wraps(view)
    def wrap_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrap_view
