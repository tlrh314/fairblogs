from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Blogger
from .models import AffiliatedBlog


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Email address is used to log in.")
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    affiliation = forms.ModelChoiceField(queryset=AffiliatedBlog.objects.all(),
        required=False, help_text="Welke blog? Laat leeg als jouw blog er niet tussen staat!")

    class Meta:
        model = Blogger
        fields = ("email", "first_name", "last_name", "facebook", "twitter", "instagram", "affiliation", "password1", "password2", )


class CreateAffiliationForm(forms.ModelForm):
    class Meta:
        model = AffiliatedBlog
        fields = ("blogname", "url", "logo", "email")

class EditBloggerForm(forms.ModelForm):
    # affiliation = forms.ModelChoiceField(queryset=AffiliatedBlog.objects.all(),
    #     required=True, help_text="Welke blog? Laat leeg als jouw blog er niet tussen staat!")

    class Meta:
        model = Blogger
        fields = ("email", "first_name", "last_name", "affiliation", "avatar", "facebook", "twitter", "instagram",)
