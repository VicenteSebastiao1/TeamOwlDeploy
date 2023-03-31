from django.urls import path
from books.views import homepage
from .views import *

urlpatterns = [
    path('feed/', homepage),
    path('addComment/', add_comment, name="addComment"),

    # Ajax Views for likes
    path('like_dislike/', like_dislike, name='like_dislike_ajax_view')
]
