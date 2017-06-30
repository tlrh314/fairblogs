from django.conf.urls import url

from .views import index
from .views import submit
from .views import post_detail
from .views import update_post_counter


urlpatterns = [
    url(r'^submit/$', submit, name='submit'),
    url(r'^post/(?P<slug>.*)', post_detail, name='post_detail'),
    url(r'^viewpost/(?P<slug>.*)', update_post_counter, name='update_post_counter'),
    url(r'^/(?P<tag>.*)', index, name='index'),
    url(r'^index/$', index, name='index'),
    url(r'^$', index, name='index'),
]
