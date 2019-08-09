#!/usr/bin/env python3

''' This module shows Product catalog as web application and
allows to add products on display under different category
'''

import random
import string
import json

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from google.oauth2 import id_token
from google.auth.transport import requests

from database_setup import Base, Category, ProductItem, User


app = Flask(__name__)

# Connect to Database and create database session
ENGINE = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = ENGINE

DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']


@app.route('/login')
def show_login():
    ''' Create anti-forgery state token '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # Returns Login screen with google account login
    return render_template('login.html', STATE=state)


def create_user(loginsession):
    ''' Create user in database from login session'''
    new_user = User(name=loginsession['username'],
                    email=loginsession['email'],
                    picture=loginsession['picture'])
    SESSION.add(new_user)
    SESSION.commit()
    user = SESSION.query(User).filter_by(email=loginsession['email']).one()
    return user.id


def get_user_id(email):
    ''' Finds user and returns id for given email, if exists '''
    user = SESSION.query(User).filter_by(email=email).first()
    if user:
        return user.id
    return None


def is_authenticated():
    ''' Checks if token exist in session then Authenticate user '''
    if 'username' in login_session:
        return True
    return False


@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' Tries to connect with Google to authenticate valid user
        Allow application login through Google account
        Make application login on successful login of google user
        Returns to Catalog home screen
    '''
    try:
        # Check if the POST request is trying to log in
        if 'idtoken' in request.form:
            if not is_authenticated():
                # Retrive token from post request
                token = request.form['idtoken']

                # Verify token and CLIENT_ID of the app for accessing backend
                idinfo = id_token.verify_oauth2_token(
                    token, requests.Request(), CLIENT_ID)

                # Prepares a list of verified providers
                verified_providers = [
                    'accounts.google.com',
                    'https://accounts.google.com'
                ]

                # Verifies Service Provider
                if idinfo['iss'] not in verified_providers:
                    raise ValueError('Wrong issuer.')

                # Adds user profile information to the session
                login_session['username'] = idinfo['name']
                login_session['email'] = idinfo['email']
                login_session['picture'] = idinfo['picture']

                # Checks if user exists, and make a new one if it doesn't
                user_id = get_user_id(idinfo["email"])
                if not user_id:
                    user_id = create_user(login_session)

                login_session['user_id'] = user_id # Adds user to the session
                # Retrive user's Google Account ID from the decoded token.
                # and add to the session
                login_session['google_id'] = idinfo['sub']

                # Add the token to the session
                login_session['idtoken'] = token

                flash('Successfully verified. You are logged in! with status 200')

            # Nothing to do with already logged in user
            flash('User is already logged in with status 201')

    except ValueError:
        # handles invalid token error
        flash('Error: unable to verify token id with status 401')

    # Returns to Catalog Screen
    return redirect(url_for('show_catalog'))


@app.route("/gdisconnect")
def logout():
    ''' Logging out only from this application and not from the google '''
    del login_session['user_id']
    del login_session['google_id']
    del login_session['idtoken']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    flash('Successfully Logged out!')
    return redirect(url_for('show_catalog'))


def category_exists(category_name):
    ''' Checks if category exist
        return list with boolean value and category object if exist
    '''
    category = SESSION.query(Category).filter_by(name=category_name).first()
    if category is None:
        return [False]
    return [True, category]


def product_exists(product_name):
    ''' Checks if product exist
        return list with boolean value and product object if exist
    '''
    product = SESSION.query(ProductItem).filter_by(name=product_name).first()
    if product is None:
        return [False]
    return [True, product]


@app.route('/')
@app.route('/catalog/')
def show_catalog():
    ''' Return all Categories '''
    categories = SESSION.query(Category).order_by(asc(Category.name))
    products = SESSION.query(ProductItem).order_by(asc(ProductItem.name))
    return render_template('catalog.html', categories=categories,
                           products=products,
                           authenticate=is_authenticated())


