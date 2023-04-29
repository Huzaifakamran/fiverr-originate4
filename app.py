import requests
from dotenv import load_dotenv
import os
import re
from textblob import TextBlob

load_dotenv() 

url = "https://api.airtable.com/v0/appvGUNxzqI6SeUIG/Entries"
headers = {"Authorization": "Bearer " + os.getenv('AIRTABLE_API_KEY')}
response = requests.get(url, headers=headers)
text = response.json()
# print(text['records'])
entryID = 75
for record in text['records']:
    if record['fields']['EntryID'] == entryID:
       entry = record['fields']['Entry Title']
       print(entry)
       break
keywords = ["Keyword1", "Keyword2", "Keyword3"] # Relevant keywords for the topic


def analyze_sentiment(text):
 blob = TextBlob(text)
 sentiment = blob.sentiment
 return sentiment.polarity, sentiment.subjectivity

def analyze_clarity(text):
 words = text.split()
 avg_word_length = sum(len(word) for word in words) / len(words)
 return avg_word_length

def analyze_relevance(text, keywords):
 keywords_found = [keyword.lower() for keyword in keywords if
keyword.lower() in text.lower()]
 return len(keywords_found)

def analyze_entry(entry, keywords):
    sentiment_polarity, sentiment_subjectivity = analyze_sentiment(entry)
    clarity = analyze_clarity(entry)
    relevance = analyze_relevance(entry, keywords)
    feedback = []
    # Sentiment analysis feedback
    if sentiment_polarity > 0.5:
        feedback.append("Your entry has a positive sentiment.")
    elif sentiment_polarity < -0.5:
        feedback.append("Your entry has a negative sentiment.")
    else:
        feedback.append("Your entry has a neutral sentiment.")
    # Clarity feedback
    if clarity < 4:
        feedback.append("Your entry is easy to read and understand.")
    elif clarity > 6:
        feedback.append("Your entry might be difficult to read for some people. Consider using shorter words and clearer language.")
    # Relevance feedback
    if relevance >= len(keywords) * 0.5:
        feedback.append("Your entry is relevant to the topic.")
    else:
        feedback.append("Your entry might not be very relevant to the topic. Consider addressing more aspects of the topic.")
    return feedback

feedback = analyze_entry(entry, keywords)
for feedback_item in feedback:
 print(feedback_item)