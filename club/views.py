from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.shortcuts import render
from profiles.models import *
from mainfeed.models import *


def club_home(request):
    user_info = request.user

    user_profile_data = UserProfile.objects.get(user=user_info.id)
    club_data_values = Club.objects.filter()
    if club_data_values.exists():
        club_data = 1
    else:
        club_data = 0
    context = {'home': False, "user_profile_data": user_profile_data, 'club_data': club_data,
               'club_data_values': club_data_values}
    return render(request, 'ClubHome.html', context)


def club_detail_post(request, club_id):
    post_comment_temp_dict = dict()
    user_info = request.user

    if request.method == 'POST':
        post_title = request.POST["postTitle"]
        post_content = request.POST["postContent"]
        club_id = request.POST["clubId"] if "clubId" in request.POST else 0
        post_image = request.FILES['postImage'] if 'postImage' in request.FILES else 0

        if club_id == 0:
            club_data = Club.objects.get(club_owner=user_info)
        else:
            club_data = Club.objects.get(id=club_id)

        if post_image != 0:
            user_post_data = Post(post_title=post_title, txtcontent=post_content,
                                  imgcontent=post_image,
                                  club=club_data, post_author=user_info)
        else:
            user_post_data = Post(post_title=post_title, txtcontent=post_content,
                                  club=club_data, post_author=user_info)
            messages.success(request, "Posted Successfully!")
        user_post_data.save()

    post_data = Post.objects.filter(club__id=club_id).select_related('post_author', 'post_author__userprofile').order_by("-date_posted")

    for data in post_data:
        if data.id in post_comment_temp_dict.keys():
            data.comments_data = post_comment_temp_dict[data.id]
            data.comments_count = len(post_comment_temp_dict[data.id])
        else:
            data.comments_data = []
            data.comments_count = 0
        data.likes_count = data.likes.count()
        data.self_liked = 1 if data.likes.filter(username=user_info.username).exists() else 0

    user_profile_data = UserProfile.objects.get(user=user_info.id)
    club_data_values = Club.objects.get(id=club_id)

    context = {'home': False, "user_profile_data": user_profile_data,
               'club_data_value': club_data_values, "post_data": post_data}
    return render(request, 'club_post.html', context)
