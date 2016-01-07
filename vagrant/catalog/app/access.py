from app import app, models
from models import *
from sqlalchemy.orm import sessionmaker

DBsession = sessionmaker(bind=engine)
session = DBsession()


def getProductCountCategory(cat_id, count):
    products = session.query(ProductItem).filter(ProductItem.category_id == cat_id).order_by(ProductItem.price.desc()).limit(count)  # noqa
    return products


def getProducts():
    """Returns the products as objects"""
    products = session.query(ProductItem).\
    order_by(ProductItem.product_name.asc()).all()
    return products


def getProductCategory(cat_id):
    """Returns all the products in the category"""
    products = session.query(ProductItem).filter(ProductItem.category_id == cat_id).all()  # noqa
    return products


def getProductCategoryByName(name):
    """Returns all the products in the category by name"""
    products = session.query(ProductItem).join(Category).filter(Category.category_name == name).all()  # noqa
    return products


def getProductByName(name):
    """Returns the product for the given product name"""
    product = session.query(ProductItem).filter(ProductItem.product_name == name).first()  # noqa
    return product


def getProductByID(id):
    """Returns the product for the given product name"""
    product = session.query(ProductItem).filter(ProductItem.product_id == id).first()  # noqa
    return product


def getCategory(cat_id):
    category = session.query(Category).filter(Category.category_id == cat_id).first()  # NOQA
    return category.category_name


def getCategories():
    categories = session.query(Category).all()
    return categories
