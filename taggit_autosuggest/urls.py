from django.urls import re_path

from .views import list_tags


urlpatterns = [
    re_path(r'^list/(?P<tagmodel>[\._\w]+)/$', list_tags,
            name='taggit_autosuggest-list'),
]
