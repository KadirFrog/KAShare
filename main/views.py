import json
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.dateformat import DateFormat
from django.views.decorators.http import require_POST

from main.forms import PostForm, CustomRegisterForm, CustomAuthenticationForm, ClassTestForm, ImageFormSet
from main.models import Post, ClassTest, Image


def signup_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
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
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form, "errors": form.errors, "logout": False})
@login_required
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():  # Validate the formset here
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for image_form in formset:
                if image_form.cleaned_data.get('image'):  # Now you can safely access cleaned_data
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('post_detail', post.id)
    else:
        form = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'post.html', {'form': form, 'formset': formset})

@login_required
def profile(request):
    device: str = request.META.get('HTTP_USER_AGENT', '').lower()
    user = request.user
    return render(request, "profile.html", {"device": device, "user": user})

def logout_view(request):
    logout(request)
    url = reverse('login')
    response = HttpResponseRedirect(url)
    response.set_cookie('logout', 'True')
    return response


@login_required
def recent_posts(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'recent_posts.html', {'posts': posts, 'user': request.user})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    images = post.images.all()  # Retrieve all images related to the post
    return render(request, 'post_detail.html', {'post': post, 'images': images})

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

