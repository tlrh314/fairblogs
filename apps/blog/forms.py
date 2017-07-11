from django import forms
from django.utils import timezone
from django.forms.utils import ErrorList
from django.template.defaultfilters import slugify

from .models import Post
from .models import Tag


class SubmitBlogpostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "url", "date_created", "tags", "image", "teaser" )

    url = forms.URLField(initial="https://")
    date_created = forms.DateTimeField(label="Post is gepubliceerd op", initial=timezone.now)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    teaser = forms.CharField(required=True, min_length=250, max_length=750, widget=forms.Textarea())

    def clean(self):
        slug = slugify(self.cleaned_data.get("title"))
        image = self.cleaned_data.get("image")
        number_of_tags = self.cleaned_data.get("tags").count()

        # Breaks when changing the Post because a Post with the same slug already exists
        # TODO: this is the quick'n'dirty fix to just not clean posts...
        # if Post.objects.filter(slug=slug).count() >=1 :
        #     self._errors["title"] = ErrorList()
        #     self._errors["title"].append("Een post met deze titel bestaat al. Kies een unieke titel!")

        if not image:
            self._errors["image"] = ErrorList()
            self._errors["image"].append("Uploaden van een plaatje is verplicht.")

        if number_of_tags < 1 or number_of_tags > 5:
            self._errors["tags"] = ErrorList()
            self._errors["tags"].append("Het aantal tags moet tussen de een en vijf liggen.")


class SelectPostForm(forms.Form):
    def __init__(self, affiliation, *args, **kwargs):
        super(SelectPostForm, self).__init__(*args, **kwargs)
        self.fields["which_post"].queryset = Post.objects.filter(author__affiliation=affiliation)

    which_post = forms.ModelChoiceField(
        label="Welke post wil je aanpassen?",
        required=True,
        queryset=None,  # note that we set the queryset in the init method above
        widget=forms.Select(attrs={"class": "form-control"})
    )
