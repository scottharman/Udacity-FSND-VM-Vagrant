from app import app, access
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Udacity Catalog Project"

@app.route('/')
@app.route('/home')
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


@app.route('/products')
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
    productItems = access.getProducts()
    for product in productItems:
        product.category_name = access.getCategory(product.category_id)
    return jsonify(Items=[i.serialize for i in productItems])


@app.route('/categories/')
@app.route('/categories/<int:id>')
def categories(id=1):
    categories = access.getCategories()
    productItems = access.getProductCategory(id)
    for product in productItems:
        product.category = access.getCategory(product.category_id)
    return render_template('productbycategory.html', categories=categories, products=productItems)


@app.route('/products/item/<int:id>/')
def getProduct(id=1):
    product = access.getProduct(id)
    product.category = access.getCategory(product.category_id)
    return render_template('product.html', product=product)


@app.route('/products/edit/<int:id>/')
def editProduct(id=1):
    return "This is where an item lives %s", id


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
    	return response
