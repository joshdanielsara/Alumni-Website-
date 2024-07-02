# forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core import validators
from django.db import models
from .models import UserProfile, Profile, Post, Comment, Message

# CustomRegistrationForm
class CustomRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=False)
    middle_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    year = forms.CharField(label='Year Graduated', max_length=4, required=False)
    strand = forms.ChoiceField(label='Strand', choices=[
        ('tvl', 'TVL'),
        ('abm', 'ABM'),
        ('humss', 'HUMSS'),
        ('stem', 'STEM'),
    ], required=False)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


# UserProfile Forms
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'middle_name', 'last_name', 'year_graduated', 'strand', 'profile_picture']




# Profile Forms
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'middle_name', 'last_name', 'year_graduated', 'strand', 'profile_picture']


# Post and Comment Forms
class PostForm(forms.ModelForm):
    link = forms.URLField(label='Link', required=False)

    class Meta:
        model = Post
        fields = ['content', 'photo', 'video', 'category', 'link']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        link = cleaned_data.get('link')

        if not content and not link:
            raise forms.ValidationError("You must provide either content or a link.")

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


# Message Form
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
