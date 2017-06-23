from django.db import models
from django.utils import timezone
from django.conf import settings
import os

def get_post_image(instance, filename):
    """ Logo of the blog (website) """
    return os.path.join("static", "img", "bloggers", str(instance.author.blogger.blogname), "posts", filename)

class Post(models.Model):
    def make_url_id(self):
        return self.title.replace(" ", "-")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=None)
    title = models.CharField(max_length=300)
    blogintro = models.TextField(default=" ", help_text="Write the short introduction of the blog here, it will be displayed in de bloglist")
    image = models.ImageField(upload_to=get_post_image, blank=True, null=True)
    # models.CharField(max_length=500, default="Add image here", help_text="Write in format: 'filename.png' and put image in static/img/blog folder")

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            default=timezone.now, blank=True, null=True)


    tag = models.CharField(max_length=300) # models.ForeignKey(Category, help_text='Category', default=1)

    featured = models.BooleanField(default=False,
            help_text="Should this post be shown in the featured list?")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ['-published_date',]

    def post_ID(self):
        '''
        Returns url-ID for blog posts: the title with only alphanumeric
        charachters and the words seperated by -. For example:
        'Example, title of a post 1.' becomes 'example-title-of-a-post-1'.
        '''
        a = self.title
        a = pattern.sub('-', a)
        if a.endswith('-'):
            a = a[:-1]
        return a.lower()

    def __str__(self):
        return self.title
