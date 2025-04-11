import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from .validators import validate_file_size
from django.core.validators import FileExtensionValidator

class MyAccaountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, age, password=None):
        if not email:
            raise ValueError("Users must have email address!!")
        if not username:
            raise ValueError("Users must have username!!")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, age, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            age=age,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    username = models.CharField(max_length=255, unique=True)
    data_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    bio = models.TextField(null=True, blank=True, max_length=255)
    age = models.DateField(default=datetime.date.today)
    profile_pic = models.ImageField(upload_to='image/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'age']

    objects = MyAccaountManager()

    def __str__(self):
        return self.username + "," + self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Adminlar"

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()  # Muallif haqida qisqacha ma'lumot
    photo = models.ImageField(upload_to='author_photos/', blank=True, null=True)  # Muallifning rasmi
    twitter = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    fil = models.FileField(upload_to='news_files/', blank=True, null=True, validators=[validate_file_size])

    video = models.FileField(
        upload_to='news_videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])],
        help_text='MP4, MOV, AVI formatdagi video fayl yuklang'
    )

    def __str__(self):
        return self.title
    
    def get_summary(self):
        return self.summary[:100]  # Faqat 100 ta belgi qaytaradi
    
class Information(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='information_files/')  # Faylni yuklash uchun
    upload_date = models.DateField(auto_now_add=True, validators=[validate_file_size])
    image = models.ImageField(upload_to='information_images/', null=True, blank=True)
    
    def __str__(self):
        return self.title

class Presentation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='presentations/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HelpGuide(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='guides/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class OfficialDocument(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='official_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
