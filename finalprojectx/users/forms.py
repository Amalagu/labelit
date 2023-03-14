from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from label.models import Project


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [  'username', 'email', 'password1']
        labels = {
              'password1': 'Password'
        }

    """def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})"""


class AuthForm(AuthenticationForm):
    '''
	Form that uses built-in AuthenticationForm to handel user auth
	'''
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','password')


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title',  'description',
                  'demo_link', 'source_link']
        widgets = {
            'annotators': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})
