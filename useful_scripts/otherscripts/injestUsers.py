import pandas as pd
from books.models import Book

import csv
import sqlite3

conn = sqlite3.connect('book_reviews.db')
c = conn.cursor()

with open('/Users/vicentesebastiao/Desktop/book-review-dataset/BX_books.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for isbn, FirstName, book_title, first_name, last_name, publication_date, publisher, image_url, publisher_id, genre_id in reader:
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (isbn, FirstName, book_title, first_name, last_name, publication_date, publisher, image_url, publisher_id, genre_id))

conn.commit()
conn.close()


