from django.db import models
from django.shortcuts import reverse

from taggit.models import TagBase, TaggedItemBase
from taggit_autosuggest.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=60)
    tags = TaggableManager(blank=True)
    people = TaggableManager(
        blank=True,
        through='TaggedPeople',
        verbose_name='People',
        related_name='post_people',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:update', args=[self.pk])


class Note(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)


class People(TagBase):
    pass


class TaggedPeople(TaggedItemBase):
    content_object = models.ForeignKey(Post, on_delete=models.CASCADE)

    tag = models.ForeignKey(
        People,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
