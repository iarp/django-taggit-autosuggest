class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(settings,
                         'TAGGIT_AUTOSUGGEST_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, dflt))
        return getter(self.prefix + name, dflt)

    @property
    def CSS_FILENAME(self):
        return self._setting('CSS_FILENAME', 'autoSuggest.css')

    @property
    def MAX_SUGGESTIONS(self):
        return self._setting('MAX_SUGGESTIONS', 20)

    @property
    def TAG_MODELS(self):
        TAG_MODELS = self._setting('MODELS', None)
        if not TAG_MODELS or not isinstance(TAG_MODELS, list):
            TAG_MODELS = []
        return TAG_MODELS

    @property
    def OPERAND(self):
        return self._setting('OPERAND', '__icontains')


# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys  # noqa


app_settings = AppSettings('TAGGIT_AUTOSUGGEST_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
