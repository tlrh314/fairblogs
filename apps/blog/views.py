from django.shortcuts import render
from django import template
from .models import *

# Create your views here.
register = template.Library()

def index(request):
    blogs = Post.objects.all()

    return render(request, 'blog/index.html', {'blogs': blogs})

def about(request):
    #  Return about us content from admin

    return render(request, 'blog/aboutus.html')