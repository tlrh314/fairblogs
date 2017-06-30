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

    # if len(words) <= 2:
    #     msg = "Please use at least 3 characters to search. "
    #     msg += "Tip: you can use exact match by placing ' or \" around words!"
    #     messages.error(request, msg)
    #     return render(request, "search/search_results.html", {"alumni": [], "key_words": []})

    # if len(words.split()) > 10:
    #     msg = "Please limit your search to <10 words. "
    #     msg += "Tip: you can use exact match by placing ' or \" around words!"
    #     messages.error(request, msg)
    #     return render(request, "search/search_results.html", {"alumni": [], "key_words": []})

    # # Check if must be exact match (i.e. if between quotation marks)
    # words = words.replace("'", '"')
    # if '"' in words:
    #     exact_match = re.findall('"([^"]*)"', words)

    #     for exact in exact_match:
    #         words.replace(exact, "")
    #         terms.append(exact)

    # # Create final lists of search terms
    # terms = terms + words.split()

    # # Set maximum number of words
    # if len(terms) > 42:
    #     return render(request, "search/search_results.html", {"alumni": [],
    #                                                           "key_words": []})
    # #  Remove single characters
    # terms = [term for term in terms if len(term) > 1]

    # # Compute filters
    # search_filter = Q()
    # time_filter = Q()
    # alumni = Alumnus.objects.all()

    # for term in terms:

    #     # Check if year, if set time filters
    #     if (term.isdigit() and len(term) == 4):
    #         end_year = str(int(term) + 1)
    #         date_range=[term+"-01-01",end_year+"-01-01"]
    #         time_filter = (time_filter | Q(theses__date_of_defence__range=date_range)
    #                                    | Q(theses__date_stop__range=date_range)
    #                                    | Q(theses__date_start__range=date_range))

    #     else:
    #         search_filter = (search_filter | Q(last_name__icontains=term)|
    #                                          Q(first_name__icontains=term) |
    #                                          Q(theses__title__icontains=term))

    # # Compute combined filter
    # total_filter = time_filter & search_filter

    # # Apply all filters
    # results = alumni.filter(total_filter).distinct()

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

