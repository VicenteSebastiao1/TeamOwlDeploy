from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.http import JsonResponse
from .models import Book, Publisher, Genre


def homepage(request):
    return render(request, 'index.html')


def getBookByName(request):
    name = request.GET.get("name")
    book_set = Book.objects.filter(book_title__contains=name)
    book_list = []
    for i in book_set:
        print(i.id, "i.id")
        publisher = Publisher.objects.filter(Publisher_id=i.publisher_id).filter()[0]
        genre = Genre.objects.filter(id=i.genre_id).filter()[0]
        data = {
            "isbn": i.isbn,
            "book_title": i.book_title,
            "publication_date": i.publication_date,
            "image_url": i.image_url,
            "publisher": publisher.pubisher_name,
            "publisher_email": publisher.publisher_email,
            "publisher_address": publisher.publisher_address,
            "genre_name": genre.name, }
        book_list.append(data)
        print(book_set)

    return render(request, "feedBook.html", locals())





