from django.conf.urls import patterns, include, url
from views import PromoCodeView

urlpatterns = patterns('',
    url(r'^$', PromoCodeView.as_view(), name='promoview'),
)
