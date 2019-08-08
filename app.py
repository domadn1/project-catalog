#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, ProductItem, User
from flask import session as login_session

import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
# import requests
from google.oauth2 import id_token
from google.auth.transport import requests
from apiclient import discovery
# import httplib2
from oauth2client import client
# import google_authentication as gAuth

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "Project Catalog"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in range(32))
    print('state ========', state)
    login_session['state'] = state
    return render_template('login.html', STATE=state) 
    #"The current session state is %s" % login_session['state']


# disconnect from the login session
@app.route('/disconnect')
def disconnect():
    if 'username' in login_session:
        gdisconnect()
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


def createUser(login_session):
    newUser = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def Is_Authenticated():
    if 'user_id' in login_session:
        return True
    return False
    # return ('user' in login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    print('\n\n\nGconnect invoked')
    try:
        # Check if the POST request is trying to log in

        print('headers ========',request.headers)
        if 'idtoken' in request.form:
            if not Is_Authenticated():
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

                # Retrive user's Google Account ID from the decoded token.
                userid = idinfo['sub']
                login_session['user_id'] = userid

                # Add the token to the flask session variable
                login_session['user'] = token

                flash('Successfully verified. You are logged in! with status 200')
                # ret_response = make_response(
                #     jsonify(
                #         message='Successfully verified. You are logged in!',
                #         status=200)
                # )

            # Nothing to do with already logged in user
            else:
                flash('User is already logged in with status 201')
                # return 'True'
                # ret_response = make_response(
                #     jsonify(message='User is already logged in.', status=201)
                # )

        # POST request without idtoken tries to log out.
        else:
            # Remove token from login session
            if Is_Authenticated():
                login_session.pop('user', None)

            flash('User has been logged out with status 200')
            # return 'False'
            # ret_response = make_response(
            #     jsonify(message="User has been logged out", status=200)
            # )

    except ValueError:
        # handles invalid token error
        flash('Error: unable to verify token id with status 401')
        # return 'False'
        # ret_response = make_response(
        #     jsonify(message='Error: unable to verify token id', status=401)
        # )

    # return ret_response
    return redirect(url_for('showCatalog'))


@app.route('/gdisconnect')
def gdisconnect():
    ''' Logout from Application '''
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['google_id']
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


def category_exists(category_name):
    ''' Checks if category exist
        return list with boolean value and category object if exist
    '''
    category = session.query(Category).filter_by(name=category_name).first()
    if category is None:
        return [False]
    return [True, category]


def product_exists(product_name):
    ''' Checks if product exist
        return list with boolean value and product object if exist
    '''
    product = session.query(ProductItem).filter_by(name=product_name).first()
    if product is None:
        return [False]
    return [True, product]


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    ''' Return all Categories '''
    categories = session.query(Category).order_by(asc(Category.name))
    products = session.query(ProductItem).order_by(asc(ProductItem.name))
    authenticate = Is_Authenticated()
    print('Is_Authenticated() === ',authenticate)
    return render_template('catalog.html', categories=categories,
        products=products, authenticate=authenticate)


@app.route('/catalog/<category_name>/items')
def exploreCategory(category_name):
    ''' Return all products which belongs to given category '''
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name).one()
    products_query = session.query(
        ProductItem).filter_by(category_id=category.id)
    products = products_query.all()
    total_products = products_query.count()
    return render_template('catagoryProducts.html', total=total_products,
        category=category, products=products,
        categories=categories, authenticate=Is_Authenticated())


@app.route('/catalog/<category_name>/<product_name>')
def exploreProduct(category_name, product_name):
    ''' Returns product detail '''
    categories = session.query(Category).order_by(asc(Category.name))
    product = session.query(
        ProductItem).filter_by(name=product_name).one()
    return render_template('product.html', product=product,
        categories=categories, authenticate=Is_Authenticated())


@app.route('/catalog/category/new/', methods=['GET', 'POST'])
def newCategory():
    ''' Create new category
        only allows to registered user
    '''
    if not Is_Authenticated():
        return redirect('/login')
    if request.method == 'POST':
        if category_exists(request.form['name'])[0]:
            flash('Category %s Already Exists! Please Try with Different Name'
                % request.form['name'])
            return render_template('newCategory.html')
        print('login_session==========',login_session)
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html', authenticate=Is_Authenticated())