@app.route('/catalog/<category_name>/items')
def explore_category(category_name):
    ''' Return all products which belongs to given category '''
    categories = SESSION.query(Category).order_by(asc(Category.name))
    category = SESSION.query(Category).filter_by(name=category_name).one()
    products_query = SESSION.query(
        ProductItem).filter_by(category_id=category.id)
    products = products_query.all()
    total_products = products_query.count()
    return render_template('catagoryProducts.html', total=total_products,
                           category=category, products=products,
                           categories=categories,
                           authenticate=is_authenticated())


@app.route('/catalog/<category_name>/<product_name>')
def explore_product(category_name, product_name):
    ''' Returns product detail '''
    categories = SESSION.query(Category).order_by(asc(Category.name))
    product = SESSION.query(
        ProductItem).filter_by(name=product_name).one()
    return render_template('product.html', product=product,
                           categories=categories,
                           category=category_name,
                           authenticate=is_authenticated())


@app.route('/catalog/category/new/', methods=['GET', 'POST'])
def new_category():
    ''' Create new category
        only allows to registered user
    '''
    if not is_authenticated():
        return redirect('/login') # if not logged in, redirect to login screen

    if request.method == 'POST':
        # Checks if category already exist
        # then return to AddCategory screen back
        if category_exists(request.form['name'])[0]:
            flash('Category %s Already Exists! Please Try with Different Name'
                  % request.form['name'])
            return render_template('newCategory.html')

        # Creates new category in database
        newcateg = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        SESSION.add(newcateg)
        flash('New Category %s Successfully Created' % newcateg.name)
        SESSION.commit()
        # Returns to catalog screen on successful creation of category
        return redirect(url_for('show_catalog'))

    # For GET request, returns to AddCategory screen
    return render_template('newCategory.html', authenticate=is_authenticated())


@app.route('/catalog/product/new/', methods=['GET', 'POST'])
def new_product():
    ''' Create new product
        only allows to registered user
    '''
    if not is_authenticated():
        return redirect('/login') # if not logged in, redirect to login screen
    categories = SESSION.query(Category).order_by(asc(Category.name))

    # Checks if request asking for data or submiting data
    if request.method == 'POST':
        # Checks if product already exist
        # then return to AddProduct screen back
        if product_exists(request.form['name'])[0]:
            flash('Product %s Already Exists! Please Try with Different Name'
                  % request.form['name'])
            return render_template('newProduct.html')
        # Creates new product in database
        newproduct = ProductItem(
            name=request.form['name'], description=request.form['description'],
            category_id=request.form['category_name'], price=request.form['price'],
            user_id=login_session['user_id'])
        SESSION.add(newproduct)
        flash('New Category %s Successfully Created' % newproduct.name)
        SESSION.commit()
        # Returns to catalog screen on successful creation of category
        return redirect(url_for('show_catalog'))

    # For GET request, returns to AddProduct screen
    return render_template('newProduct.html', categories=categories,
                           authenticate=is_authenticated())


