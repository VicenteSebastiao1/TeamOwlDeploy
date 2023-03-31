from django.db import models
from profiles.models import Club 
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    post_title = models.CharField(max_length=120)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    txtcontent = models.TextField(max_length=500, blank=True)
    imgcontent = models.ImageField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    likes = models.ManyToManyField(User, blank=True,  related_name="post_likes")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE,related_name="name")
    body = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True,related_name="likes")

    # def total_likes(self):
    #     return self.likes.count()

    # def __str__(self):
    #     return '%s - %s' %(self.post.post_title, self.name)


class CommentReplys(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="comment")
    reply = models.ForeignKey(Comment,on_delete=models.CASCADE, related_name="reply")
    

