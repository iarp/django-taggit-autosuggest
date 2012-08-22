from django.db import models
from taggit_autosuggest.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=60)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title
