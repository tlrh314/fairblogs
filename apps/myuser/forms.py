from django import forms
from django.contrib.auth.forms import UserCreationForm

from myuser.models import AffiliatedBlog, Blogger


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, label="Email", help_text="Email address is used to log in."
    )
    first_name = forms.CharField(max_length=30, label="Voornaam", required=True)
    last_name = forms.CharField(max_length=30, label="Achternaam", required=True)
    affiliation = forms.ModelChoiceField(
        queryset=AffiliatedBlog.objects.all(),
        required=False,
        label="Blog",
        help_text="Welke blog? Laat leeg als jouw blog er niet tussen staat!",
    )
    avatar = forms.FileField(
        required=True, label="Avatar", help_text="Upload hier een foto van jezelf."
    )

    class Meta:
        model = Blogger
        fields = (
            "email",
            "first_name",
            "last_name",
            "avatar",
            "affiliation",
            "password1",
            "password2",
        )


class CreateAffiliationForm(forms.ModelForm):
    blogname = forms.CharField(label="Naam van de Blog")
    url = forms.URLField(label="Link naar de Blog", initial="https://")
    facebook = forms.URLField(
        initial="https://",
        required=False,
        help_text="Begint met 'https://'. Laat helemaal leeg als er geen Facebook voor de blog is.",
    )
    twitter = forms.URLField(
        initial="https://",
        required=False,
        help_text="Begint met 'https://'. Laat helemaal leeg als er geen Twitter voor de blog is.",
    )
    instagram = forms.URLField(
        initial="https://",
        required=False,
        help_text="Begint met 'https://'. Laat helemaal leeg als er geen Instagram voor de blog is.",
    )

    class Meta:
        model = AffiliatedBlog
        fields = (
            "blogname",
            "url",
            "logo",
            "email",
            "facebook",
            "twitter",
            "instagram",
        )


class SelectAffiliationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelectAffiliationForm, self).__init__(*args, **kwargs)
        self.fields["which_blog"].queryset = AffiliatedBlog.objects.all()

    which_blog = forms.ModelChoiceField(
        label="Voor welke blog schrijf je?",
        required=False,
        queryset=None,  # note that we set the queryset in the init method above
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class EditAffiliationForm(forms.ModelForm):
    blogname = forms.CharField(label="Naam van de Blog")
    url = forms.URLField(label="Link naar de Blog", initial="https://")
    facebook = forms.URLField(
        initial="https://",
        required=False,
        help_text="Begint met 'https://'. Laat helemaal leeg als er geen Facebook voor de blog is.",
    )
    twitter = forms.URLField(
        initial="https://",
        required=False,
        help_text="Begint met 'https://'. Laat helemaal leeg als er geen Twitter voor de blog is.",
    )
    instagram = forms.URLField(
        initial="https://",
        required=False,
        help_text="Begint met 'https://'. Laat helemaal leeg als er geen Instagram voor de blog is.",
    )

    class Meta:
        model = AffiliatedBlog
        fields = (
            "blogname",
            "url",
            "logo",
            "email",
            "facebook",
            "twitter",
            "instagram",
        )


class EditBloggerForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ("email", "first_name", "last_name", "avatar", "affiliation")
