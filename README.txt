Disclaimer: This project is unmaintained since I don't use it myself anymore
and I did not find a maintainer within the user base so far.
However, I'm happy to accept pull requests!


*** Credits ***
    This project is directly based on those projects:
    * Alex Gaynor, https://github.com/alex/django-taggit
    * Ludwik Trammer, http://code.google.com/p/django-tagging-autocomplete/
    * Jeremy Epstein, https://github.com/Jaza/django-taggit-autocomplete
    * Flavio Curella, https://github.com/fcurella/django-taggit-autocomplete
    * Drew Wilson, http://code.drewwilson.com/entry/autosuggest-jquery-plugin

*** Installation ***
   * Add "taggit_autosuggest" to your INSTALLED_APPS in your project settings
   * Run "python manage.py collectstatic" in your django site dir.
   * Add the following line to your project's urls.py file:
         (r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),


*** Settings ***
    TAGGIT_AUTOSUGGEST_STATIC_BASE_URL:
        Instead of collecting and serving the static files directly, you can
        also set this variable to your static base URL somewhere else.
    TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS (Defaults to 20):
        The amount of suggestions is limited, you can raise or lower the limit
        of default 20 using this setting.
    TAGGIT_AUTOSUGGEST_CSS_FILENAME (Defaults to 'autoSuggest.css'):
        Set the CSS file which best fits your site elements.
            The CSS file have to be in 'jquery-autosuggest/css/'.
    TAGGIT_AUTOSUGGEST_MODELS (Defaults to tuple('taggit','Tag'))
        The Tag model used, if you happen to use Taggit custom tagging.

*** Usage ***
To enable autosuggesting Tags, just let the tagged model use TaggableManager:

    from django.db import models
    from taggit_autosuggest.managers import TaggableManager


    class SomeModel(models.Model):

        tags = TaggableManager()

To use autosuggesting Tags outside of Django Admin pages ensure that the static
files are added to the template's <head>, either hardcoded, e.g.

    <link href="{{ STATIC_URL }}jquery-autosuggest/css/autoSuggest-upshot.css"
        type="text/css" media="all" rel="stylesheet" />
    <script type="text/javascript"
        src="{{ STATIC_URL }}jquery-autosuggest/js/jquery.autoSuggest.minified.js">
        </script>

or by adding the form/formset's media attribute to the template's context
(this is what happens in Django Admin), e.g.

    # In the view:
    context.update({'media': form.media})  # or however you add to the context

    # In the template:
    {{ media }}

(Either way, of course, the template must also include a jQuery library.)

If Taggit custom tagging is used the autosuggested Tags can be filtered by
attributes of the request object after the name filtering. To enable this
the custom tag model should have a function called request_filter which
takes a request object and returns a django.db.models.Q object, e.g.

    from django.db import models

    class MyTag(TagBase):

        @staticmethod
        def request_filter(request):

            return models.Q(...)

There's a demo project using Grappelli bundled, you can run it and browse
/admin/ using the username 'demo' and password 'demo'.
