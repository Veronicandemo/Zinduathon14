from config import app, db
import bcrypt
from flask import Flask, jsonify, make_response, request, session
from models import User, Farmer, Product, Course
import jwt;
import os ;
import base64;
from datetime import datetime, timedelta;

import cloudinary
import cloudinary.uploader

from utils import cloudconfig
cloudconfig

secret_key = base64.b64encode(os.urandom(24)).decode('utf-8')

@app.route("/users")
def get_users():
    users_list = []
    users = User.query.all()
    for user in users:
        user_dict = {
            "username": user.username,
            "email": user.email
        }
        users_list.append(user_dict)

    response_body = users_list
    response = make_response(jsonify(response_body), 200)

    return response

@app.route("/farmers")
def get_farmers():
    farmers_list = []
    farmers = Farmer.query.all()
    for farmer in farmers:
        farmer_dict = {
            "username": farmer.username,
            "email": farmer.email
        }
        farmers_list.append(farmer_dict)

    response_body = farmers_list
    response = make_response(jsonify(response_body), 200)

    return response

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    if request.method == 'POST':
        existing_username = User.query.filter(User.username == data.get('username')).first()
        existing_email = User.query.filter(User.username == data.get('email')).first()

        if existing_username is None and existing_email is None:

            image_file = request.files['profile_img']
            if image_file:
                try:
                    result = cloudinary.uploader.upload(image_file)  # Upload the image to Cloudinary
                    image_url = result['secure_url']  # Get the secure URL of the uploaded image

                except Exception as e:
                    response_body = {"error": "Image upload failed"}
                    response = make_response(response_body, 500)
                    return response
            else:
                # If no image is provided, set image_url to None or any default value you prefer
                image_url = None

            hashpass = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
            new_user = User(
                username=data.get('username'),
                email=data.get('email'),
                password=hashpass,
                profile_img = image_url
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        
        

        return jsonify({'error': 'Username/Password already exists!'}), 403

@app.route('/login', methods=['POST'])
def login():
    data = request.form

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Input the required fields'}), 401

    user = User.query.filter(User.email == email).first()

    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            expiration_time = datetime.utcnow() + timedelta(hours=400)
            token = jwt.encode({'user_id': user.id, 'exp': expiration_time}, secret_key, algorithm='HS256')
            profile_img = user.profile_img

            return jsonify({'message': 'Logged in successfully!', 'token': token, 'profile_img': profile_img}), 200
        
    return jsonify({'error': 'Invalid username/password!'}), 401

@app.route('/farmer/register', methods=['POST'])
def register_farmer():
    data = request.form
    if request.method == 'POST':
        existing_username = Farmer.query.filter(Farmer.username == data.get('username')).first()
        existing_email = Farmer.query.filter(Farmer.username == data.get('email')).first()

        if existing_username is None and existing_email is None:
            image_file = request.files['profile_img']
            if image_file:
                try:
                    result = cloudinary.uploader.upload(image_file)  # Upload the image to Cloudinary
                    image_url = result['secure_url']  # Get the secure URL of the uploaded image

                except Exception as e:
                    response_body = {"error": "Image upload failed"}
                    response = make_response(response_body, 500)
                    return response
                
            else:
                # If no image is provided, set image_url to None or any default value you prefer
                image_url = None


            hashpass = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
            new_farmer = Farmer(
                username=data.get('username'),
                email=data.get('email'),
                password=hashpass,
                profile_img = image_url
            )
            db.session.add(new_farmer)
            db.session.commit()
            return jsonify({'message': 'Farmer created successfully'}), 201

        return jsonify({'error': 'Username/Password already exists!'}), 403

@app.route('/farmer/login', methods=['POST'])
def login_farmer():
    data = request.form

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Input the required fields'}), 401

    farmer = Farmer.query.filter(Farmer.email == email).first()

    if farmer:
        if bcrypt.checkpw(password.encode('utf-8'), farmer.password):
            expiration_time = datetime.utcnow() + timedelta(hours=400)
            token = jwt.encode({'user_id': farmer.id, 'exp': expiration_time}, secret_key, algorithm='HS256')
            profile_img = farmer.profile_img

            session['farmer_id'] = farmer.id

            return jsonify({'message': 'Logged in successfully!', 'token': token, 'profile_img': profile_img}), 200
        
    return jsonify({'error': 'Invalid username/password!'}), 401
    

# Helper function to decode the token
def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token has expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
    
@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('farmer_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        product_list = []
        products = Product.query.all()
        for product in products:
            farmer = Farmer.query.filter(Farmer.id == product.farmer_id).first()
            product_dict = {
                'id': product.id,
                'image_url': product.image_url,
                'location': product.location,
                'quantity': product.quantity,
                'farmer_id': product.farmer_id,
                'farmer_name': farmer.username
            }
            product_list.append(product_dict)
        response_body = product_list
        response = make_response(jsonify(response_body), 200)
        return response
    
    elif request.method == 'POST':
        data = request.form
        if data:
            

            if session.get('farmer_id'):
                farmer = Farmer.query.filter(Farmer.id == session.get('farmer_id')).first()
            else:
                response_body = {"error": "Login as farmer to add product!"}
                response = make_response(response_body)
                return response

            image_file = request.files['image_file']
            location = data.get('location')
            quantity = data.get('quantity')
            farmer_id = farmer.id

            if image_file:
                try:
                    result = cloudinary.uploader.upload(image_file)  # Upload the image to Cloudinary
                    image_url = result['secure_url']  # Get the secure URL of the uploaded image

                except Exception as e:
                    response_body = {"error": "Image upload failed"}
                    response = make_response(response_body, 500)

            else:
                # If no image is provided, set image_url to None or any default value you prefer
                image_url = None

            new_product = Product(image_url=image_url, location=location, quantity=quantity, farmer_id=farmer_id)
            db.session.add(new_product)
            db.session.commit()
            response_body = {"message": "Product created successfully!"}
            response = make_response(response_body, 201)

        else:
            response_body = {"error": "Input data!"}
            response = make_response(response_body)

        return response
    
@app.route('/products/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def product_by_id(id):
    product = Product.query.filter_by(id=id).first()
    
    if product:
        farmer = Farmer.query.filter(Farmer.id == product.farmer_id).first()
        # product.farmer_name = farmer.username
        if request.method == 'GET':
        #     return jsonify(product.serialize(), farmer_name=farmer.username)

            product_dict = {
                    'id': product.id,
                    'image_url': product.image_url,
                    'location': product.location,
                    'quantity': product.quantity,
                    'farmer_id': product.farmer_id,
                    'farmer_name': farmer.username
                }
            response_body = product_dict
            response = make_response(jsonify(response_body), 200)
            return response

        
        if request.method == "DELETE":
            db.session.delete(product)
            db.session.commit()
            response_body = {"message": "Product deleted!"}
            response = make_response(response_body, 200)
            return response
        if request.method == "DELETE":
            db.session.delete(product)
            db.session.commit()
            response_body = {"message": "Product deleted!"}
            response = make_response(response_body, 200)
            return response
    else:
        response_body = {"error": "Product not found"}
        response = make_response(jsonify(response_body), 404)
        return response
    
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'GET':
        course_list = []
        courses = Course.query.all()
        for course in courses:
            
            product_dict = {
                'id': course.id,
                'image_url': course.image_url,
                'video_url': course.video_url,
                'title':course.title,
                'description': course.description,
                'content': course.content
            }
            course_list.append(product_dict)
        response_body = course_list
        response = make_response(jsonify(response_body), 200)
        return response
    
    elif request.method == 'POST':
        data = request.form
        if data:

            image_file = request.files['image_file']
            video_file = request.files['video_file']
            title = data.get('title')
            description = data.get('description')
            content = data.get('content')

            if image_file:
                try:
                    result = cloudinary.uploader.upload(image_file)  # Upload the image to Cloudinary
                    image_url = result['secure_url']  # Get the secure URL of the uploaded image

                except Exception as e:
                    response_body = {"error": "Image upload failed"}
                    response = make_response(response_body, 500)

            else:
                # If no image is provided, set image_url to None or any default value you prefer
                image_url = None

            if video_file:
                try:
                    result = cloudinary.uploader.upload(video_file, resource_type='video')  # Upload the image to Cloudinary
                    video_url = result['secure_url']  # Get the secure URL of the uploaded image
                

                except Exception as e:
                    response_body = {"error": "Video upload failed"}
                    response = make_response(response_body, 500)

            new_course = Course(image_url=image_url, video_url=video_url, title=title, description=description, content=content)
            db.session.add(new_course)
            db.session.commit()
            response_body = {"message": "Course created successfully!"}
            response = make_response(response_body, 201)

        else:
            response_body = {"error": "Input data!"}
            response = make_response(response_body)

        return response
    
if __name__ == '__main__':
    app.run(debug=True)