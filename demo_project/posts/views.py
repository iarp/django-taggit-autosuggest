from django.views.generic import ListView, UpdateView

from .models import Post


class PostListView(ListView):
    model = Post


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'tags', 'people']
