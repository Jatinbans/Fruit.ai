# from flask import Flask, request, jsonify
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId

# app = Flask(__name__)

# # MongoDB Atlas connection string (replace with your URI)
# app.config["MONGO_URI"] = "mongodb+srv://ishayadav77199:Muktsar1234@cluster0.fkpry.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Initialize PyMongo
# mongo = PyMongo(app)

# # Define routes
# @app.route('/')
# def index():
#     return "Welcome to the FAQ API"

# # GET all FAQs
# @app.route('/faqs', methods=['GET'])
# def get_faqs():
#     faqs = mongo.db.faqs.find()
#     result = []
#     for faq in faqs:
#         result.append({
#             'id': str(faq['_id']),
#             'title': faq['title'],
#             'description': faq['description'],
#             'image': faq.get('image'),
#             'altText': faq.get('altText')
#         })
#     return jsonify(result)

# # GET a single FAQ
# @app.route('/faqs/<id>', methods=['GET'])
# def get_faq(id):
#     faq = mongo.db.faqs.find_one({'_id': ObjectId(id)})
#     if faq:
#         return jsonify({
#             'id': str(faq['_id']),
#             'title': faq['title'],
#             'description': faq['description'],
#             'image': faq.get('image'),
#             'altText': faq.get('altText')
#         })
#     else:
#         return jsonify({'error': 'FAQ not found'}), 404

# # POST a new FAQ
# @app.route('/faqs', methods=['POST'])
# def add_faq():
#     data = request.get_json()
#     result = mongo.db.faqs.insert_one({
#         'title': data.get('title'),
#         'description': data.get('description'),
#         'image': data.get('image'),
#         'altText': data.get('altText')
#     })
#     return jsonify({'id': str(result.inserted_id)}), 201

# # PUT (Update) an existing FAQ
# @app.route('/faqs/<id>', methods=['PUT'])
# def update_faq(id):
#     data = request.get_json()
#     result = mongo.db.faqs.update_one(
#         {'_id': ObjectId(id)},
#         {'$set': {
#             'title': data.get('title'),
#             'description': data.get('description'),
#             'image': data.get('image'),
#             'altText': data.get('altText')
#         }}
#     )
#     if result.matched_count:
#         return jsonify({'message': 'FAQ updated successfully'})
#     else:
#         return jsonify({'error': 'FAQ not found'}), 404

# # DELETE an FAQ
# @app.route('/faqs/<id>', methods=['DELETE'])
# def delete_faq(id):
#     result = mongo.db.faqs.delete_one({'_id': ObjectId(id)})
#     if result.deleted_count:
#         return jsonify({'message': 'FAQ deleted successfully'})
#     else:
#         return jsonify({'error': 'FAQ not found'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import os

import certifi


app = Flask(__name__)

# MongoDB Atlas connection string
# MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://ishayadav77199:Muktsar1234@cluster0.fkpry.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://ishayadav77199:Muktsar1234@cluster0.fkpry.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true')

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

try:
    client = MongoClient(MONGO_URI)
    # Test the connection
    client.server_info()  # This will raise an exception if the connection fails
    print("Successfully connected to MongoDB")
except errors.ServerSelectionTimeoutError as err:
    print(f"Failed to connect to MongoDB: {err}")
    exit(1)

# Connect to the specific database
db = client['faq_project']  # Replace with your database name

# Define routes
@app.route('/')
def index():
    return "Welcome to the FAQ API"

# GET all FAQs
@app.route('/faqs', methods=['GET'])
def get_faqs():
    faqs = db.faqs.find()
    result = []
    for faq in faqs:
        result.append({
            'id': str(faq['_id']),
            'title': faq['title'],
            'description': faq['description'],
            'image': faq.get('image'),
            'altText': faq.get('altText')
        })
    return jsonify(result)

# GET a single FAQ by ID
@app.route('/faqs/<id>', methods=['GET'])
def get_faq(id):
    faq = db.faqs.find_one({'_id': ObjectId(id)})
    if faq:
        return jsonify({
            'id': str(faq['_id']),
            'title': faq['title'],
            'description': faq['description'],
            'image': faq.get('image'),
            'altText': faq.get('altText')
        })
    else:
        return jsonify({'error': 'FAQ not found'}), 404

# POST a new FAQ
@app.route('/faqs', methods=['POST'])
def add_faq():
    data = request.get_json()
    result = db.faqs.insert_one({
        'title': data.get('title'),
        'description': data.get('description'),
        'image': data.get('image'),
        'altText': data.get('altText')
    })
    return jsonify({'id': str(result.inserted_id)}), 201

# PUT (Update) an existing FAQ by ID
@app.route('/faqs/<id>', methods=['PUT'])
def update_faq(id):
    data = request.get_json()
    result = db.faqs.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'title': data.get('title'),
            'description': data.get('description'),
            'image': data.get('image'),
            'altText': data.get('altText')
        }}
    )
    if result.matched_count:
        return jsonify({'message': 'FAQ updated successfully'})
    else:
        return jsonify({'error': 'FAQ not found'}), 404

# DELETE an FAQ by ID
@app.route('/faqs/<id>', methods=['DELETE'])
def delete_faq(id):
    result = db.faqs.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'FAQ deleted successfully'})
    else:
        return jsonify({'error': 'FAQ not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
