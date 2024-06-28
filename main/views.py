from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.forms import PostForm, CustomRegisterForm, CustomAuthenticationForm


def signup_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomRegisterForm()
        return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})
@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('success_url')
    else:
        form = PostForm()
    return render(request, 'main/post.html')

@login_required
def profile(request):
    device: str = request.META.get('HTTP_USER_AGENT', '').lower()
    user = request.user
    return render(request, "profile.html", {"device": device, "user": user})