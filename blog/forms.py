# blog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, News, Category, Author, Information

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Users
        fields = ('username', 'phone_number', 'profile_picture', 'password1', 'password2')

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image','fil', 'category', 'video'] 
        # widgets = {
        #     'category': forms.Select()  # Customize widget if needed
        # }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'photo', 'twitter', 'telegram', 'linkedin', 'instagram']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'description', 'file']