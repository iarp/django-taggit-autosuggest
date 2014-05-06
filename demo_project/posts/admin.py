from django.contrib import admin

from posts.models import Note
from posts.models import Post


class NoteInline(admin.TabularInline):
    model = Note


class PostAdmin(admin.ModelAdmin):
    inlines = [
        NoteInline,
    ]


admin.site.register(Post, PostAdmin)
