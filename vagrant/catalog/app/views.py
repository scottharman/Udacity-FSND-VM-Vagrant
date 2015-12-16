from app import app, access
from flask import jsonify, render_template




@app.route('/')
@app.route('/products/')
def products():
    """Returns the last 5 products for each category"""
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
