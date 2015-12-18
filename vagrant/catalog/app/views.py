from app import app, access
from flask import jsonify, render_template




@app.route('/')
@app.route('/home/')
def homepage():
    """Returns the last 5 products for each category"""
    """Should have two panels - LHS lists categories, and initial RHS view lists most recent products across all categories plus price and category
    category and/or product are clickable, to return either the category page or the product page.
    Users can edit, create, or delete only the items that they created
    """
    #productItems = access.getProducts()
    #for product in productItems:
    #    product.category = access.getCategory(product.category_id)
    productItems = []
    categories = access.getCategories()
    for category in categories:
        productItems += access.getProductCountCategory(category.category_id, 5)
    for product in productItems:
        product.category_name = access.getCategory(product.category_id)
    return render_template('producthome.html', categories=categories,
        products=productItems)


@app.route('/products/')
def products():
    """Returns the last 5 products for each category"""
    """Should have two panels - LHS lists categories, and initial RHS view lists most recent products across all categories plus price and category
    category and/or product are clickable, to return either the category page or the product page.
    Users can edit, create, or delete only the items that they created
    """
    #productItems = access.getProducts()
    #for product in productItems:
    #    product.category = access.getCategory(product.category_id)
    productItems = []
    categories = access.getCategories()
    for category in categories:
        productItems += access.getProductCountCategory(category.category_id, 5)
    return render_template('products.html', categories=categories,
        products=productItems)


@app.route('/products/json')
def json_products():
    print products
    return jsonify(Items=[i.serialize for i in products])


@app.route('/categories')
def categories():
    categories = access.getCategories()
    return render_template('categories.html', categories=categories,
        products=categories)

@app.route('/categories/<int:id>')
def showProductCategory(id):
    productItems = access.getProductCategory(id)
    for product in productItems:
        product.category = access.getCategory(product.category_id)
    return render_template('productbycategory.html', products=productItems)


@app.route('/products/item/<int:id>/')
def getProduct(id=1):
    return "This is where an item lives %s", id


@app.route('/products/edit/<int:id>/')
def editProduct(id=1):
    return "This is where an item lives %s", id
