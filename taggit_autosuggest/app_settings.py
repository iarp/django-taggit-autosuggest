from django.conf import settings


def _get_setting(name, dflt=None):
    return getattr(settings, 'TAGGIT_AUTOSUGGEST_{}'.format(name), dflt)


CSS_FILENAME = _get_setting('CSS_FILENAME', 'autoSuggest.css')

MAX_SUGGESTIONS = _get_setting('MAX_SUGGESTIONS', 20)

TAG_MODELS = _get_setting('MODELS')
if not TAG_MODELS or not isinstance(TAG_MODELS, list):
    TAG_MODELS = []
