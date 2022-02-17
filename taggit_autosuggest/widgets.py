import copy

from django import forms
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


try:
    from django.contrib.staticfiles.templatetags.staticfiles import static
except ImportError:
    from django.templatetags.static import static

from . import app_settings
from .utils import edit_string_for_tags


class TagAutoSuggest(forms.TextInput):
    input_type = 'text'
    tagmodel = None

    def __init__(self, tagmodel, *args, **kwargs):
        super(TagAutoSuggest, self).__init__(*args, **kwargs)
        self.tagmodel = tagmodel

    def render(self, name, value, attrs=None, renderer=None, *args, **kwargs):
        if hasattr(value, "select_related"):
            tags = [o.tag for o in value.select_related("tag")]
            value = edit_string_for_tags(tags)
        elif value is not None and not isinstance(value, str):
            value = edit_string_for_tags(value)

        autosuggest_url = reverse('taggit_autosuggest-list', kwargs={
            'tagmodel': self.tagmodel
        })

        result_attrs = copy.copy(attrs) if attrs else {}
        initial_input_type, self.input_type = self.input_type, 'hidden'
        result_html = super(TagAutoSuggest, self).render(
            name, value, result_attrs, renderer
        )
        self.input_type = initial_input_type

        widget_attrs = copy.copy(attrs) if attrs else {}
        widget_attrs['id'] += '__tagautosuggest'
        widget_html = super(TagAutoSuggest, self).render(
            name, value, widget_attrs, renderer
        )

        js = u"""
            <script type="text/javascript">
            (function ($) {
                var tags_as_string;

                String.prototype.toProperCase = function () {
                    return this.replace(/\w\S*/g, function(txt) {
                        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                    });
                };

                Array.prototype.toUnique = function() {
                    var dict = {},
                        arrayLength = this.length,
                        elem,
                        i,
                        key,
                        uniqueArray = [];
                    for (i = 0; i < arrayLength; i++) {
                        elem = this[i];
                        dict[elem] = elem;
                    }
                    for (key in dict) {
                        uniqueArray.push(key);
                    }
                    return uniqueArray;
                };

                $(document).ready(function (){
                    tags_as_string = $('#%(result_id)s').val();

                    /* Be sure to instantiate it a single time */
                    if (typeof($("#as-selections-" + "%(widget_id)s").get(0)) === 'undefined') {
                        $("#%(widget_id)s").autoSuggest("%(url)s", {
                            asHtmlID: "%(widget_id)s",
                            startText: "%(start_text)s",
                            emptyText: "%(empty_text)s",
                            limitText: "%(limit_text)s",
                            preFill: tags_as_string,
                            queryParam: 'q',
                            retrieveLimit: %(retrieve_limit)d,
                            minChars: 1,
                            neverSubmit: true
                        });
                    }

                    $('.as-selections').addClass('vTextField');
                    $('ul.as-selections li.as-original input').addClass('vTextField');

                    $('#%(result_id)s').parents().find('form').submit(function (){
                        tags_as_string = $("#as-values-%(widget_id)s").val();
                        $("#%(widget_id)s").remove();
                        $("#%(result_id)s").val(tags_as_string);
                    });
                });
            })(django.jQuery);
            </script>""" % {  # noqa
                'result_id': result_attrs['id'],
                'widget_id': widget_attrs['id'],
                'url': autosuggest_url,
                'start_text': _("Enter Tag Here"),
                'empty_text': _("No Results"),
                'limit_text': _('No More Selections Are Allowed'),
                'retrieve_limit': app_settings.MAX_SUGGESTIONS,
            }
        return result_html + widget_html + mark_safe(js)

    class Media:
        css = {
            'all': (
                static('jquery-autosuggest/css/{}'.format(
                    app_settings.CSS_FILENAME
                )),
            )
        }
        js = (
            static('admin/js/jquery.init.js'),
            static('jquery-autosuggest/js/jquery.autoSuggest.minified.js'),
        )
