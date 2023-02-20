import datetime
import re
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    categories = Category.objects.all()
    post = Post.objects.all()[:3]
    context = {
        'categories': categories,
        'posts': post,
    }
    return render(request, "index.html", context)


def category(request, slug):
    categories = Category.objects.all()
    post = Post.objects.filter(category__slug=slug)
    context = {
        'post': post,
        'categories': categories
    }

    return render(request, "category.html", context)


def seepost(request):
    categories = Category.objects.all()
    post_slug = request.GET.get("post_slug")

    if post_slug == None:
        post = Post.objects.all()
    else:
        post = Post.objects.get(slug=post_slug)
    context = {
        'post': post,
        'categories': categories
    }
    return render(request, "seepost.html", context)


def viewallpost(request):
    categories = Category.objects.all()
    post = Post.objects.all()
    context = {
        'posts': post,
        'categories': categories
    }

    return render(request, "viewallpost.html", context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, "signin.html", context)
    return render(request, "signin.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        emailRegex = r'/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/'
        passRegex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

        if username == '':
            messages.warning(request, "Please enter username")
            return redirect("signup")
        elif username == request.user:
            messages.warning(request, "User name already exist")
            return redirect("signup")
        elif fname == "":
            messages.warning(request, "Please enter first name")
            return redirect("signup")
        elif lname == "":
            messages.warning(request, "Please enter last name")
            return redirect("signup")
        elif email == "":
            messages.warning(request, "Please enter email")
            return redirect("signup")

        elif re.fullmatch(emailRegex, email):
            messages.warning(request, "Please enter a valid email")
            return redirect("signup")
        elif password == "":
            messages.warning(request, "Please enter password")
            return redirect("signup")

        elif re.fullmatch(passRegex, password):
            messages.warning(request, "Minimum eight characters, at least one letter, one number and one special character!")
            return redirect("signup")

        elif password2 == "":
            messages.warning(request, "Please enter confirm password")
            return redirect("signup")

        elif password2 != password:
            messages.warning(request, "Both passwords must be same")
            return redirect("signup")

        create_user = User.objects.create_user(username, email, password)
        create_user.first_name = fname
        create_user.last_name = lname
        create_user.save()
        return redirect("/signin")
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, "signup.html", context)


def signout(request):
    logout(request)
    return redirect('/signin')


# User Profile

def dashboard(request):
    if request.user:
        show_posts = Post.objects.filter(creator=request.user)
    else:
        show_posts = None
    categories = Category.objects.all()

    # check if request.user == profile.user
    # show profile.name
    profile_name = ProfileName.objects.all()

    if len(profile_name) > 1:
        # messages.warning(request, "SUCCESS")
        profile_name = ProfileName.objects.all()[:1]

    context = {
        'show_posts': show_posts,
        'categories': categories,
        'profile_name': profile_name
    }
    return render(request, "userprofile/dashboard.html", context)


def addblog(request):
    if request.user.is_anonymous:
        messages.warning(request, "Sign in or Sign up to make bolgs")
        return redirect("signin")
    else:
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            image = request.FILES.get("image")
            video = request.FILES.get("video")
            category = request.POST.get("category")
            loggedInUser = request.user
            messages.success(request, "Post successfully Submit!")
            if category == "none":
                category = None
            else:
                category = Category.objects.get(id=category)
            create_blog = Post(
                title=title,
                description=description,
                image=image,
                video=video,
                creator=loggedInUser,
                category=category,
                created_at=datetime.datetime.now()
            )
            create_blog.save()
            return redirect("addblog")
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, "userprofile/addblog.html", context)


def update_blog(request, slug):
    post = Post.objects.get(slug=slug)

    categories = Category.objects.all()
    context = {
        'post': post,
        'categories': categories
    }
    return render(request, "userprofile/update_blog.html", context)


def updated_blog_fields(request, id):
    title = request.POST.get("title")
    description = request.POST.get("description")
    image = request.FILES.get("image")
    video = request.FILES.get("video")
    category = request.POST.get("category")
    create_blog = Post.objects.get(id=id)
    if category != "none":
        cate = Category.objects.get(id=3)
    else:
        cate = None

    create_blog.title = title
    create_blog.description = description
    create_blog.image = image
    create_blog.video = video
    create_blog.category = cate
    create_blog.created_at = datetime.datetime.now()
    create_blog.save()
    return redirect("dashboard")


def deleteBlog(request, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return redirect("dashboard")


def readmore(request, slug):
    categories = Category.objects.all()
    post = Post.objects.get(slug=slug)
    context = {
        'post': post,
        'categories': categories
    }
    return render(request, "userprofile/readmore.html", context)


def usercategory(request, slug):
    # posts = Post.objects.filter(category__slug=slug)
    if request.user:
        show_posts = Post.objects.filter(creator=request.user, category__slug=slug)
    else:
        show_posts = None
    categories = Category.objects.all()
    context = {
        'show_posts': show_posts,
        'categories': categories
    }
    return render(request, 'userprofile/usercategory.html', context)


def profile(request):
    if request.method == "POST":
        profile_name = request.POST.get("profile_name")
        profile_username = request.POST.get("profile_username")
        if request.user:
            user = request.user
        messages.success(request, "Updated Profile Name!")
        if profile_name == "":
            messages.warning(request, "Please enter a name!")
        new_profile_name = ProfileName(
            profile_name=profile_name,
            username=profile_username,
            created_at=datetime.datetime.now()
        )
        new_profile_name.save()
        return redirect("profile")
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "userprofile/profile.html", context)
