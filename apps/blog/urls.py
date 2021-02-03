from django.urls import path

from blog.views import (
    PostsFeed,
    TagAutocomplete,
    change_post,
    index,
    post_detail,
    select_post,
    submit,
    update_post_counter,
)

app_name = "blogs"
urlpatterns = [
    path("submit/", submit, name="submit"),
    path("post/<slug>", post_detail, name="post_detail"),
    path("viewpost/<slug>", update_post_counter, name="update_post_counter"),
    path("<tag>", index, name="index"),
    path("select_post/", select_post, name="select_post"),
    path("change_post/<slug>", change_post, name="change_post"),
    path("tag-autocomplete/", TagAutocomplete.as_view(), name="tag-autocomplete"),
    path("index/", index, name="index"),
    path("", index, name="index"),
    # feed posts
    path("feeds/posts/", PostsFeed(), name="posts"),
]
