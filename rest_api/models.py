from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth import get_user_model


FULL_TIME = 'FULL_TIME'
PART_TIME = 'PART_TIME'
REMOTE = 'REMOTE'
HYBRID = 'HYBRID'

JOB_TYPE_CHOICES = [
    (FULL_TIME, 'Full Time'),
    (PART_TIME, 'Part Time'),
    (REMOTE, 'Remote'),
    (HYBRID, 'Hybrid'),
]


# Create your models here.



# class Profile(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, username=username, password=password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    last_login = None
    first_name = models.CharField("First Name", max_length=127, blank=True, null=True)
    last_name = models.CharField("First Name", max_length=127, blank=True, null=True)
    email = models.EmailField("email address", unique=True, db_index=True)
    profile_picture = models.ImageField("Profile Picture", upload_to="profile_picture", null=True, blank=True)
    is_employer = models.BooleanField(default=False)

    # Override groups and user_permissions with custom related_names
    groups = models.ManyToManyField("auth.Group", verbose_name="groups", blank=True, help_text="The groups this user belongs to.", related_name="core_user_set", related_query_name="core_user")
    user_permissions = models.ManyToManyField("auth.Permission", verbose_name="user permissions", blank=True, help_text="Specific permissions for this user.", related_name="core_user_set", related_query_name="core_user")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']  # Add 'username' to REQUIRED_FIELDS

    def __str__(self):
        return f"{self.email} - {self.is_employer}"


class CheckCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.code


class Company(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    location = models.CharField(max_length=500)

    job_type = models.CharField(
        max_length=100,
        choices=JOB_TYPE_CHOICES,
        default=FULL_TIME,
    )

    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    last_message = models.DateTimeField(auto_now=True)


class Message(models.Model):
    content = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    cv_file = models.FileField(upload_to='files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:30]}"




class CV(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    profession = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)

    skills = models.TextField(help_text="Comma-separated skills: Python, Django, Docker")
    languages = models.TextField(help_text="Comma-separated languages: English, Uzbek")

    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)

    cv_file = models.FileField(upload_to='cv_files/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}'s CV"

