from crispy_forms.helper import FormHelper
from allauth.account.forms import (
    LoginForm,
    SignupForm,
    ChangePasswordForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordForm,
)
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django_select2.forms import Select2Widget

from dash.models import DistrictSanitaire, HealthRegion, PolesRegionaux, ServiceSanitaire, SyntheseActivites
from dash.widgets import DistrictNomSelect2Widget, RegionSelect2Widget, CentreSanteSelect2Widget


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["login"].label = False
        self.fields["password"].label = False
        self.fields["login"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Username",
                "id": "username",
            }
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
                "id": "password",
                "aria-label": "Password",
                "aria-describedby": "password-addon",
            }
        )
        # self.fields['remember'].widget = forms.CheckboxInput(attrs={'class': 'h-4 w-4 border border-gray-300 rounded bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain ltr:float-left rtl:float-right ltr:mr-2 rtl:ml-2 cursor-pointer focus:ring-offset-0 mb-3'})
        # self.fields["remember"].label = "Remember Me"


class UserRegistrationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Username",
                "id": "username",
            }
        )
        self.fields["email"].widget = forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Email", "id": "email"}
        )
        self.fields["email"].label = "Email"
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
                "id": "password1",
                "aria-label": "Password",
                "aria-describedby": "password-addon",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Confirm Password",
                "id": "password2",
                "aria-label": "Password",
                "aria-describedby": "password-addon",
            }
        )
        self.fields["password2"].label = "Confirm Password"


class PasswordChangeForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["oldpassword"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter currunt password",
                "id": "password3",
            }
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
                "id": "password4",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter confirm password",
                "id": "password5",
            }
        )
        self.fields["oldpassword"].label = "Currunt Password"
        self.fields["password2"].label = "Confirm Password"


class PasswordResetForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["email"].widget = forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": " Enter Email",
                "id": "email",
            }
        )
        self.fields["email"].label = "Email"


class PasswordResetKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
                "id": "password6",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter confirm password",
                "id": "password7",
            }
        )
        self.fields["password2"].label = "Confirm Password"


class PasswordSetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordSetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
                "id": "password8",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter confirm password",
                "id": "password9",
            }
        )
        self.fields["password2"].label = "Confirm Password"


class ExcelUploadForm(forms.Form):
    file = forms.FileField()


class DistrictSanitaireForm(forms.ModelForm):
    class Meta:
        model = DistrictSanitaire
        fields = '__all__'
        widgets = {
            'nom': DistrictNomSelect2Widget,  # Recherche AJAX pour le nom du district
            'region': RegionSelect2Widget,  # Recherche AJAX pour la région
        }

class SyntheseActivitesForm(forms.ModelForm):
    class Meta:
        model = SyntheseActivites
        fields = '__all__'
        widgets = {
            'centre_sante': CentreSanteSelect2Widget,  # Utilise le widget Select2 AJAX pour centre_sante
        }


class FilterForm(forms.Form):
    start_date = forms.DateField(required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    district = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-control'}))  # You can populate this dynamically
    region = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-control'}))  # You can populate this dynamically
    pres = forms.ChoiceField(required=False,
                             widget=forms.Select(attrs={'class': 'form-control'}))  # You can populate this dynamically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate districts and regions choices from your models

        self.fields['district'].choices = [(d.id, d.nom) for d in DistrictSanitaire.objects.all()]
        self.fields['region'].choices = [(r.id, r.name) for r in HealthRegion.objects.all()]
        self.fields['pres'].choices = [(r.id, r.name) for r in PolesRegionaux.objects.all()]
