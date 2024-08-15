from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from myblog.models import UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'

        # Remove the password field
        if 'password' in self.fields:
            self.fields.pop('password')

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

class EditProfilePageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_pic', 'website_link', 'instagram_link', 'facebook_link', 'twitter_link')

    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    website_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    instagram_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    facebook_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    twitter_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_pic', 'website_link', 'instagram_link', 'facebook_link', 'twitter_link')

    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    website_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    instagram_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    facebook_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    twitter_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)