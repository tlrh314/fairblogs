from captcha.fields import CaptchaField
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Naam",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Wat is uw naam?"}),
    )
    message = forms.CharField(
        label="Bericht",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Wat wilt u ons vertellen?"}),
    )
    sender = forms.EmailField(
        label="Afzender",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "email@adres.nl - zodat we contact met u kunnen opnemen."
            }
        ),
    )
    cc_myself = forms.BooleanField(
        label="Verstuur een kopie'tje naar jezelf.",
        required=False,
        widget=forms.CheckboxInput(),
    )

    captcha = CaptchaField()
