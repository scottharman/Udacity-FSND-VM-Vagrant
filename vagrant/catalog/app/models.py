import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from app import app

Base = declarative_base()


class Category(Base):
    """The category of objects avaiable"""
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(50), nullable=False)
    category_description = Column(String(120), nullable=True)

    def getID(self):
        return unicode(self.category_id)


class ProductItem(Base):
    """Product items"""
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(80), nullable=False)
    product_description = Column(String(120))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    price = Column(Numeric(12, 2))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }

engine = create_engine("postgresql+psycopg2://vagrant@/catalog")
Base.metadata.create_all(engine)
