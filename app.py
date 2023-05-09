# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from werkzeug.utils import secure_filename
from document_reader import save_pdf_content_to_db
from document_analyzer import analyze_document
import json
from google.auth.transport import requests
import os

# Create Flask app and configure it
app = Flask(__name__)
app.config.from_object('config')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Initialize session for the app
Session(app)

# Connect to the database
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client.pdf_analysis

# Set up Google OAuth2 flow
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Load client secrets for OAuth2
with open("client_secret.json", "r") as f:
    client_secrets = json.load(f)

flow = Flow.from_client_secrets_file(
    "client_secret.json",
    scopes=['openid', 'email', 'profile'],
    redirect_uri=client_secrets["web"]["redirect_uris"][0]
)

# Define routes for the app

# Home route
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('index.html')

# Login route
@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

# Callback route for OAuth2
@app.route('/callback')
def callback():
    flow.fetch_token(code=request.args.get('code'))
    token = id_token.verify_oauth2_token(
        flow.credentials.id_token, requests.Request())

    session['user_id'] = token['sub']
    session['email'] = token['email']
    return redirect(url_for('index'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('index'))

# Route to handle PDF uploads
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"result": "error", "message": "Unauthorized access."}), 401

    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    # Check if the file has a valid filename and extension
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    # Save the file and analyze it
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Read PDF content and save it to the database
        document_id = save_pdf_content_to_db(os.path.join(app.config['UPLOAD_FOLDER'], filename), db)

        # Analyze document and store the result in the database
        option = request.form.get('option')
        analyze_document(document_id, option, db)

        return jsonify({'result': 'success', 'document_id': str(document_id)}), 200
    else:
        return jsonify({'error': 'An error occurred'}), 400

@app.route('/get_result', methods=['POST'])
def get_result():
    # Retrieve document_id and analysis option from request
    document_id = request.form['document_id']
    option = request.form['option']
    # Check if document_id is provided
    if not document_id:
        return jsonify({'error': 'Invalid document ID'})

    # Fetch the document from the database
    document = db.documents.find_one({"_id": ObjectId(document_id)})

    # Check if the analysis result is available
    if document is None or 'result' not in document:
        return jsonify({'error': 'Analysis is still in progress. Please try again later.'})

    # Retrieve the analysis result for the specified option
    result = document['result'][option]

    # Check if there are any results for the specified option
    if len(result) == 0:
        return jsonify({'error': 'No {} found'.format(option)})

    # Return the analysis result as a JSON object
    return jsonify({'result': result})

# Function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Main entry point for the application

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)