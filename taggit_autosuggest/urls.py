from django.conf.urls import url

from .views import list_tags


urlpatterns = [
    url(r'^list/$', list_tags, name='taggit_autosuggest-list'),
    url(r'^list/(?P<tagmodel>[\._\w]+)/$', list_tags,
        name='taggit_autosuggest-list'),
]
