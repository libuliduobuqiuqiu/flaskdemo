# coding: utf-8
"""
    :date: 2023-11-8
    :author: linshukai
    :description: About Restful API Demo
"""
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import Resource, reqparse, Api
from flask import Blueprint
from faker import Faker
from flasker.model import User
from flasker import db, app
import uuid

bp = Blueprint("rest", __name__, url_prefix="/rest")
rest_api = Api(bp)


class PersonResource(Resource):
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument("name", type=str, location="args", required=True)

        args = get_parser.parse_args()
        fake = Faker()
        return {"code": 200, "data": {"address": fake.address(), "name": args.name}, "msg": "success"}

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument("name", type=str, location="args", required=True)
        post_parser.add_argument("address", type=str, location="json", required=True)
        post_parser.add_argument("age", type=int, location="json", required=True)

        args = post_parser.parse_args()
        user = User(id=str(uuid.uuid1()), name=args.name, password=generate_password_hash("admin"),
                    address=args.address)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"数据库错误：{e}")
            raise e

        return {"code": 200, "msg": "success"}


rest_api.add_resource(PersonResource, "/person")
