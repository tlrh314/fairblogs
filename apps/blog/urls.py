from django.conf.urls import url

from .views import index
from .views import submit
from .views import post_detail

urlpatterns = [
    url(r'^submit/$', submit, name='submit'),
    url(r'^/post/(?P<slug>.*)', post_detail, name='post_detail'),
    url(r'^/(?P<tag>.*)', index, name='index'),
    url(r'^index/$', index, name='index'),
    url(r'^$', index, name='index'),
]
