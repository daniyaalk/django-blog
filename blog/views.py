from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        ListView,
        CreateView,
        DetailView,
        UpdateView,
        DeleteView
    )

from .models import Post, Comment
from .forms import CommentForm

# Create your views here.
class PostsListView(ListView):
    template_name = "blog/home.html"
    context_object_name = 'posts'
    model = Post
    ordering = "-date_posted"

class UserPostsView(ListView):
    template_name = "blog/user.html"
    context_object_name = "posts"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs['username'])
        # print(context['user'])
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.get_object()
            form.save()
            return redirect(form.instance)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()
        comments = post.comment_set.all()
        context['comments'] = comments

        context['c_form'] = CommentForm

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.info(request, "Your post has been deleted successfully!")
        return super().delete(request, *args, **kwargs)

def comments(request):
    return render(request, "blog/comments.html", {"comments": Comment.objects.all()})

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/home.html', context)