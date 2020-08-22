from django.db import models
from django.shortcuts import reverse

from taggit_autosuggest.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=60)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:update', args=[self.pk])


class Note(models.Model):
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
