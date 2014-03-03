import copy

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from taggit_autosuggest.utils import edit_string_for_tags


MAX_SUGGESTIONS = getattr(settings, 'TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS', 20)


class TagAutoSuggest(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            tags = [o.tag for o in value.select_related("tag")]
            value = edit_string_for_tags(tags)

        result_attrs = copy.copy(attrs)
        result_attrs['type'] = 'hidden'
        result_html = super(TagAutoSuggest, self).render(name, value,
            result_attrs)

        widget_attrs = copy.copy(attrs)
        widget_attrs['id'] += '__tagautosuggest'
        widget_html = super(TagAutoSuggest, self).render(name, value,
            widget_attrs)

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

                    $('.as-selections').addClass('vTextField');
                    $('ul.as-selections li.as-original input').addClass('vTextField');

                    $('#%(result_id)s').parents().find('form').submit(function (){
                        tags_as_string = $("#as-values-%(widget_id)s").val()
                            .split(',')
                            .filter(function(v) { return Boolean(v); })
                            .map(function(v) { return $.trim(v); })
                            .map(function(v) { return v.toProperCase(); })
                            .toUnique()
                            .sort()
                            .join(', ');
                        $("#%(widget_id)s").remove();
                        $("#%(result_id)s").val(tags_as_string);
                    });
                });
            })(django.jQuery);
            </script>""" % {
                'result_id': result_attrs['id'],
                'widget_id': widget_attrs['id'],
                'url': reverse('taggit_autosuggest-list'),
                'start_text': _("Enter Tag Here"),
                'empty_text': _("No Results"),
                'limit_text': _('No More Selections Are Allowed'),
                'retrieve_limit': MAX_SUGGESTIONS,
            }
        return result_html + widget_html + mark_safe(js)

    class Media:
        css_filename = getattr(settings, 'TAGGIT_AUTOSUGGEST_CSS_FILENAME',
            'autoSuggest.css')
        js_base_url = getattr(settings, 'TAGGIT_AUTOSUGGEST_STATIC_BASE_URL',
            '%sjquery-autosuggest' % settings.STATIC_URL)
        css = {
            'all': ('%s/css/%s' % (js_base_url, css_filename),)
        }
        js = (
            '%s/js/jquery.autoSuggest.minified.js' % js_base_url,
        )
