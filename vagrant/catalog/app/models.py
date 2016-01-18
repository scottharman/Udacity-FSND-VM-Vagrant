import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

from app import app

Base = declarative_base()


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return 'Not recorded'
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Category(Base):
    """The category of objects avaiable"""
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(50), nullable=False)
    category_description = Column(String(120), nullable=True)

    def getID(self):
        return unicode(self.category_id)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category_name': self.category_name,
            'category_id': self.category_id,
            'category_description': self.category_description,
            'Items': self.serializeItems
        }

    @property
    def serializeItems(self):
        """Serialize items from other class"""
        return [item.serialize for item in self.Items]


class ProductItem(Base):
    """Product items"""
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(80), nullable=False)
    product_description = Column(String(120))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    price = Column(Numeric(12, 2))
    user_id = Column(String(80), nullable=False)
    created = Column(DateTime(timezone=True))
    updated = Column(DateTime(timezone=True))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'product_name': self.product_name,
            'product_description': self.product_description,
            'product_id': self.product_id,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'price': self.price,
            'user_id': self.user_id,
            'created': dump_datetime(self.created),
            'updated': dump_datetime(self.updated)
        }


class User(Base):
    """User class - basic authentication"""
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(80))
    password = Column(String(120))
    registered = Column(DateTime)
    # def __init__(self, username, password, email, can_edit, edit_note, can_create, is_admin):  # noqa
    #     self.username = username
    #     self.set_password(password)
    #     self.email = email
    #     self.registered_on = datetime.utcnow()
    #     self.can_edit = can_edit
    #     self.edit_note = edit_note
    #     self.can_create = can_create
    #     self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


engine = create_engine("postgresql+psycopg2://vagrant@/catalog")
Base.metadata.create_all(engine)
