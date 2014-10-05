from django.utils.text import capfirst

from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager
from taggit_autosuggest.widgets import TagAutoSuggest


class TaggableManager(BaseTaggableManager):

    def formfield(self, form_class=TagField, **kwargs):
        tagmodel = "%s.%s" % (self.rel.to._meta.app_label, self.rel.to._meta.module_name)
        defaults = {
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "required": not self.blank,
            "widget": TagAutoSuggest(tagmodel=tagmodel),
        }
        defaults.update(kwargs)
        return form_class(**defaults)
