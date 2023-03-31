from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Author(models.Model):
    author_id = models.AutoField(primary_key=True, db_index=True)
    first_name = models.CharField(max_length=100, null=False, default= '')
    last_name = models.CharField(max_length=100, null=False, default= '')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Publisher(models.Model):
    Publisher_id = models.AutoField(primary_key=True,db_index=True)
    pubisher_name = models.CharField(max_length=100)
    publisher_email = models.CharField(max_length=200)
    publisher_address= models.CharField(max_length=200)


class Genre(models.Model):
    # genre_id = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

class Ratings(models.Model):
    user_id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=15)
    book_rating = models.FloatField()

class Book(models.Model):
    isbn = models.CharField(max_length=20, default='')
    book_title = models.CharField(max_length=300, db_index=True)
    authors = models.ManyToManyField(Author)
    publication_date = models.DateField(null=True,default='2023-01-01')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    image_url= models.URLField(max_length=1000,blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True) 

    # def __str__(self):
    #     return self.book_title + ' By ' + self.authors + self.publication_date


