# -*- coding: utf-8 -*-
"""Scoring.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1theIegPyhoZ6o8SwJZnydC3Xqm_qci4C
"""

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from nltk import pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer

# Load datasets
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# Display basic information about the datasets
print("Train Data:")
print(train_data.head())
print(train_data.info())

print("\nTest Data:")
print(test_data.head())
print(test_data.info())

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

# Text preprocessing function
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Lowercasing
    tokens = [token.lower() for token in tokens]

    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Join tokens back into text
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

# Apply text preprocessing to discourse_text column
train_data['clean_text'] = train_data['discourse_text'].apply(preprocess_text)
test_data['clean_text'] = test_data['discourse_text'].apply(preprocess_text)

# Display the preprocessed text
print("Preprocessed Text:")
print(train_data[['discourse_text', 'clean_text']].head())

# Function to calculate word count
def word_count(text):
    return len(text.split())

# Function to calculate average word length
def avg_word_length(text):
    words = text.split()
    if len(words) == 0:
        return 0
    else:
        return sum(len(word) for word in words) / len(words)

# Function to perform POS tagging
def pos_tagging(text):
    tokens = word_tokenize(text)
    return pos_tag(tokens)

# Function to perform sentiment analysis
def sentiment_analysis(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores['compound']  # Using compound score as an overall sentiment

# Apply feature engineering functions to the preprocessed text
train_data['word_count'] = train_data['clean_text'].apply(word_count)
train_data['avg_word_length'] = train_data['clean_text'].apply(avg_word_length)
train_data['pos_tags'] = train_data['clean_text'].apply(pos_tagging)
train_data['sentiment_score'] = train_data['clean_text'].apply(sentiment_analysis)

test_data['word_count'] = test_data['clean_text'].apply(word_count)
test_data['avg_word_length'] = test_data['clean_text'].apply(avg_word_length)
test_data['pos_tags'] = test_data['clean_text'].apply(pos_tagging)
test_data['sentiment_score'] = test_data['clean_text'].apply(sentiment_analysis)

# Display the engineered features
print("Engineered Features:")
print(train_data[['word_count', 'avg_word_length', 'pos_tags', 'sentiment_score']].head())