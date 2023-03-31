from django.urls import path
from .views import homepage,getBookByName

urlpatterns = [
    path('books/',homepage),
    path('getBookByName',getBookByName)
]
