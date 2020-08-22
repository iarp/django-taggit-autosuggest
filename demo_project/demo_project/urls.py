from django.urls import path, include

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('', include('posts.urls')),
]