@app.route('/catalog/<product_name>/edit/', methods=['GET', 'POST'])
def edit_product(product_name):
    ''' Updates product detail
        only allows related user
    '''
    if not is_authenticated():
        return redirect('/login') # if not logged in, redirect to login screen
    categories = SESSION.query(Category).order_by(asc(Category.name))

    # Search Product from database for given product name
    product_to_edit = SESSION.query(
        ProductItem).filter_by(name=product_name).one()

    # Check if the user is the owner of this product
    if product_to_edit.user_id != login_session['user_id']:
        flash('Only owner of the product can make changes.')
        category = SESSION.query(Category).filter_by(
            id=product_to_edit.category_id).one()
        return redirect(url_for('explore_product', category_name=category.name,
                                product_name=product_name))

    # Checks if request asking for data or submiting data
    if request.method == 'POST':
        # Fetches Category from database for given product
        category = SESSION.query(Category).filter_by(
            id=product_to_edit.category_id).one()

        # Update product name in database if edited by web user
        if request.form['name'] and (
                product_to_edit.name != request.form['name']):

            # Checks if Product's name updated through web then reflect in DB
            product_to_edit.name = request.form['name']
            flash('Product name successfully edited %s' % product_to_edit.name)

        # Update product description in database if edited by web user
        if request.form['description'] and (
                product_to_edit.description != request.form['description']):

            # Checks if Product's description updated through web
            # then reflect in DB
            product_to_edit.description = request.form['description']
            flash('Product description successfully edited %s' %
                  product_to_edit.description)

        # Update product price in database if edited by web user
        if request.form['price'] and (
                product_to_edit.price != request.form['price']):

            # Checks if Product's price updated through web
            # then reflect in DB
            product_to_edit.price = request.form['price']
            flash('Product price successfully edited to %s' %
                  product_to_edit.price)

        # Update product category in database if edited by web user
        if request.form['category_name'] and product_to_edit.category_id != int(
                request.form['category_name']):

            # Checks if Product's Category updated through web
            # then reflect in DB
            product_to_edit.category_id = request.form['category_name']
            category = SESSION.query(Category).filter_by(
                id=product_to_edit.category_id).one()
            flash('Product category successfully edited %s' % category.name)
        SESSION.commit()

        # Returns to Product Detail screen with updated detail
        return redirect(url_for('explore_product',
                                category_name=category.name,
                                product_name=product_to_edit.name))

    # For GET request, returns to EditProduct screen
    return render_template(
        'editProduct.html', product=product_to_edit, categories=categories,
        authenticate=is_authenticated())


@app.route('/catalog/<product_name>/delete/',
           methods=['GET', 'POST'])
def delete_product(product_name):
    ''' Deletes Product permananetly
        only allows related user
    '''
    if  not is_authenticated():
        return redirect('/login') # if not logged in, redirect to login screen
    product = SESSION.query(
        ProductItem).filter_by(name=product_name).one()
    category = SESSION.query(Category).filter_by(id=product.category_id).one()

    # Check if the user is the owner of this product
    if product.user_id != login_session['user_id']:
        flash('Only owner of the product can make changes.')
        category = SESSION.query(Category).filter_by(
            id=product.category_id).one()
        return redirect(url_for('explore_product', category_name=category.name,
                                product_name=product_name))

    # Checks if request asking for data or submiting data
    if request.method == 'POST':
        SESSION.delete(product) # Removes product from database
        flash('%s Successfully Deleted' % product.name)
        SESSION.commit()

        # Returns to ShowProduct for category page after removing product
        return redirect(
            url_for('explore_category', category_name=category.name))

    # For GET request, returns to DeleteProduct screen
    return render_template(
        'deleteProduct.html', product=product, category=category,
        authenticate=is_authenticated())


@app.route('/api/v1/catalog.json')
def catalog_json():
    ''' Returns json endpoint for all items with all categories '''
    categories = SESSION.query(Category).all()
    category_list = []

    for category in categories:
        products = SESSION.query(
            ProductItem).filter_by(category_id=category.id).all()
        category_dict = category.serialize
        category_list.append(category_dict)
        product_list = [product.serialize for product in products]
        category_dict.update({'items': product_list})

    return jsonify(category=category_list)


@app.route('/api/v1/catalog/<category_name>/items.json')
def category_items_json(category_name):
    ''' Returns json endpoint for all items with specified category '''
    valid_category = category_exists(category_name)
    if valid_category[0]:
        products = SESSION.query(ProductItem).filter_by(
            category_id=valid_category[1].id).all()
        return jsonify(items=[p.serialize for p in products])
    return jsonify(error='This category does not exist!')


@app.route('/api/v1/catalog/<category_name>/<product_name>/json')
def category_product_json(category_name, product_name):
    ''' Returns json endpoint with specified category and Product '''
    valid_category = category_exists(category_name)
    valid_product = product_exists(product_name)
    if valid_category[0]:
        if valid_product[0]:
            if valid_product[1].category_id == valid_category[1].id:
                return jsonify(item=[valid_product[1].serialize])
            return jsonify(error='Product Category does not match with this category!')
        return jsonify(error='This Product does not exist!')
    return jsonify(error='This category does not exist!')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
