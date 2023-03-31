from django.shortcuts import render, redirect
from .models import Post
from profiles.views import login_required
from .models import Comment
from django.contrib import messages
from django.http import JsonResponse


def first(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'templates/feed.html', context)


@login_required
def add_comment(request):
    user_info = request.user
    if request.method == 'POST':
        post_id = request.POST["post_id"]
        comment_body = request.POST["comment_body"]
        Comment(post_id=post_id, name=user_info, body=comment_body).save()
        messages.success(request, "comment Posted successfully!")
        return redirect("base")


@login_required
def like_dislike(request):
    user_info = request.user
    status = request.GET["status"]
    post_id = request.GET["post_id"]
    post_data = Post.objects.get(id=post_id)
    if int(status) == 1:
        post_data.likes.add(user_info)
    else:
        post_data.likes.remove(user_info)
    return JsonResponse({'12': "123"})
