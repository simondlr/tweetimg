from django.conf.urls import patterns, include, url
import os

from app import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'texttotwitterimg.views.home', name='home'),
    url(r'^/?$',views.index),
    # url(r'^texttotwitterimg/', include('texttotwitterimg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

#locally, let django serve static files.
ENV = os.environ.get('ENV',None)
if ENV == None: 
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
