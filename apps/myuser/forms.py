from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Blogger
from .models import AffiliatedBlog


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Email address is used to log in.")
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    affiliation = forms.ModelChoiceField(queryset=AffiliatedBlog.objects.all(),
        required=False, help_text="Which blog? Leave blank if you're new!")

    class Meta:
        model = Blogger
        fields = ("email", "first_name", "last_name", "affiliation", "password1", "password2", )