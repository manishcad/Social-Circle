from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Post, Like, Followers_Model, Chat
from itertools import chain
from django.contrib.auth.decorators import login_required
import random
# Create your views here.


@login_required(login_url="Login_page")
def home(request):
    profile = Profile.objects.filter(user=request.user).first()
    #post_list = Post.objects.all()

    user_following_list = []
    user_feed = []
    user_following = Followers_Model.objects.filter(
        user=request.user.username)

    for users in user_following:
        user_following_list.append(users.follower)

    for username in user_following_list:
        posts = Post.objects.filter(user=username)
        user_feed.append(posts)
    feeds = list(chain(*user_feed))
    # Chat Sections
    user_profile = Profile.objects.get(user=request.user)
    msgs = Chat.objects.filter(receiver=user_profile)

    # Profile.objects.get()
    # User suggestions
    new_suggestions = []
    all_users = User.objects.all()
    for user in all_users:
        if user.username not in user_following_list:
            new_suggestions.append(Profile.objects.filter(user=user))

    new_suggestions = list(chain(*new_suggestions))
    new_suggestions = [
        x for x in new_suggestions if x.user.username != request.user.username][0:5]

    random.shuffle(new_suggestions)
    context = {'profile': profile, 'post_list': feeds,
               "suggestions": new_suggestions, 'msgs': msgs}
    return render(request, "index.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(username=username, password=password)

        print(user)
        if user:
            login(request, user)
            return redirect("Home")
        else:

            messages.warning(request, "Username Or Password Is Incorrect")
            return redirect("Login_page")
    return render(request, "signin.html")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        user = User.objects.filter(username=username)
        print(username, password, password2, email)
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.warning(request, "Username is already taken")
            return redirect("Register_page")
        else:
            if password != password2:
                messages.warning(
                    request, "The Two Password Field Does Not Match")
                return redirect("Register_page")
            else:
                user = User.objects.create(
                    username=username, email=email)
                user.set_password(raw_password=password)
                user.save()

                new_profile = Profile.objects.create(user=user)
                new_profile.save()
                login(request, user)
                return redirect("Profile_settings")
    return render(request, "signup.html")


@login_required(login_url="Login_page")
def logout_page(request):
    logout(request)
    return redirect("Login_page")


@login_required(login_url="Login_page")
def profile_setting(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get("profile_image") == None:
            print("User Did nOt Upload the image")
            location = request.POST.get("location")
            profile_image = user_profile.proflie_image
            bio = request.POST.get("bio")

            user_profile.proflie_image = profile_image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get("profile_image"):
            print("user Upload the image")
            image = request.FILES.get("profile_image")

            location = request.POST.get("location")
            bio = request.POST.get("bio")
            user_profile.proflie_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect("Home")

    context = {"user_profile": user_profile}
    return render(request, "setting.html", context)


@login_required(login_url="Login_page")
def upload_post(request):
    if request.method == "POST":
        username = request.user.username
        image = request.FILES.get("post_image")
        caption = request.POST.get("caption")
        post = Post.objects.create(user=username, image=image, caption=caption)
        post.save()

    return redirect("Home")


@login_required(login_url="Login_page")
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")
    post = Post.objects.get(uid=post_id)
    like_post = Like.objects.filter(username=username, post_id=post_id).first()

    if like_post == None:
        new_like = Like.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect("Home")
    else:
        like_post.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect("Home")


@login_required(login_url="Login_page")
def profile(request, pk):
    user_obj = User.objects.get(username=pk)
    profile_obj = Profile.objects.get(user=user_obj)
    posts = Post.objects.filter(user=pk)
    len_of_posts = posts.count()

    follower = request.user.username
    user = pk

    no_of_follower = Followers_Model.objects.filter(follower=pk).count()
    no_of_following = Followers_Model.objects.filter(user=pk).count()

    if Followers_Model.objects.filter(follower=user, user=follower):
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    context = {"user_obj": user_obj, "profile_obj": profile_obj,
               'posts': posts, 'len_of_posts': len_of_posts, "button_text": button_text, "no_of_follow": no_of_follower, 'no_of_following': no_of_following}
    return render(request, "profile.html", context)


@login_required(login_url="Login_page")
def follow(request):
    if request.method == "POST":

        user = request.POST.get("user")
        follower = request.POST.get("follower")
        if Followers_Model.objects.filter(user=user, follower=follower):
            follow_obj = Followers_Model.objects.get(
                user=user, follower=follower)
            follow_obj.delete()
            return redirect(f"profile/{follower}")
        else:
            new_follow = Followers_Model.objects.create(
                user=user, follower=follower)
            return redirect(f"profile/{follower}")
    else:
        return redirect("Home")


@login_required(login_url="Login_page")
def search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        user_model = User.objects.filter(username__startswith=search)
        all_profile = []
        user_profile = Profile.objects.get(user=request.user)
        for username in user_model:
            profile = Profile.objects.get(user=username)
            all_profile.append(profile)
        context = {'all_profiles': all_profile, 'user_profile': user_profile}
        return render(request, 'search.html', context)
    else:
        return redirect("Home")


def inbox(request):
    user_profile = Profile.objects.get(user=request.user)
    msgs = Chat.objects.filter(receiver=user_profile)
    unread_msgs = Chat.objects.filter(is_read=False).count()

    context = {"msgs": msgs, "unread_msg_count": unread_msgs}
    return render(request, "inbox.html", context)


def view_msg(request, pk):
    user_obj = User.objects.get(username=pk)
    profile_obj = Profile.objects.get(user=user_obj)

    all_msg = Chat.objects.filter(sender=profile_obj)
    for msg in all_msg:
        msg.is_read = True
        msg.save()
    context = {"all_msg": all_msg}
    return render(request, "message.html", context)


def send_msg(request):
    if request.method == "POST":
        msg = request.POST.get("msg")
        receiver = request.POST.get("username")
        user_recevier = User.objects.get(username=receiver)
        user_profile_receiver = Profile.objects.get(user=user_recevier)

        sender_profile = Profile.objects.get(user=request.user)
        Chat.objects.create(sender=sender_profile,
                            receiver=user_profile_receiver, msg=msg)

    return HttpResponse("/")
