from django import forms
from django.forms.utils import ErrorList
from tinymce.widgets import TinyMCE
from django.utils import timezone
from django.contrib.admin import widgets

from .models import Post
from .models import Tag

TINYMCE_LOCAL_CONFIG= {
    'selector': 'textarea',
    'height': 200,
    'width': 0,
    'menubar': False,
    'statusbar': False,
    'elementpath': False,
    'plugins': [
        'paste',
    ],
    'toolbar1': 'undo redo | bold italic | bullist numlist outdent indent | ',
    'toolbar2': '',
    'paste_as_text': True,
}


class SubmitBlogpostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "url", "date_created", "tags", "image", "teaser" )

    # tags = forms.ModelMultipleChoiceField(
    #         widget=forms.CheckboxSelectMultiple(),
    #         queryset=Tag.objects.all(),
    #         required=True)

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    date_created = forms.DateTimeField(label="Post is gepubliceerd op")

    teaser = forms.CharField(
        required=True,
        max_length=2048,
        widget=TinyMCE(mce_attrs=TINYMCE_LOCAL_CONFIG)
    )


    def clean(self):
        image = self.cleaned_data.get("image")
        if not image:
            self._errors["image"] = ErrorList()
            self._errors["image"].append("Please upload an image")
