# This is the Script that gets the genre category from the ISBN 10 digits using the Google Books API
# You can update this script to extract all types of data from Google Books Api and uploads it to the Database Directly.
# Instructions: To run this script use the command python manage.py shell < useful_scripts/getisbn2.py 
# within a >>PYTHON Shell TERMINAL in the project enviorment.

from books.models import Book,Genre
from tqdm import tqdm
import csv
import requests
import io 
# API endpoint
url = 'https://www.googleapis.com/books/v1/volumes'
# Open the CSV file
# filename = '/Users/vicentesebastiao/Desktop/book-review-dataset/BookRelatedData/BX_Books.csv'
# isbn_list = []
# with io.open(filename, 'r') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=";")
#     problems = 0
#     try:
#         for row in reader:
#             isbn_list.append(row['isbn'])
#     except Exception as e:
#         problems+=1
#     print(problems)
#     # Get the values in the ISBN column
#     # isbn_list = [row['isbn;book_title;first_name;last_name;publication_date;publisher;image_url;publisher_id;genre_id'] for row in reader]
# # Create a dictionary to store the genres for each ISBN

genre_dict = {}
counter = 0

for b in tqdm(Book.objects.filter(genre_id__lt=41 )):

    isbn = b.isbn
    # Create a dictionary of parameters to pass to the API
    # params = {'q': 'isbn:{}'.format(isbn)}
    tmp = url
    url = url + '?q='+isbn
    # # Send a GET request to the API endpoint
    response = requests.get(url) 
    url = tmp
    counter +=1

    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        try:
            data = response.json()
            #print(data)
            # Get the genre for the book, if available
            genre = data['items'][0]['volumeInfo']['categories'][0]

            if genre is None or len(genre) == 0:
                continue
            
            if not Genre.objects.filter(name=genre).exists():
                g = Genre(name=genre)
                g.save()
                b.genre = g
                b.save()
            else:
                try:
                    g = Genre.objects.filter(name=genre)[:1].get()
                    b.genre = g
                    b.save()
                except:
                    continue
        except:
            continue