# coding: utf-8
"""
    :date: 2023-10-31
    :author: linshukai
"""
import pymysql
import sqlalchemy.exc
from flask import (
    Blueprint, request, render_template, url_for, redirect, flash, session, g, abort, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flasker.model import User
from flasker import db
import uuid

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@bp.errorhandler(400)
def handle_exception(d):
    return "Login Failed...."


@bp.route("/index", methods=["GET"])
def index():
    if g.get("user") is None:
        abort(400)

    username = g.user.name
    return f"<p>Hello, {username}, Welcome to my Website."


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 注册视图处理函数
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User(id=str(uuid.uuid1()), name=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()

            except sqlalchemy.exc.IntegrityError:
                error = "Name已存在，请重新注册"
                db.session.rollback()

            except Exception as e:
                error = e
                db.session.rollback()

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
        error = None
        user = User.query.filter(User.name == username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print(user_id, current_app.config['SECRET_KEY'], current_app.config['DEBUG'])

    if user_id is None:
        g.user = None
    else:
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            session.clear()
            return redirect(url_for("auth.index"))

        g.user = user


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
