from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from django import template
from .models import *

# Create your views here.
register = template.Library()

def index(request):
    blogs = Post.objects.all()

    tags = request.GET.getlist('tag', None)

    # Filter by tag
    if tags:
    	print tags
        multifilter = Q()
        for tag in tags:
            label_value = get_object_or_404(Tag, tag_name=tag)
            multifilter = multifilter | Q(tags=label_value)   

    	blogs = blogs.filter(multifilter)  	


    # Make list a paginator object to handle number of products shown
    # per page
    products_per_page = request.GET.get('limit', '15')

    
    blogs_per_page = 10 	# Temporarily always max 10
    # Validate input (protection agains hacking..)
    # if not blogs_per_page.isdigit():
    #     blogs_per_page = 10

    paginator = Paginator(blogs, blogs_per_page)
    page = request.GET.get('page', 1)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'blogs': blogs,
    											'current_tags': tags})

def about(request):
    #  Return about us content from admin

    return render(request, 'blog/aboutus.html')