# coding: utf-8
from flasker import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, unique=True)
    password = db.Column(db.String(255))
    address = db.Column(db.String(255))
