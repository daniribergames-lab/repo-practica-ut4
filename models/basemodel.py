from peewee import *
from database import db


class BaseModel(Model):
    class Meta:
        database = db