from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .choices import *
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError


# override basic authentication form to allow logging in with email or username
class EmailAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.data['username']
        if '@' in username:
            try:
                username = User.objects.get(email=username).username
            except ObjectDoesNotExist:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return username


# override basic user creation for to add required email field
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


# form for creating basic text note
class NoteForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "20", 'height': '100%'}), required=False)
    theme = forms.ChoiceField(choices=THEMES, label="Theme", initial='', widget=forms.Select(), required=True)


# form for creating list note
class NoteListForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(required=False, label="List items",
                              widget=forms.TextInput(attrs={'placeholder': 'Add item and press Enter'}))
    theme = forms.ChoiceField(choices=THEMES, label="Theme", initial='', widget=forms.Select(), required=True)


# form for creating picture note
class NotePictureForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "20", 'height': '100%'}), required=False)
    picture = forms.ImageField()


# override picture note form to show actual picture path
class NotePictureFormUpdate(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "20", 'height': '100%'}),
        required=False)
    picture = forms.ImageField(required=False)
