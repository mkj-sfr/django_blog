from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Blog

class RegisterForm(UserCreationForm):
    firstname=forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'First name',
        'class': 'form-control'
    }))

    lastname=forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Last name',
        'class': 'form-control'
    }))

    username=forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))

    email=forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))

    password1=forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
        'data-toggle': 'password',
        'id': 'password'
    }))

    password2=forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'form-control',
        'data-toggle': 'password',
        'id': 'password'
    }))


    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']

class UpdateBlogForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Blog
        fields = ['title', 'image', 'content']

class CreateBlogForm(forms.ModelForm):
    title = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Blog
        fields = ['title', 'image', 'content']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'firstname', 'lastname']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class DeleteBlogForm(forms.ModelForm):
    id = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'hidden'}))