from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Blogger
from .models import AffiliatedBlog


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, label="Email", help_text="Email address is used to log in.")
    first_name = forms.CharField(max_length=30, label="Voornaam", required=True)
    last_name = forms.CharField(max_length=30, label="Achternaam", required=True)
    affiliation = forms.ModelChoiceField(queryset=AffiliatedBlog.objects.all(),
        required=False, label="Blog", help_text="Welke blog? Laat leeg als jouw blog er niet tussen staat!")
    avatar = forms.FileField(required=True, label="Avatar", help_text="Upload hier een foto van jezelf.")

    class Meta:
        model = Blogger
        fields = ("email", "first_name", "last_name", "avatar", "affiliation", "password1", "password2", )


class CreateAffiliationForm(forms.ModelForm):
    url = forms.URLField(initial="https://")
    facebook = forms.URLField(required=False, initial="https://")
    twitter = forms.URLField(required=False, initial="https://")
    instagram = forms.URLField(required=False, initial="https://")

    class Meta:
        model = AffiliatedBlog
        fields = ("blogname", "url", "logo", "email", "facebook", "twitter", "instagram",)


class EditAffiliationForm(forms.ModelForm):
    url = forms.URLField(initial="https://")
    facebook = forms.URLField(initial="https://")
    twitter = forms.URLField(initial="https://")
    instagram = forms.URLField(initial="https://")

    class Meta:
        model = AffiliatedBlog
        fields = ("blogname", "url", "logo", "email", "facebook", "twitter", "instagram",)


class EditBloggerForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ("email", "first_name", "last_name", "avatar", "affiliation")
