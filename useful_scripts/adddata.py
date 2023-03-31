import pandas as pd
import os,sys
import django
import sys, os
sys.path.append('/Users/vicentesebastiao/python-workspace/TeamOwl')
sys.path.append('/Users/vicentesebastiao/python-workspace/TeamOwl/teamowl')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from books.models import Author, Book, Publisher,Genre



def addAuthor():
    df = pd.read_excel('/Users/vicentesebastiao/Desktop/book-review-dataset/AuthorRelatedData/authoridclean.xlsx')
    for index,row in df.iterrows():
        print(row['author_id'],row['first_name'],row['last_name'])
        author = Author(row['author_id'],row['first_name'],row['last_name'])
        author.save()

def addBookNoGenre():
    filename = '/Users/vicentesebastiao/Desktop/book-review-dataset/BookRelatedData/BX_Books.csv'
    df = pd.read_csv(filename,delimiter=";")
    try:
        g = Genre(name="fiction")
        g.save()
    except Exception as e:
        print(e)
    
    for index,row in df.iterrows():
       
        try:
            isbn = row['isbn']
            book_title = row['book_title']
            first_name = row['first_name']
            last_name = row['last_name']
            publish_date = str(int(row['publication_date'])) + '-01-01'
            author = Author.objects.filter(first_name=first_name, last_name=last_name)

            publisher = Publisher.objects.filter(pubisher_name=row['publisher'])[:1].get()
            genre = Genre.objects.filter(name="fiction")[:1].get()
            
            book = Book(isbn=isbn,book_title=book_title,publication_date=publish_date,publisher=publisher,genre=genre)
            book.save()
            book.authors.set(author)

        except Exception as e:
            print(e)
        
        



def addPublisher():
    filename = '/Users/vicentesebastiao/Desktop/book-review-dataset/PublisherRelatedData/publishers.xlsx'
    df = pd.read_excel(filename)
    print(df)
    for index,row in df.iterrows():
        print(row['publisher_id'])
        try:
        # isbn	book_title	first_name	last_name	publication_date	publisher	genre_id
            a = row['publisher_id']
            b = row['publisher_name']
            c = row['publisher_email']
            d = row['publisher_address']
            p = Publisher(a,b,c,d)
            p.save()
        except Exception as e:
            print(e)

    for p in Publisher.objects.all():
        print(p.pubisher_name)

# addPublisher()
addBookNoGenre()