from app import app, models
from models import *
from sqlalchemy.orm import sessionmaker

DBsession = sessionmaker(bind=engine)
session = DBsession()


def getProductCountCategory(cat_id, count):
    """Return count of product for specific category"""
    products = session.query(ProductItem).\
        filter(ProductItem.category_id == cat_id)\
        .order_by(ProductItem.price.desc()).limit(count)
    return products


def getProductCount(count):
    """Return specific number of products"""
    products = session.query(ProductItem).\
        order_by(ProductItem.created.desc()).limit(count)
    return products


def getProducts():
    """Returns the products as objects"""
    products = session.query(ProductItem).\
        order_by(ProductItem.product_name.asc()).all()
    return products


def getProductCategory(cat_id):
    """Returns all the products in the category"""
    products = session.query(ProductItem)\
        .filter(ProductItem.category_id == cat_id).all()
    return products


def getProductCategoryByName(name):
    """Returns all the products in the category by name"""
    products = session.query(ProductItem).join(Category)\
        .filter(Category.category_name == name).all()
    return products


def getProductByName(name):
    """Returns the product for the given product name"""
    product = session.query(ProductItem)\
        .filter(ProductItem.product_name == name).first()
    return product


def getProductByID(id):
    """Returns the product for the given product name"""
    product = session.query(ProductItem)\
        .filter(ProductItem.product_id == id).first()
    return product


def getCategory(cat_id):
    category = session.query(Category)\
        .filter(Category.category_id == cat_id).first()
    return category.category_name


def getCategoryByName(name):
    category = session.query(Category)\
        .filter(Category.category_name == name).all()
    return category


def getCategories():
    """Return all the categories as objects"""
    categories = session.query(Category).all()
    return categories


def countItemsByCategory(name):
    """Return a count of the number of items in the category"""
    return session.query(ProductItem).join(Category)\
        .filter(Category.category_name == name).count()


def getProductOwner(name):
    """Return the user_id for the product to determine owner"""
    product = session.query(ProductItem)\
        .filter(ProductItem.product_name == name).first()
    return product.user_id


def checkLogin(name, password):
    """Checks for valid user, if fails handles empty value or
    mismatched creds"""
    user = session.query(User).filter(User.username == name).first()
    if user is None:
        return False
    return models.User.check_password(user, password)


def userExists(name):
    return session.query(User).filter(User.username == name).first()  # noqa
