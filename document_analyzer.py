# Import necessary libraries

from summarizer import Summarizer
from rake_nltk import Rake

# Function to summarize the given text
def summarize_text(content):
    model = Summarizer()
    summary = model(content, min_length=60, max_length=100, ratio=0.4)
    return summary

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Function to extract keywords from the given content
def extract_keywords(content):
    stop_words = set(stopwords.words("english"))
    word_tokens = nltk.word_tokenize(content)
    
    # Filter out stopwords and non-alphabetic tokens
    filtered_tokens = [word for word in word_tokens if word.isalpha() and word.lower() not in stop_words]

    # Calculate the frequency of each word
    freq_dist = nltk.FreqDist(filtered_tokens)

    # Extract the top 10 most common keywords
    keywords = [word for word, freq in freq_dist.most_common(10)]

    return keywords

#Function to analyze the document based on the chosen option and update the database with the result
def analyze_document(document_id, option, db):

    document = db.documents.find_one({"_id": document_id})
    content = document['content']

    if option == 'summary':
        result = summarize_text(content)
    elif option == 'keywords':
        result = extract_keywords(content)
    else:
        return None

    db.documents.update_one({"_id": document_id}, {"$set": {"result": {option: result}}})
    return result