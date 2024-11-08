from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostCreateForm, PostEditForm


class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'all-posts.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'show-post.html', {'post': post})


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostCreateForm()
        return render(request, 'create-post.html', {'form': form})

    def post(self, request):
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-list')
        return render(request, 'create-post.html', {'form': form})


class PostEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostEditForm(instance=post)
        return render(request, 'edit-post.html', {'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-list')
        return render(request, 'edit-post.html', {'form': form})
