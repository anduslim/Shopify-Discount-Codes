from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shopifyHack.views.home', name='home'),
    # url(r'^shopifyHack/', include('shopifyHack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

        #  URLS FOR ADMIN_PAGES
    # -----------------------------
    url(r'^promo/', include('shopifypromo.urls')), 
)
