from django.db import models
from taggit_autosuggest.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=60)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.title


class Note(models.Model):
    text = models.TextField()
    post = models.ForeignKey('Post')
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.text
