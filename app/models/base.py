from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.query import Query as BaseQuery
from sqlalchemy import inspect, Column, Integer, SmallInteger, orm
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield  # The preceding execution will return to continue execution.
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    # Abstract model, does not create entity table, otherwise need to create the primary key.
    __abstract__ = True
    
    # Add a creation time property to record when the instance object was created.
    create_time = Column('create_time', Integer)
    # default=1 means not deleted, and =0 means deleted.
    status = Column(SmallInteger, default=1)

    def __init__(self):
        # Gets the system timestamp as the time the object was created.
        self.create_time = int(datetime.now().timestamp())

    # Setting objects to return the value of a dictionary is also common to all instances
    # and is therefore included in the Base class.
    def __getitem__(self, item):
        return getattr(self, item)

    # Methods for setting column attributes (common to all instances).
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # Defines methods to delete model objects.
    def delete(self):
        self.status = 0
