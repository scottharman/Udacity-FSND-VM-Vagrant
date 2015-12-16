from app import app, models
from models import *
from sqlalchemy.orm import sessionmaker

DBsession = sessionmaker(bind=engine)
session = DBsession()

def getProductCountCategory(cat_id, count):
    products = session.query(ProductItem).filter(ProductItem.category_id == cat_id).limit(count)  # noqa
    return products

def getProducts():
    """Returns the products as objects"""
    products = session.query(ProductItem).all()
    print products
    return products


def getProductCategory(cat_id):
    """Returns all the products in the category"""
    print cat_id
    products = session.query(ProductItem).filter(ProductItem.category_id == cat_id).all()  # noqa
    return products


def getProduct(id):
    """Returns the product for the given ID"""
    return


def addProduct():
    """Add a product to the database"""
    return


def deleteProduct(id):
    """Delete a product from the database"""
    return


def updateProduct(id):
    """Change a product description, price, or title in the database"""
    return


def getCategory(cat_id):
    print id

    category = session.query(Category).filter(Category.category_id==cat_id).first()
    return category.category_name

def getCategories():
    categories = session.query(Category).all()
    return categories

def addUser():
    """Add a new user"""
    return
