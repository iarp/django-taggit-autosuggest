from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson as json
from django.db.models.loading import get_model

MAX_SUGGESTIONS = getattr(settings, 'TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS', 20)

# define the default models for tags and tagged items
TAG_MODELS = getattr(settings, 'TAGGIT_AUTOSUGGEST_MODELS', {'default': ('taggit', 'Tag')})
if not type(TAG_MODELS) == dict:
    TAG_MODELS = {'default': TAG_MODELS}


def list_tags(request, tagmodel=None):
    """
    Returns a list of JSON objects with a `name` and a `value` property that
    all start like your query string `q` (not case sensitive).
    """
    if not tagmodel or tagmodel not in TAG_MODELS:
        TAG_MODEL = get_model(*TAG_MODELS['default'])
    else:
        TAG_MODEL = get_model(*TAG_MODELS[tagmodel])
        
    query = request.GET.get('q', '')
    limit = request.GET.get('limit', MAX_SUGGESTIONS)
    try:
        request.GET.get('limit', MAX_SUGGESTIONS)
        limit = min(int(limit), MAX_SUGGESTIONS)  # max or less
    except ValueError:
        limit = MAX_SUGGESTIONS

    tag_name_qs = TAG_MODEL.objects.filter(name__icontains=query).\
        values_list('name', flat=True)
    data = [{'name': n, 'value': n} for n in tag_name_qs[:limit]]

    return HttpResponse(json.dumps(data), mimetype='application/json')
