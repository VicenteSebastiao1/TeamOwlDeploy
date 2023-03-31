import requests
from books.models import book

def get_genre(isbn):

     results = []
     for isbns in isbns:
     url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn
     response = requests.get(url)
     data = response.json()
     results.append(data['items'][0]['volumeInfo']['categories'][0])
     return results












