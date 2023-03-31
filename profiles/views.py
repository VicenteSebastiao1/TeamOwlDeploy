from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from mainfeed.models import *
from books.models import *
from profiles.models import UserProfile, Club
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.core.paginator import Paginator
import  json as simplejson
from django.db.models import Q


MEDIA_URL = settings.MEDIA_URL


def login_required(view_func):
    def func_wrapper(request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            return redirect('login')

        except Exception as e:
            print(e)
            if request.user.is_authenticated:
                return redirect('login')
    return func_wrapper


@login_required
def profile(request, profile_id):
    if request.method == 'POST':
        profile_photo = request.FILES['ProfilePhoto'] if 'ProfilePhoto' in request.FILES else 0

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        bio = request.POST['bio']
        user_data = User.objects.get(id=request.user.id)
        user_data.first_name = first_name
        user_data.last_name = last_name
        user_data.username = username
        user_data.save()

        user_profile_data = UserProfile.objects.get(user=user_data)
        user_profile_data.first_name = first_name
        user_profile_data.last_name = last_name
        user_profile_data.bio = bio
        if profile_photo != 0:
            user_profile_data.picture = profile_photo
        user_profile_data.save()
        messages.success(request, 'Profile updated successfully!')

    user_info = request.user
    user_profile_data = UserProfile.objects.get(user=user_info.id)
    user_static_profile_data = UserProfile.objects.get(user=profile_id)
    return render(request, 'profile.html', {'home': False, 'user_profile_data': user_profile_data,
                                            'user': User.objects.get(id=user_info.id),
                                            'media_path': MEDIA_URL, "profile_id": profile_id,
                                            "user_static_profile_data": user_static_profile_data})


@login_required
def base(request):
    user_info = request.user
    user_profile_data = UserProfile.objects.get(user=user_info.id)
    return render(request, 'base.html', {'home': True, "user_profile_data": user_profile_data})


def myclub(request):
    user_info = request.user

    if request.method == 'POST':
        club_picture = request.FILES['club_picture'] if 'club_picture' in request.FILES else 0
        club_name = request.POST['club_name']
        club_location = request.POST['club_location']
        club_description = request.POST['club_description']
        eighteen_plus = request.POST.get('restriction', False)

        if eighteen_plus is not False:
            eighteen_plus = True

        Club.objects.filter(club_owner=user_info).delete()
        if club_picture != 0:
            user_club_data = Club(club_name=club_name, club_location=club_location,
                                  club_description=club_description,
                                  eighteen_plus=eighteen_plus,
                                  club_picture=club_picture,
                                  club_owner=user_info)
        else:
            user_club_data = Club(club_name=club_name, club_location=club_location,
                                  club_description=club_description,
                                  eighteen_plus=eighteen_plus, club_owner=user_info)
        user_club_data.save()

    post_data = Post.objects.filter(post_author=user_info).select_related('post_author', 'post_author__userprofile').order_by("-date_posted")
    post_comments = Comment.objects.select_related("post", "name", "name__userprofile")

    post_comment_temp_dict = {}
    for data in post_comments:
        if data.post.id in post_comment_temp_dict:
            post_comment_temp_dict[data.post.id].append(data)
        else:
            post_comment_temp_dict[data.post.id] = [data]

    for data in post_data:
        if data.id in post_comment_temp_dict.keys():
            data.comments_data = post_comment_temp_dict[data.id]
            data.comments_count = len(post_comment_temp_dict[data.id])
        data.likes_count = data.likes.count()
        data.self_liked = 1 if data.likes.filter(username=user_info.username).exists() else 0

    user_profile_data = UserProfile.objects.get(user=user_info.id)
    club_data = Club.objects.filter(club_owner=user_info)
    if club_data.exists():
        club_data_value = club_data[0]
        club_data = 1
    else:
        club_data_value = dict()
        club_data = 0
    context = {'home': False, "user_profile_data": user_profile_data, 'club_data': club_data,
               'club_data_value': club_data_value, "post_data": post_data}
    return render(request, 'myclub.html', context)


@login_required
def delete_clubs(request):
    user_info = request.user
    Club.objects.filter(club_owner=user_info).delete()
    return redirect('myclub')


def myposts(request):
    today = date.today()
    seven_day_before = today - timedelta(days=7)
    user_info = request.user

    if request.method == 'POST':
        post_title = request.POST["postTitle"]
        post_content = request.POST["postContent"]
        post_image = request.FILES['postImage'] if 'postImage' in request.FILES else 0

        club_data = Club.objects.get(club_owner=user_info)
        if post_image != 0:
            user_post_data = Post(post_title=post_title, txtcontent=post_content,
                                  imgcontent=post_image,
                                  club=club_data, post_author=user_info)
        else:
            user_post_data = Post(post_title=post_title, txtcontent=post_content,
                                  club=club_data, post_author=user_info)
            messages.success(request, "Posted Successfully!")
        user_post_data.save()

    seven_days_post_data = Post.objects.filter(date_posted__gte=seven_day_before, post_author=user_info).select_related('post_author', 'post_author__userprofile').order_by("-date_posted")

    post_data = Post.objects.filter(post_author=user_info).select_related('post_author', 'post_author__userprofile').order_by("-date_posted")
    post_comments = Comment.objects.select_related("post", "name", "name__userprofile")

    post_comment_temp_dict = {}
    for data in post_comments:
        if data.post.id in post_comment_temp_dict:
            post_comment_temp_dict[data.post.id].append(data)
        else:
            post_comment_temp_dict[data.post.id] = [data]

    for data in post_data:
        if data.id in post_comment_temp_dict.keys():
            data.comments_data = post_comment_temp_dict[data.id]
            data.comments_count = len(post_comment_temp_dict[data.id])
        else:
            data.comments_data = []
            data.comments_count = 0
        data.likes_count = data.likes.count()
        data.self_liked = 1 if data.likes.filter(username=user_info.username).exists() else 0

    best_post_data = hottest_post_sorting(post_data)

    for data in seven_days_post_data:
        if data.id in post_comment_temp_dict.keys():
            data.comments_data = post_comment_temp_dict[data.id]
            data.comments_count = len(post_comment_temp_dict[data.id])
        else:
            data.comments_data = []
            data.comments_count = 0

        data.likes_count = data.likes.count()
        data.self_liked = 1 if data.likes.filter(username=user_info.username).exists() else 0

    trending_post_data = trending_post_sorting(post_data)
    hottest_post_data = hottest_post_sorting(post_data)

    user_profile_data = UserProfile.objects.get(user=user_info.id)
    context = {'home': False, "user_profile_data": user_profile_data, "user": user_info, "post_data": post_data,
               "best_post_data": best_post_data,
               "hottest_post_data": hottest_post_data,
               "trending_post_data": trending_post_data}
    return render(request, 'myposts.html', context)


def delete_post(request, post_id):
    Post.objects.filter(id=post_id).delete()
    return redirect("myposts")



def recommend(request):
    return render(request, 'recommendations.html', {'home': False})
@login_required
def recommendations(request):
    print(1)
    user_info = request.user
    print(2)
    jsonDec = json.decoder.JSONDecoder()
    print(3)

    user_info = request.user
    user = UserProfile.objects.get(user=user_info.id)

    myCollectBookIds = jsonDec.decode(user.favourites)
    print("Book Collection:",myCollectBookIds)

    otherUser = UserProfile.objects.filter(~Q(user_id=user_info.id))
    otherUserIds = []
    for u in otherUser:
        otherUserIds.append(u.user.id)
    print("Other Users:",otherUserIds)
    #Users who are 30 per cent similar to themselves
    otherpercentage = []

    for otherid in otherUserIds:
        percentage = 0
        user = UserProfile.objects.get(user_id=otherid)
        books =  jsonDec.decode(user.favourites)
        for bookid in myCollectBookIds:
            if bookid in books:
                percentage = percentage + 1
       
        if len(books)>0:
            percentage = percentage / len(books)
        if percentage > 0.3:
            otherpercentage.append(otherid)
    user_profile_data = UserProfile.objects.get(user=user_info.id)

    
    resultBook = []
    #Process books from similar users to pick out those that are not already preferred by users
    for l in otherpercentage:
        us = UserProfile.objects.get(user_id=l)
        kn = jsonDec.decode(us.favourites) # (book_id__in=myCollectBookIds)
        for im in kn:
            if im not in myCollectBookIds:
                print(im)
                for bb in Book.objects.filter(isbn=im):
                    if bb not in resultBook:
                        resultBook.append(bb)
    
    print("Results:",resultBook)
    context = {'home': False, "user_profile_data": user_profile_data,'resultBook':resultBook}


    return render(request, 'recommendations.html', context)

def authors(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if Author.objects.filter(first_name=first_name, last_name=last_name).exists():
            messages.error(request, "Author name already exists!")
        else:
            Author(first_name=first_name, last_name=last_name).save()
            messages.success(request, "Author added successfully!")
    user_info = request.user
    user_profile_data = UserProfile.objects.get(user=user_info.id)
    all_authors = Author.objects.all()
    context = {'home': False, "user_profile_data": user_profile_data, "user": user_info,
               "all_authors": all_authors}
    return render(request, 'authors.html', context)


def publishers(request):
    if request.method == 'POST':
        pubisher_name = request.POST['pubisher_name']
        publisher_email = request.POST['publisher_email']
        publisher_address = request.POST['publisher_address']
        if Publisher.objects.filter(publisher_email=publisher_email).exists():
            messages.error(request, "Publisher email already exists!")
        else:
            Publisher(publisher_email=publisher_email, pubisher_name=pubisher_name,
                      publisher_address=publisher_address).save()
            messages.success(request, "Publisher added successfully!")
    user_info = request.user
    user_profile_data = UserProfile.objects.get(user=user_info.id)
    all_publishers = Publisher.objects.all()
    paginator = Paginator(all_publishers,10)
    context = {'home': False, "user_profile_data": user_profile_data, "user": user_info,
               "all_publishers": all_publishers}
    return render(request, 'publishers.html', context)


def library(request):
    if request.method == "POST":
        isbn = request.POST["isbn"]
        book_title = request.POST["book_title"]
        genre = request.POST["genre"]
        image_url = request.POST["image_url"]
        publication_date = request.POST["publication_date"]
        author = request.POST.getlist("author")
        publisher = request.POST["publisher"]

        genre_obj = Genre.objects.filter(name=genre)
        if genre_obj.exists():
            genre_obj = genre_obj[0]
        else:
            genre_obj = Genre(name=genre)
            genre_obj.save()
        filtered_authors = Author.objects.filter(author_id__in=author)
        filtered_publisher = Publisher.objects.get(Publisher_id=publisher)

        book_creation = Book(isbn=isbn, book_title=book_title, genre=genre_obj, image_url=image_url,
                             publication_date=publication_date,
                             publisher=filtered_publisher)
        book_creation.save()

        for i in filtered_authors:
            book_creation.authors.add(i)

        # filtered_authors = Author.objects.filter(author_id__in=author)
        # filtered_publisher = Publisher.objects.get(Publisher_id=publisher)

        # for i in filtered_authors:
        #     book_creation.authors.add(i)
        # book_creation.publisher = filtered_publisher
        # book_creation.save()

    user_info = request.user
    user_profile_data = UserProfile.objects.get(user=user_info.id)
    all_publishers = Publisher.objects.all()
    all_authors = Author.objects.all()
    # all_books_fetched = Book.objects.all().all()
    all_books_fetched = Book.objects.all()#[:10]
    all_books = []
    for i in all_books_fetched:
        books_authors = ""
        for author_obj in i.authors.all():
        # for author_obj in Author.objects.select_related(i):
            books_authors += author_obj.first_name + "-" + author_obj.last_name + ","
        all_books.append({'isbn': i.isbn, 'book_title': i.book_title, 'genre': i.genre,
                          'image_url': i.image_url, 'publication_date': i.publication_date,
                          'author': books_authors.strip(","), 'publisher': i.publisher})
    context = {'home': False, "user_profile_data": user_profile_data, "user": user_info,
               "all_authors": all_authors, "all_publishers": all_publishers,
               "all_books": all_books}

    return render(request, 'library.html', context)


def favourite(request):
    return render(request, 'favourite.html', {'home': False})


def homefeed(request):
    today = date.today()
    seven_day_before = today - timedelta(days=7)

    user_info = request.user
    club_found = 0
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
    if Club.objects.filter(club_owner=user_info).exists():
        club_found = 1

    seven_days_post_data = Post.objects.filter(date_posted__gte=seven_day_before).select_related('post_author', 'post_author__userprofile').order_by("-date_posted")

    post_data = Post.objects.select_related('post_author', 'post_author__userprofile').order_by("-date_posted")
    post_comments = Comment.objects.select_related("post", "name", "name__userprofile")

    post_comment_temp_dict = {}
    for data in post_comments:
        if data.post.id in post_comment_temp_dict:
            post_comment_temp_dict[data.post.id].append(data)
        else:
            post_comment_temp_dict[data.post.id] = [data]

    for data in post_data:
        if data.id in post_comment_temp_dict.keys():
            data.comments_data = post_comment_temp_dict[data.id]
            data.comments_count = len(post_comment_temp_dict[data.id])
        else:
            data.comments_data = []
            data.comments_count = 0
        data.likes_count = data.likes.count()
        data.self_liked = 1 if data.likes.filter(username=user_info.username).exists() else 0

    best_post_data = hottest_post_sorting(post_data)

    for data in seven_days_post_data:
        if data.id in post_comment_temp_dict.keys():
            data.comments_data = post_comment_temp_dict[data.id]
            data.comments_count = len(post_comment_temp_dict[data.id])
        else:
            data.comments_data = []
            data.comments_count = 0
        data.likes_count = data.likes.count()
        data.self_liked = 1 if data.likes.filter(username=user_info.username).exists() else 0

    trending_post_data = trending_post_sorting(post_data)
    hottest_post_data = hottest_post_sorting(post_data)

    user_profile_data = UserProfile.objects.get(user=user_info.id)
    context = {"user_profile_data": user_profile_data, "user": user_info, "post_data": post_data,
               "club_found": club_found, "best_post_data": best_post_data,
               "hottest_post_data": hottest_post_data,
               "trending_post_data": trending_post_data
               }
    return render(request, 'homefeed.html', context)


def checklogin(request):
    if request.user.is_authenticated:
        return redirect('base')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user_data = User.objects.filter(email=email)
            if user_data.exists():
                user = authenticate(username=user_data[0].username, password=password)
                if user is not None:
                    login(request, user)
                    # all_posts = Post.objects.all().order_by('-date_posted')
                    # for p in all_posts:
                    #     print(p.post_title)
                    # return render(request, 'base.html', {'posts': all_posts, 'home': True})  # directs to feed.
                    return redirect("base")

            messages.error(request, "User does not exist")
            return render(request, 'index.html')
        except Exception as e:
            print(e)
            pass
    else:
        return render(request, 'index.html')


def reg(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname', 0)
        last_name = request.POST.get('lastname', 0)
        username = request.POST.get('username')
        age = request.POST.get('age', 0)
        email = request.POST.get('email', 0)
        password = request.POST.get('password', 0)
        sex = request.POST.get('sex', 0)

        username_test = User.objects.filter(username=username)
        email_test = User.objects.filter(email=email)
        if username_test.exists():
            messages.error(request, "Username already Taken!")
        elif email_test.exists():
            messages.error(request, "Email already registered user another email!")
        else:
            with transaction.atomic():
                user = User(first_name=first_name, last_name=last_name, username=username, email=email)
                user.set_password(password)
                user.save()
                user_profile = UserProfile(user=user, first_name=first_name, last_name=last_name, age=age, sex=sex)
                user_profile.save()
                messages.success(request, "Congratulation user registered successfully!")

    return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('login')


def update_password(request):
    entered_current_password = request.POST['CurrentPassword']
    new_password = request.POST['NewPassword']
    confirm_password = request.POST['ConfirmPassword']
    if request.user.check_password(entered_current_password):
        if new_password == confirm_password:
            user_data = User.objects.get(id=request.user.id)
            user_data.set_password(new_password)
            user_data.save()
            messages.success(request, "Password Updated successfully!")
        else:
            messages.error(request, "New password and current password does not match !")
    else:
        messages.error(request, "Error in current password!")
    return redirect('profile')


def hottest_post_sorting(sort_list):
    sort_list = list(sort_list)

    # Sort the array in ascending order
    for i in range(0, len(sort_list)):
        for j in range(i + 1, len(sort_list)):
            if sort_list[i].likes_count > sort_list[j].likes_count:
                temp = sort_list[i]
                sort_list[i] = sort_list[j]
                sort_list[j] = temp
    return sort_list[::-1]


def trending_post_sorting(sort_list):
    sort_list = list(sort_list)

    # Sort the array in ascending order
    for i in range(0, len(sort_list)):
        for j in range(i + 1, len(sort_list)):
            if sort_list[i].comments_count > sort_list[j].comments_count:
                temp = sort_list[i]
                sort_list[i] = sort_list[j]
                sort_list[j] = temp
    return sort_list[::-1]


def favourites(request):
    checked_items = request.POST.getlist('favourite[]')
    user_info = request.user
    user = UserProfile.objects.get(user=user_info.id)
    user.favourites = json.dumps(checked_items)
    user.save()

    return None