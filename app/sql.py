from flask_sqlalchemy import BaseQuery

from app.extensions import db
from app.models import *


def general_create(model, data: dict, flush=False):
    model = model.__call__()
    for field, values in data:
        setattr(model, field, values)
    if flush:
        db.session.flush()
    return model


def general_edit(model, data: dict) -> None:
    for field, values in data:
        setattr(model, field, values)


def general_query(model, filters: dict) -> BaseQuery:
    return db.session.query(model).filter_by(**filters)


def query_one(model, filters: dict) -> BaseQuery:
    return general_query(model, filters).first()


def query_all(model, filters: dict, page: int = 1, count: int = 15) -> BaseQuery:
    return general_query(model, filters).offset((page-1) * count).limit(count).all()


def query_count(model, filters: dict) -> BaseQuery:
    return general_query(model, filters).count()