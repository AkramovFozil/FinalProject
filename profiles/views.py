from django.shortcuts import render, redirect
from .models import UserProfile, Post
from django.contrib.auth.models import User
from .forms import UserProfileForm


def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    posts = Post.objects.filter(author=user)
    return render(request, 'profiles/user-profile.html', {'profile': profile, 'posts': posts})


def edit_profile(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profiles/edit-profile.html', {'form': form})


def my_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    posts = Post.objects.filter(author=user)
    return render(request, 'profiles/my-profile.html', {'profile': profile, 'posts': posts})
