from django.utils.text import capfirst

from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager
from taggit_autosuggest.widgets import TagAutoSuggest
from .utils import get_model_name


class TaggableManager(BaseTaggableManager):

    def formfield(self, form_class=TagField, **kwargs):
        if hasattr(self, 'rel'): # Django < 1.9
            related_model = self.rel.to
        else: # Django >= 1.9
            related_model = self.remote_field.model
        tagmodel = ".".join([related_model._meta.app_label,
                            get_model_name(related_model)])
        defaults = {
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "required": not self.blank,
            "widget": TagAutoSuggest(tagmodel=tagmodel),
        }
        defaults.update(kwargs)
        return form_class(**defaults)
