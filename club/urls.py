from django.urls import path
from .views import *

urlpatterns = [
    path('clubs/', club_home, name="club_home"),
    path('club/<int:club_id>/post', club_detail_post, name="club_detail_post"),
]
