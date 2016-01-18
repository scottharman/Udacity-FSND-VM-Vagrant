from app import app, access, models
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, make_response
from werkzeug.contrib.atom import AtomFeed
from werkzeug.security import generate_password_hash
from werkzeug import secure_filename
from flask.ext.seasurf import SeaSurf

from flask import session as login_session
import random
import string
import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from urlparse import urljoin
from datetime import datetime
from functools import wraps
csrf = SeaSurf(app)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Udacity Catalog Project"
UPLOAD_FOLDER = '/vagrant/catalog/app/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def login_required(f):
    """Test to see if user is logged in and has a valid session"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in login_session:
            return redirect(url_for('showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def login_owner(f):
    """Test to see if the current user is the owner of the object"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'name' in kwargs:
            name = kwargs.get('name')
        else:
            return redirect(url_for('showLogin', next=request.url))
        if 'email' not in login_session:
            flash('User not logged in')
            return redirect(url_for('showLogin', next=request.url))
        elif login_session['email'] != access.getProductOwner(name):
            flash('%s is not owner of %s' % (login_session['email'],
                  name))
            return redirect(url_for('showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Test to see if the filetype is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/products')
def products():
    """Returns the last 5 products for each category"""
    """Should have two panels - LHS lists categories, and initial RHS view lists
    most recent products across all categories plus price and category
    category and/or product are clickable, to return either the category page or
    the product page.
    Users can edit, create, or delete only the items that they created
    """
    productItems = []
    categories = access.getCategories()
    for category in categories:
        category.count = access.countItemsByCategory(category.category_name)
        productItems += access.getProductCountCategory(category.category_id, 5)
    for product in productItems:
        product.category_name = access.getCategory(product.category_id)
        if product.product_image:
            product.product_url = 'uploads/' + product.product_image
    return render_template('products.html', categories=categories,
                           products=productItems)


# Switch product global view to category, then add counters per category
@app.route('/catalog')
@app.route('/catalog/')
@app.route('/catalog/<path:name>/items')
def categories(name=''):
    """Returns the last 5 products for each category"""
    """Should have two panels - LHS lists categories, and initial RHS view lists
     most recent products across all categories plus price and category
    category and/or product are clickable, to return either the category page or
     the product page.
    Users can edit, create, or delete only the items that they created
    """
    productItems = []
    categories = access.getCategories()
    if name != '':
        categories = access.getCategoryByName(name)
        productItems = access.getProductCategoryByName(name)
    else:
        for category in categories:
            productItems += access.getProductCategory(category.category_id)
    for product in productItems:
        product.category = access.getCategory(product.category_id)
        if product.product_image:
            product.product_url = 'uploads/' + product.product_image
    for category in categories:
        category.count = access.countItemsByCategory(category.category_name)
    return render_template('products.html', categories=categories,
                           products=productItems)


@app.route('/catalog.json')
def json_products():
    categories = access.getCategories()
    for category in categories:
        category.Items = access.getProductCategory(category.category_id)
        for product in category.Items:
            product.category_name = access.getCategory(product.category_id)
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/catalog/<path:name>/items/json')
def category_json(name):
    productItems = []
    categories = access.getCategories()
    categories = access.getCategoryByName(name)
    for category in categories:
        category.Items = access.getProductCategory(category.category_id)
        for product in category.Items:
            product.category_name = access.getCategory(product.category_id)
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/catalog/<path:name>/')
def getProduct(name):
    product = access.getProductByName(name)
    if product.product_image:
        product.product_url = 'uploads/' + product.product_image
    product.category = access.getCategory(product.category_id)
    return render_template('product.html', product=product)


@app.route('/catalog/<path:name>/edit/', methods=['GET', 'POST'])
@login_owner
def editProduct(name):
    categories = access.getCategories()
    product = access.getProductByName(name)
    if product.product_image:
        product.product_url = '/uploads/', product.product_image
    product.category = access.getCategory(product.category_id)
    if request.method == 'POST':
        product_image = request.files['product_image']
        if product_image and allowed_file(product_image.filename):
            filename = secure_filename(product_image.filename)
            product_image.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                            filename))
            product.product_image = filename
        product.product_name = request.form['product_name']
        product.price = request.form['price']
        product.product_description = request.form['product_description']
        product.category_id = request.form['category_id']
        product.updated = datetime.now()
        flash('Product Edited %s' % product.product_name)
        access.session.commit()
        return redirect(request.referrer)
    else:
        return render_template('editProduct.html', product=product,
                               categories=categories)


