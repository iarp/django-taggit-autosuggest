from django import VERSION
from django.utils.text import capfirst

from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager
from taggit_autosuggest.widgets import TagAutoSuggest


def _model_name(model):
    """
    The meta.module_name property got deprecated in favor of meta.model_name.
    """
    if VERSION < (1, 7):
        return model._meta.module_name
    else:
        return model._meta.model_name


class TaggableManager(BaseTaggableManager):

    def formfield(self, form_class=TagField, **kwargs):
        tagmodel = "%s.%s" % (self.rel.to._meta.app_label,
                              _model_name(self.rel.to))
        defaults = {
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "required": not self.blank,
            "widget": TagAutoSuggest(tagmodel=tagmodel),
        }
        defaults.update(kwargs)
        return form_class(**defaults)
