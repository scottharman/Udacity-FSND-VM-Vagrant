import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from app import app

Base = declarative_base()


class Category(Base):
    """The category of objects avaiable"""
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def getID(self):
        return unicode(self.category_id)


class ProductItem(Base):
    """Product items"""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(120))
    category_id = Column(Integer, ForeignKey('category.category_id'))

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
