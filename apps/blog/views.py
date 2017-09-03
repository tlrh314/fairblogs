from django import template
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.syndication.views import Feed


from dal import autocomplete

from .models import Post
from .models import Tag
from .forms import SubmitBlogpostForm
from .forms import SelectPostForm


register = template.Library()


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(tag_name__icontains=self.q)

        return qs


def index(request):
    blogs = Post.objects.filter(is_published=True)

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


    blogs_per_page = 6     # Temporarily always max 6
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
    # Catch rascals that created user account w/o AffiliatedBlog
    if not request.user.affiliation:
        request.session["new_user_pk"] = request.user.pk
        return redirect("set_affiliation")

    if request.method == "POST":
        form = SubmitBlogpostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = Post()
            post.author = request.user
            post.title = form.cleaned_data["title"]
            post.teaser = form.cleaned_data["teaser"]
            post.url = form.cleaned_data["url"]
            post.image = form.cleaned_data["image"]
            post.date_created = form.cleaned_data["date_created"]
            # TODO: if is_published should be included in the SubmitBlogpostForm, then
            # post.publish() if form.cleaned_data["is_published"] else post.unpublish()
            post.publish()  # publish implies save

            # Caution, post needs to be saved before m2m can be added!
            post.tags = form.cleaned_data["tags"]

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(Post).pk
            LogEntry.objects.log_action(
                    request.user.pk, content_type_pk, post.pk, str(post), ADDITION,
                    change_message="New Post created via submit form."
                    )

            return HttpResponseRedirect(reverse("blogs:post_detail", kwargs={"slug": post.slug}))
    else:
        form = SubmitBlogpostForm()

    return render(request, "blog/submit.html", { "form": form })


@login_required
def select_post(request):
    if request.method == "POST":
        form = SelectPostForm(data=request.POST, affiliation=request.user.affiliation)
        if form.is_valid():
            post = form.cleaned_data["which_post"]
            return HttpResponseRedirect(reverse("blogs:change_post", kwargs={"slug": post.slug}))
    else:
        form = SelectPostForm(affiliation=request.user.affiliation)

    return render(request, "blog/select_post.html", { "form": form })


def affiliation_check(user):
    return user.affiliation.endswith("sjenk")


@login_required
def change_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.affiliation != post.author.affiliation:
        return redirect(reverse("pages:permission_denied"))

    if not post.is_published:
        raise Http404("Post is unpublished. First publish the blogpost, then edit the blogpost on the website. ")

    if request.method == "POST":
        form = SubmitBlogpostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save()

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(Post).pk
            LogEntry.objects.log_action(
                    request.user.pk, content_type_pk, post.pk, str(post), CHANGE,
                    change_message="Post changed via submit form."
                    )

            return HttpResponseRedirect(reverse("blogs:post_detail", kwargs={"slug": post.slug}))
    else:
        form = SubmitBlogpostForm(instance=post)

    return render(request, "blog/change_post.html", { "form": form })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    full_url = request.build_absolute_uri()
    teaser80 = post.teaser[0:80] + "... | FairBlogs: Vind duurzame en eerlijke blogs via één website!"
    if not post.is_published:
        raise Http404("Post is unpublished. First publish the blogpost, then view the blogpost on the website. ")
    return render(request, "blog/detail.html", { "post": post, "full_url": full_url, "teaser80": teaser80 })


def update_post_counter(request, slug):
    post = get_object_or_404(Post, slug=slug.replace('/', ''))
    if not post.is_published:
        raise Http404("Post is unpublished. First publish the blogpost, then use the outlink.")
    post.popularity += 1
    post.save()
    return HttpResponseRedirect(request.GET.get('next'))



class PostsFeed(Feed):
    title = "Feed blog posts"
    link = "feeds/posts/"
    description = "Posts from FairBlogs"

    def items(self):
        return Post.objects.order_by('date_created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser

    def item_author(self, item):
        return item.author

    def item_link(self, item):
        return reverse('Post', args=[item.pk])