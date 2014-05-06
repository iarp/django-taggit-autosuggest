from django.contrib import admin

from models import Note
from models import Post


class NoteInline(admin.TabularInline):
    model = Note


class PostAdmin(admin.ModelAdmin):
    inlines = [
        NoteInline,
    ]


admin.site.register(Post, PostAdmin)
