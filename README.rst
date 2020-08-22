=========================
django-taggit-autosuggest
=========================

Disclaimer: The original project this repo is based on (see Fabian Topfstedt in credits)
is unmaintained since they no longer use it anymore.

Installation
============

Install from repo::

    pip install -e git+https://github.com/iarp/django-taggit-autosuggest.git#egg=django-taggit-autosuggest

settings.py::

    INSTALLED_APPS = [
        ...
        'taggit_autosuggest',
        ...
    ]

urls.py::

    urlpatterns = [
        ...
        path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
        ...
    ]

Be sure to run `python manage.py collectstatic` when deploying

Settings
========

TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS (=20)
  The number of suggestions to return when searching.

TAGGIT_AUTOSUGGEST_CSS_FILENAME (='autoSuggest.css'):
  Set the CSS file which best fits your site elements.
  The CSS file have to be in ``jquery-autosuggest/css/``.

TAGGIT_AUTOSUGGEST_MODELS (=None)
  If you do not supply this then any model can be searched.
  A column with the name of "name" is required.

  If you wish to restrict which models can be searched then use the following
  example on the basis of having an app named photos and a model named People which are tags::

    TAGGIT_AUTOSUGGEST_MODELS = [
        'taggit.Tag',  # Ensure default Tag model is there just in case.
        'photos.People',
    ]


Usage
=====

To enable autosuggesting Tags, just let the tagged model use TaggableManager::

    from django.db import models
    from taggit_autosuggest.managers import TaggableManager

    class SomeModel(models.Model):
        tags = TaggableManager()

To use autosuggesting Tags on your own pages ensure that the 
static files are added to the template's head

- You must include jquery above the following
- add ``{{ form.media }}``
- OR hardcode using the following in your templates
    - ``<link href="{% static 'jquery-autosuggest/css/autoSuggest-upshot.css' %}" rel="stylesheet"/>``
    - ``<script src="{% static 'admin/js/jquery.init.js' %}"></script>``
    - ``<script src="{% static 'jquery-autosuggest/js/jquery.autoSuggest.minified.js' %}"></script>``

Custom Query
------------

If Taggit custom tagging is used the autosuggested Tags can be filtered by
attributes of the request object after the name filtering. To enable this
the custom tag model should have a function called taggit_autosuggest_queryset which
takes a request object and returns a queryset e.g.::

    from django.db import models

    class MyTag(TagBase):

        @classmethod
        def taggit_autosuggest_queryset(cls, request, query):
            return cls.objects.filter(
                name__icontains=query
            ).values_list('name', flat=True)

Demo
====

There's a demo project using Grappelli bundled, you can run it and browse
/admin/ using the username 'demo' and password 'demo'.

Credits
=======

This project is directly based on those projects:

- Alex Gaynor, https://github.com/alex/django-taggit
- Ludwik Trammer, http://code.google.com/p/django-tagging-autocomplete/
- Jeremy Epstein, https://github.com/Jaza/django-taggit-autocomplete
- Flavio Curella, https://github.com/fcurella/django-taggit-autocomplete
- Drew Wilson, http://code.drewwilson.com/entry/autosuggest-jquery-plugin
- Fabian Topfstedt, https://bitbucket.org/fabian/django-taggit-autosuggest/
