from django.apps import apps
from django.http import JsonResponse

from .app_settings import MAX_SUGGESTIONS, TAG_MODELS


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

    queryset_func = getattr(TAG_MODEL, 'taggit_autosuggest_queryset', None)
    if callable(queryset_func):
        tag_name_qs = queryset_func(request=request, query=query)
    else:

        field = request.GET.get('f', 'name')
        query = {'{}__icontains'.format(field): query}

        tag_name_qs = TAG_MODEL.objects.filter(
            **query
        ).values_list(field, flat=True)

    data = []
    for item in tag_name_qs[:limit]:

        # in case someone forgets values_list, obtain the first field.
        if isinstance(item, tuple):
            item = item[0]
        data.append({
            'name': item,
            'value': item,
        })

    return JsonResponse(data, safe=False)
