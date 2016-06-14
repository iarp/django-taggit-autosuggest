from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
]
