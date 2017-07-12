from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import AboutUs
from .models import ContactInfo
from .models import PrivacyPolicy
from .models import Disclaimer


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("rename_text",)
    readonly_fields = ( "date_created", "date_updated", "last_updated_by" )

    fieldsets = [
        ( "About Us -- Bovenste deel", {
            "fields": [ "about" ] }
        ), ("About Fairfrog", {
            "fields": [ "about_fairfrog", "url_fairfrog", "logo_fairfrog" ]}
        ), ("About Socii", {
            "fields": [ "about_sociii", "url_sociii", "logo_sociii" ]}
        ), ("About Project Cece", {
            "fields": [ "about_projectcece", "url_projectcece", "logo_projectcece" ]}
        ), ( "About Us -- Onderste deel", {
            "fields": [ "about_below" ] }
        ), ( "Meta", {
            "classes": ["collapse"],
            "fields": ["date_created", "date_updated", "last_updated_by"]}
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def rename_text(self, obj):
        return "Click here to change the About Us page"
    rename_text.short_description = "About Us"

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ("rename_text",)
    readonly_fields = ( "date_created", "date_updated", "last_updated_by" )

    fieldsets = [
        ( "Privacy Policy", {
            "fields": [ "policy", "date_updated"]}
        ), ( "Meta", {
            "classes": ["collapse"],
            "fields": ["date_created", "date_updated", "last_updated_by"]}
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def rename_text(self, obj):
        return "Click here to change the Privacy Policy"
    rename_text.short_description = "Privacy Policy"


@admin.register(Disclaimer)
class DisclaimerAdmin(admin.ModelAdmin):
    list_display = ("rename_text",)
    readonly_fields = ( "date_created", "date_updated", "last_updated_by" )

    fieldsets = [
        ( "Disclaimer", {
            "fields": [ "policy", "date_updated"]}
        ), ( "Meta", {
            "classes": ["collapse"],
            "fields": ["date_created", "date_updated", "last_updated_by"]}
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def rename_text(self, obj):
        return "Click here to change the Disclaimer"
    rename_text.short_description = "Disclaimer"


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = "__all__"

    # def clean(self):
    #     phonenumber = self.cleaned_data.get("phone")

    #     if len(phonenumber) != 13 and phonenumber[0:4] != "003120":
    #         raise forms.ValidationError("Please enter 13 digits for the phone number, starting with 003120")
    #     return self.cleaned_data


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("contact_email", "webmaster_email",
            "address", "postbox", "phone" )
    readonly_fields = ( "date_created", "date_updated", "last_updated_by" )
    form = ContactInfoForm

    fieldsets = [
        ( "Contact Information", {
            "fields": ["contact_email", "webmaster_email", "address", "postbox", "phone"]}
        ), ( "Meta", {
            "classes": ["collapse"],
            "fields": ["date_created", "date_updated", "last_updated_by"]}
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()
