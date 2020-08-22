from django.apps import apps
from django.conf import settings
from django.http import JsonResponse


MAX_SUGGESTIONS = getattr(settings, 'TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS', 20)

# define the default models for tags and tagged items
TAG_MODELS = getattr(settings, 'TAGGIT_AUTOSUGGEST_MODELS', None)
if not isinstance(TAG_MODELS, dict):
    # TAG_MODELS = {
    #     'default': ('taggit', 'Tag'),
    # }
    TAG_MODELS = None


def list_tags(request, tagmodel=None):
    """
    Returns a list of JSON objects with a `name` and a `value` property that
    all start like your query string `q` (not case sensitive).
    """
    if not tagmodel or (TAG_MODELS and tagmodel not in TAG_MODELS):
        TAG_MODEL = apps.get_model('taggit.Tag')
    else:
        TAG_MODEL = apps.get_model(tagmodel)

    query = request.GET.get('q', '')
    limit = request.GET.get('limit', MAX_SUGGESTIONS)
    try:
        request.GET.get('limit', MAX_SUGGESTIONS)
        limit = min(int(limit), MAX_SUGGESTIONS)  # max or less
    except ValueError:
        limit = MAX_SUGGESTIONS

    field = request.GET.get('f', 'name')
    query = {'{}__icontains'.format(field): query}

    tag_name_qs = TAG_MODEL.objects.filter(
        **query
    ).values_list(field, flat=True)

    if callable(getattr(TAG_MODEL, 'request_filter', None)):
        tag_name_qs = tag_name_qs.filter(
            TAG_MODEL.request_filter(request)
        ).distinct()

    data = [{'name': n, 'value': n} for n in tag_name_qs[:limit]]

    return JsonResponse(data, safe=False)
