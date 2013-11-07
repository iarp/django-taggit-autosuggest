try:
    from django.conf.urls import *
except ImportError:
    from django.conf.urls.defaults import *


urlpatterns = patterns('taggit_autosuggest.views',
    url(r'^list/$', 'list_tags', name='taggit_autosuggest-list'),
)
