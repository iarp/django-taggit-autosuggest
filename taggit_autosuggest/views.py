from django.apps import apps
from django.http import JsonResponse

from . import app_settings


def list_tags(request, tagmodel):
    """
    Returns a list of JSON objects with a `name` and a `value` property that
    all start like your query string `q` (not case sensitive).
    """
    if not tagmodel or (app_settings.TAG_MODELS and
                        tagmodel not in app_settings.TAG_MODELS):
        raise LookupError('Invalid lookup model')
    else:
        TAG_MODEL = apps.get_model(tagmodel)

    query = request.GET.get('q')

    if not query:
        return JsonResponse({})

    limit = request.GET.get('limit')
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = app_settings.MAX_SUGGESTIONS

    queryset_func = getattr(TAG_MODEL, 'taggit_autosuggest_queryset', None)
    if callable(queryset_func):
        tag_name_qs = queryset_func(request=request, query=query)
    else:

        field = request.GET.get('f', 'name')
        query = {'{}{}'.format(field, app_settings.OPERAND): query}

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
