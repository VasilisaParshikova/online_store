from django import forms
from user_app.models import Profile


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "E-mail"}))
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreationForm(forms.Form):
    name = forms.CharField
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "E-mail"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "avatar", "phone"]
