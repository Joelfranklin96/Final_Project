# ECE Software Engineering Final Project - Spring 2023

[Demo Video](https://drive.google.com/file/d/1H65_E3qXuOnRlH9AbZd2DZwwVLL8HJUn/view?usp=share_link)

## Introduction

This repository contains the code for the final project in the ECE Software Engineering course for Spring 2023. The project is a web-based application that allows users to analyze PDF documents. The application is built using Flask, a Python-based web framework, and implements Google OAuth for user authentication.

## Features

- **Google OAuth Authentication:** Users can log in to the application using their Google accounts.
- **File Upload:** Users can upload PDF files to be analyzed.
- **Document Analysis:** The application can provide a summary of the uploaded document or extract the top 10 most common keywords from it.
- **Database Storage:** The content of the uploaded PDF and the results of the analysis are stored in a MongoDB database.
- **Result Retrieval:** Users can retrieve the results of the analysis through the web interface.

## Prerequisites

- Python 3.8 or later
- MongoDB

## Dependencies

This project requires the following Python libraries:

- Flask
- PyMongo
- PyPDF2
- google-auth-oauthlib
- google-auth
- nltk
- bson
- Werkzeug
- Flask-Session
- BERT Extractive Summarizer
- RAKE-NLTK

These can be installed by running `pip install -r requirements.txt` in your terminal.

## Setup and Installation

1. **Clone the Repository:** 
2. **Navigate into the Project Directory:**
3. **Install Dependencies:**
4. **Start the Flask Server:**

## Usage

1. **Home Page:** Navigate to the home page of the web app. If you're not logged in, you will see a login button.
2. **Login:** Click the login button and sign in with your Google account.
3. **Upload a Document:** After logging in, you will be redirected to a page where you can upload a PDF document for analysis.
4. **Select Analysis Type:** Choose the type of analysis you want (summary or keywords) and submit the form.
5. **View Results:** After the analysis is complete, you can view the results on the web interface.

## Contributing

Contributions are welcome. To contribute:

1. Fork the project.
2. Create a new branch for your features or bug fixes.
3. Commit your changes in your branch.
4. Push your changes to your fork.
5. Submit a pull request.
