# blog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, News, Category, Author, Information
from django.core.exceptions import ValidationError

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

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and file.size > 2 * 1024 * 1024:  # 2 MB
            raise ValidationError("Fayl hajmi 2MB dan oshmasligi kerak.")
        return file

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video and video.size > 5 * 1024 * 1024:  # 10 MB
            raise ValidationError("Video hajmi 5MB dan oshmasligi kerak.")
        return video

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'photo', 'twitter', 'telegram', 'linkedin', 'instagram']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'description', 'file']