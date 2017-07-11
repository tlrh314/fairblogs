from django.conf.urls import url

from .views import index
from .views import submit
from .views import post_detail
from .views import select_post
from .views import change_post
from .views import update_post_counter


urlpatterns = [
    url(r'^submit/$', submit, name='submit'),
    url(r'^post/(?P<slug>.*)', post_detail, name='post_detail'),
    url(r'^viewpost/(?P<slug>.*)', update_post_counter, name='update_post_counter'),
    url(r'^/(?P<tag>.*)', index, name='index'),
    url(r'^select_post/$', select_post, name='select_post'),
    url(r'^change_post/(?P<slug>.*)', change_post, name='change_post'),
    url(r'^index/$', index, name='index'),
    url(r'^$', index, name='index'),
]
