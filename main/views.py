from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.forms import PostForm, CustomRegisterForm, CustomAuthenticationForm


def signup_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        print(request.POST)  # Add this line
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
    return render(request, 'login.html', {'form': form, "errors": form.errors})
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
    return redirect('login')
