# from dbm.ndbm import library
from django.urls import path
from books.views import homepage
from profiles import views

urlpatterns = [
    path('', views.checklogin, name="login"),
    path('reg', views.reg, name="RegisterUser"),
    path('lg/', views.logout_user, name="logout_user"),
    path('profile/<int:profile_id>', views.profile, name="profile"),
    path('updatePassword', views.update_password, name="UpdatePassword"),
    # path('base', views.base, name="base"),
    path('base', views.homefeed, name="base"),
    path('myclub', views.myclub, name="myclub"),
    path('delete_clubs', views.delete_clubs, name="delete_clubs"),
    path('myposts', views.myposts, name="myposts"),
    path('delete_post/<int:post_id>', views.delete_post, name="deletePost"),
    path('recommendations', views.recommendations, name="recommendations"),
    path('library', views.library, name="library"),
    path('favourites', views.favourites, name="favourites"),
    path('homefeed', views.homefeed, name="homefeed"),
    path('Authors', views.authors, name="Authors"),
    path('Publishers', views.publishers, name="Publishers"),
    path('getClubByName', views.getClubByName,name="getClubByName")
]
