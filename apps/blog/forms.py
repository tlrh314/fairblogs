from dal import autocomplete
from django import forms
from django.forms.utils import ErrorList
from django.utils import timezone

from .models import Post


class SubmitBlogpostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "url", "date_created", "tags", "image", "teaser")

        widgets = {
            "tags": autocomplete.ModelSelect2Multiple(url="blogs:tag-autocomplete"),
        }

    url = forms.URLField(initial="https://")
    date_created = forms.DateTimeField(
        label="Post is gepubliceerd op", initial=timezone.now
    )
    teaser = forms.CharField(
        required=True, min_length=250, max_length=750, widget=forms.Textarea()
    )

    def clean(self):
        image = self.cleaned_data.get("image")
        number_of_tags = self.cleaned_data.get("tags").count()

        # Breaks when changing the Post because a Post with the same slug already exists
        # TODO: this is the quick'n'dirty fix to just not clean posts...
        # slug = slugify(self.cleaned_data.get("title"))
        # if Post.objects.filter(slug=slug).count() >=1 :
        #     self._errors["title"] = ErrorList()
        #     self._errors["title"].append("Een post met deze titel bestaat al. Kies een unieke titel!")

        if not image:
            self._errors["image"] = ErrorList()
            self._errors["image"].append("Uploaden van een plaatje is verplicht.")

        if number_of_tags < 1 or number_of_tags > 5:
            self._errors["tags"] = ErrorList()
            self._errors["tags"].append(
                "Het aantal tags moet tussen de een en vijf liggen."
            )


class SelectPostForm(forms.Form):
    def __init__(self, affiliation, *args, **kwargs):
        super(SelectPostForm, self).__init__(*args, **kwargs)
        # is_published is not included in the SubmitBlogpostForm, so it cannot be changed on-site.
        # Only admins can change it. TODO: decide whether or not Bloggers should be able to change is_published
        # if so, add it to the form
        self.fields["which_post"].queryset = Post.objects.filter(
            author__affiliation=affiliation
        ).exclude(is_published=False)

    which_post = forms.ModelChoiceField(
        label="Welke post wil je aanpassen?",
        required=True,
        queryset=None,  # note that we set the queryset in the init method above
        widget=forms.Select(attrs={"class": "form-control"}),
    )