@app.route('/catalog/<path:name>/delete/', methods=['GET', 'POST'])
@login_owner
def deleteProduct(name):
    """Delete defined product if you are the user who owns it"""
    product = access.getProductByName(name)
    product.category = access.getCategory(product.category_id)
    if login_session['email'] == product.user_id:
        if request.method == 'POST':
            access.session.delete(product)
            access.session.commit()
            flash('Product Deleted %s' % product.product_name)
            return redirect(url_for('categories'))
        else:
            return render_template('deleteProduct.html', product=product)
    else:
        flash('No permission to delete %s' % login_session['username'])
        return redirect(url_for('products'))


@app.route('/catalog/<path:name>/json')
def product_json(name):
    """Display JSON record for product"""
    product = access.getProductByName(name)
    product.category_name = access.getCategory(product.category_id)
    return jsonify(Items=[product.serialize])


@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def addProduct():
    """Add product to database"""
    categories = access.getCategories()
    if request.method == 'POST':
        product_image = request.files['product_image']
        filename = ''
        if product_image and allowed_file(product_image.filename):
            filename = secure_filename(product_image.filename)
            product_image.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                            filename))
        product = models.ProductItem(
            product_name=request.form['product_name'],
            price=request.form['price'],
            product_image=filename,
            product_description=request.form['product_description'],
            category_id=request.form['category_id'],
            user_id=login_session['email'],
            created=datetime.now(),
            updated=datetime.now())
        flash('Product Added %s' % product.product_name)
        access.session.add(product)
        access.session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template('addProduct.html', categories=categories)


@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def addCategory():
    """Add ability to create new category currently not implemented """
    return "add category here"


def make_external(url):
    """Tiny function to make the url sensible for atom feed"""
    return urljoin(request.url_root, url)


@app.route('/catalog.atom')
def recent_feed():
    feed = AtomFeed('Recent Products',
                    feed_url=request.url, url=request.url_root)
    categories = access.getCategories()
    productItems = access.getProductCount(15)
    for product in productItems:
        product.category_name = access.getCategory(product.category_id)
        feed.add(product.product_name, unicode(product.product_description),
                 content_type='html',
                 author=product.user_id,
                 url=make_external(url_for('getProduct', name=product.product_name)),  # noqa
                 updated=product.updated or product.created,
                 published=product.created)
    return feed.get_response()


@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    if request.method == 'POST':
        if access.checkLogin(request.form['username'],
                             request.form['password']):
            flash(u'Successfully logged in as %s' % request.form['username'])
            login_session['email'] = request.form['username']
            login_session['logged_in'] = 'true'
            login_session['local'] = 'true'
            return redirect(url_for('products'))
        else:
            flash(u'Login as %s failed - please check and try again' % request.form['username'])  # noqa
            return render_template('login.html', STATE=state)
    return render_template('login.html', STATE=state)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if access.userExists(request.form['username']):
            flash(u'User %s already exists!  Please login' % request.form['username'])  # noqa
            return redirect(url_for('showLogin'))
        user = models.User(username=request.form['username'],
         password=generate_password_hash(request.form['password']))  # noqa
        access.session.add(user)
        access.session.commit()
        login_session['email'] = request.form['username']
        login_session['logged_in'] = 'true'
        login_session['local'] = 'true'
        flash('User %s successfully registered' % request.form['username'])
        return redirect(url_for('products'))
    else:
        return render_template('register.html')


@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Login to google, and authenticate - added csrf exemption"""
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
        login_session['logged_in'] = 'true'
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
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
    login_session['logged_in'] = 'true'
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # NOQA
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    if 'local' in login_session:
        del login_session['email']
        del login_session['logged_in']
        del login_session['local']
        flash('Successfully Disconnected')
        return redirect(url_for('products'))
    else:
        """Remove Gplus login"""
        access_token = login_session['access_token']
        print 'In gdisconnect access token is %s', access_token
        print 'User name is: '
        print login_session['username']
        if access_token is None:
            print 'Access Token is None'
            response = make_response(json.dumps('Current user not connected.'), 401)  # noqa
            response.headers['Content-Type'] = 'application/json'
            return response
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # NOQA
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
            del login_session['logged_in']
            flash('Successfully Disconnected')
            return redirect(url_for('products'))
        else:
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['logged_in']
            flash('Error occurred with Disconnection')
            return redirect(url_for('products'))
