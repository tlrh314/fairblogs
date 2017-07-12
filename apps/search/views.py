from __future__ import unicode_literals, absolute_import, division

import re

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render

from .forms import SearchForm
from ..myuser.models import Blogger
from ..myuser.models import AffiliatedBlog
from ..blog.models import Post

def search(request):
    """
    Searches through following fields:
        - Post teaser
        - Blogger last_name
        - AffilatedBlog blogname
        - Exact matches if input is given between quotes ' or "
    Return list of alumni with all thesis links """

    words = request.GET.get("terms", "")
    terms, posts, bloggers, affiliated_blogs = [], [], [], []

    if len(words) <= 2:
        messages.error(request, "Error: Please use at least 3 characters to search.")
        messages.info(request, "Tip: you can use exact match by placing ' or \" around words!")
        return render(request, "search/search_results.html",
            {
                "posts": posts,
                "bloggers": bloggers,
                "affiliated_blogs": affiliated_blogs,
                "key_words": terms
            }
        )

    if len(words.split()) > 10:
        messages.error(request, "Error: Please limit your search to <10 words.")
        messages.info(request, "Tip: you can use exact match by placing ' or \" around words!")
        return render(request, "search/search_results.html",
            {
                "posts": posts,
                "bloggers": bloggers,
                "affiliated_blogs": affiliated_blogs,
                "key_words": terms
            }
        )

    # Check if must be exact match (i.e. if between quotation marks)
    words = words.replace("'", '"')
    if '"' in words:
        exact_match = re.findall('"([^"]*)"', words)

        for exact in exact_match:
            words.replace(exact, "")
            terms.append(exact)

    # Create final lists of search terms
    terms = terms + words.split()

    #  Remove single characters
    terms = [term for term in terms if len(term) > 1]

    # Compute filters
    posts_filter = Q()
    bloggers_filter = Q()
    affiliated_blogs_filter = Q()
    all_posts = Post.objects.filter(is_published=True)
    all_bloggers = Blogger.objects.all()
    all_affiliated_blogs = AffiliatedBlog.objects.all()

    for term in terms:
        posts_filter = (posts_filter |
            Q(teaser__icontains=term) | Q(url__icontains=term) | Q(title__icontains=term)
        )

        bloggers_filter = (bloggers_filter |
            Q(first_name__icontains=term) | Q(last_name__icontains=term) |
            Q(affiliation__blogname__icontains=term)
        )

        affiliated_blogs_filter = (affiliated_blogs_filter |
            Q(blogname__icontains=term) | Q(url__icontains=term)
        )

    # # Compute combined filter
    # total_filter = time_filter & search_filter

    # # Apply all filters
    posts = all_posts.filter(posts_filter).distinct()
    bloggers = all_bloggers.filter(bloggers_filter).distinct()
    affiliated_blogs = all_affiliated_blogs.filter(affiliated_blogs_filter).distinct()

    # if len(results) > 10:
    #     msg = "Search matched {0} items. Tip: you can use exact match by placing ' or \" around words!".format(len(results))
    #     messages.warning(request, msg)


    return render(request, "search/search_results.html",
        {
            "posts": posts,
            "bloggers": bloggers,
            "affiliated_blogs": affiliated_blogs,
            "key_words": terms
        }
    )