@app.route('/catalog/product/new/', methods=['GET', 'POST'])
def newProduct():
    ''' Create new product
        only allows to registered user
    '''
    if not Is_Authenticated():
        return redirect('/login')
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        if product_exists(request.form['name'])[0]:
            flash('Product %s Already Exists! Please Try with Different Name'
                % request.form['name'])
            return render_template('newProduct.html')
        newProduct = ProductItem(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newProduct)
        flash('New Category %s Successfully Created' % newProduct.name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newProduct.html', categories=categories,
            authenticate=Is_Authenticated())


@app.route('/catalog/<product_name>/edit/', methods=['GET', 'POST'])
def editProduct(product_name):
    ''' Updates product detail
        only allows related user
    '''
    if not Is_Authenticated():
        return redirect('/login')
    categories = session.query(Category).order_by(asc(Category.name))

    productToEdit = session.query(
        ProductItem).filter_by(name=product_name).one()

    if request.method == 'POST':
        category = session.query(Category).filter_by(
            id=productToEdit.category_id).one()
        if request.form['name'] and (
            productToEdit.name != request.form['name']):
            # Checks if Product's name updated through web then reflect in DB
            productToEdit.name = request.form['name']
            flash('Product name successfully edited %s' % productToEdit.name)
        if request.form['description'] and (
            productToEdit.description != request.form['description']):
            # Checks if Product's description updated through web
            # then reflect in DB
            productToEdit.description = request.form['description']
            flash('Product description successfully edited %s' %
                  productToEdit.description)
        if request.form['price'] and (
            productToEdit.price != request.form['price']):
            # Checks if Product's price updated through web
            # then reflect in DB
            productToEdit.price = request.form['price']
            flash('Product price successfully edited to %s' %
                  productToEdit.price)
        if request.form['category_name'] and productToEdit.category_id != int(
            request.form['category_name']):
            # Checks if Product's Category updated through web 
            # then reflect in DB
            productToEdit.category_id = request.form['category_name']
            category = session.query(Category).filter_by(
                id=productToEdit.category_id).one()
            flash('Product category successfully edited %s' % category.name)
        session.commit()
        return redirect(url_for('exploreProduct',
                                category_name=category.name,
                                product_name=productToEdit.name))
    else:
        return render_template(
            'editProduct.html', product=productToEdit, categories=categories,
            authenticate=Is_Authenticated())


@app.route('/catalog/<product_name>/delete/',
           methods=['GET', 'POST'])
def deleteProduct(product_name):
    ''' Deletes Product permananetly
        only allows related user
    '''
    if  not Is_Authenticated():
        return redirect('/login')
    product = session.query(
        ProductItem).filter_by(name=product_name).one()
    category = session.query(Category).filter_by(id=product.category_id).one()
    if request.method == 'POST':
        session.delete(product)
        flash('%s Successfully Deleted' % product.name)
        session.commit()
        return redirect(
            url_for('exploreCategory', category_name=category.name))
    else:
        return render_template(
            'deleteProduct.html', product=product, category=category,
            authenticate=Is_Authenticated())


@app.route('/api/v1/catalog.json')
def catalogJSON():
    ''' Returns json endpoint for all items with all categories '''
    categories = session.query(Category).all()
    category = []

    for c in categories:
        products = session.query(
            ProductItem).filter_by(category_id=c.id).all()
        category_dict = c.serialize
        category.append(category_dict)
        product_list = [p.serialize for p in products]
        category_dict.update({'items': product_list})

    return jsonify(category=category)


@app.route('/api/v1/catalog/<category_name>/items.json')
def categoryItemsJSON(category_name):
    ''' Returns json endpoint for all items with specified category '''
    valid_category = category_exists(category_name)
    if valid_category[0]:
        products = session.query(ProductItem).filter_by(
            category_id=valid_category[1].id).all()
        return jsonify(items=[p.serialize for p in products])
    else:
        return jsonify(error='This category does not exist!')


@app.route('/api/v1/catalog/<category_name>/<product_name>/json')
def categoryProductJSON(category_name, product_name):
    ''' Returns json endpoint with specified category and Product '''
    valid_category = category_exists(category_name)
    valid_product = product_exists(product_name)
    if valid_category[0]:
        if valid_product[0]:
            if valid_product[1].category_id == valid_category[1].id:
                return jsonify(item=[valid_product[1].serialize])
            else:
                return jsonify(error='Product Category does not match with this category!')
        else:
            return jsonify(error='This Product does not exist!')
    else:
        return jsonify(error='This category does not exist!')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5002)
