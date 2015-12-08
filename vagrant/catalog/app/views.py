from app import app, access
from flask import jsonify, render_template




@app.route('/')
@app.route('/products/')
def products():
    productItems = access.showProducts()
    for product in productItems:
        product.category = access.showCategory(product.category_id)
    return render_template('products.html', products=productItems)


@app.route('/products/json')
def json_products():
    print products
    return jsonify(Items=[i.serialize for i in products])


@app.route('/categories')
def categories():
    return render_template('categories.html', categories=categories)

@app.route('/categories/<int:id>')
def showProductCategory(id):
    productItems = access.showProductCategory(id)
    return render_template('productbycategory.html', products=productItems)


@app.route('/products/item/<int:id>/')
def getProduct(id=1):
    return "This is where an item lives %s", id


@app.route('/products/edit/<int:id>/')
def editProduct(id=1):
    return "This is where an item lives %s", id
