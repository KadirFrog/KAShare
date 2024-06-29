import json
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.dateformat import DateFormat
from django.views.decorators.http import require_POST

from main.forms import PostForm, CustomRegisterForm, CustomAuthenticationForm, ClassTestForm
from main.models import Post, ClassTest


def signup_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
            return render(request, 'signup.html', {'form': form, "errors": form.errors})
    else:
        form = CustomRegisterForm()
        return render(request, 'signup.html', {'form': form, "errors": None})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form, "errors": form.errors, "logout": False})
@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post1 = form.save(commit=False)
            post1.author = request.user
            post1.save()
            return redirect('profile')
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form, "errors": form.errors})

@login_required
def profile(request):
    device: str = request.META.get('HTTP_USER_AGENT', '').lower()
    user = request.user
    return render(request, "profile.html", {"device": device, "user": user})

def logout_view(request):
    logout(request)
    return redirect('login', {"logout": True})


@login_required
def recent_posts(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'recent_posts.html', {'posts': posts, 'user': request.user})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.like_post(request.user)
    return redirect('recent_posts')

@login_required
def home(request):
    events = ClassTest.objects.all()
    formatted_events = [
        {"event_date": DateFormat(event.test_date).format('Y-m-d'), "event_title": event.test_name}
        for event in events
    ]
    form = ClassTestForm()
    return render(request, 'home.html', {"events": json.dumps(formatted_events), "form": form})

@login_required
@require_POST
def create_classtest(request):
    form = ClassTestForm(request.POST)
    if form.is_valid():
        classtest = form.save(commit=False)
        classtest.related_class_id = request.user.id
        classtest.save()
    return redirect('home')

