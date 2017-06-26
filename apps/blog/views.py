from django import template
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import Post
from .models import Tag
from .forms import SubmitBlogpostForm


register = template.Library()


def index(request):
    blogs = Post.objects.all()

    tags = request.GET.getlist("tag", None)

    # Filter by tag
    if tags:
        multifilter = Q()
        for tag in tags:
            label_value = get_object_or_404(Tag, tag_name=tag)
            multifilter = multifilter | Q(tags=label_value)

        blogs = blogs.filter(multifilter)


    # Make list a paginator object to handle number of products shown
    # per page
    products_per_page = request.GET.get("limit", "15")


    blogs_per_page = 10     # Temporarily always max 10
    # Validate input (protection agains hacking..)
    # if not blogs_per_page.isdigit():
    #     blogs_per_page = 10

    paginator = Paginator(blogs, blogs_per_page)
    page = request.GET.get("page", 1)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    return render(request, "blog/index.html", {"blogs": blogs,
                                                "current_tags": tags})

@login_required
def submit(request):
    if request.method == "POST":
        form = SubmitBlogpostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # TODO: this is why blog should have slug. Then submit-success can be reversed and redirected to the blogpost...

            post = Post()
            post.author = request.user
            post.title = form.cleaned_data["title"]
            post.teaser = form.cleaned_data["teaser"]
            post.url = form.cleaned_data["url"]
            post.image = form.cleaned_data["image"]
            post.date_created = form.cleaned_data["date_created"]
            post.publish()  # publish implies save
            return HttpResponseRedirect(reverse("post_detail", kwargs={"slug": post.slug}))
    else:
        form = SubmitBlogpostForm()

    return render(request, "blog/submit.html", { "form": form })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/detail.html", { "post": post })
