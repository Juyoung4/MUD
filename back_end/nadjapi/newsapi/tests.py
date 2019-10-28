from django.test import TestCase
import requests
import json

# Create your tests here.

def latest():
    URL = 'https://newsapi.org/v2/top-headlines?country=kr&apiKey=e12b2ee6e72c4abbb34d3462f8f00120'
    content = requests.get(URL).content
    dataset = json.loads(content)

    articles = dataset['articles']
    counter = 0
    for article in articles:
        counter += 1
    
    return print(f"Data Fetched Successfully. {counter} Articles")

latest()