from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name= ('groups'),
        blank=True,
        help_text= ('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='custom_user_groups'  # Provide a unique related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name= ('user permissions'),
        blank=True,
        help_text= ('Specific permissions for this user.'),
        related_name='custom_user_permissions'  # Provide a unique related_name
    )
    phone_number = models.IntegerField(default=0)
    full_name = models.CharField(max_length=30, default="")
    def __str__(self):
        return self.first_name
    


class UserProfile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, default="")
    age = models.IntegerField(default=0, validators=[MaxValueValidator(110)])
    gender = models.CharField(max_length=10, default="", choices=GENDER_CHOICES)
    current_address = models.TextField(default="")
    native_address = models.TextField(default="")
    mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999)], default=0)
    marital_status = models.CharField(max_length=15, default="Unmarried")
    profile_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.full_name
    
class FamilyDetails(models.Model):
    related_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    relation = models.CharField(max_length=40, default="")
    full_name = models.CharField(max_length=50, default="")
    mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999)])
    current_address = models.TextField(default="")
    marital_status = models.CharField(default="", max_length=20)
    age = models.IntegerField(default=0,validators=[MaxValueValidator(110)])
    photo = models.ImageField(upload_to='images/')
    def __str__(self):
        return f"{self.related_to.full_name}'s {self.relation}"

class Post(models.Model):
    MARRIAGE = 'Marriage'
    BIRTH = 'Birth'
    DEATH = "Death"
    BUSINESS = "Business"
    JOB = "Job"
    TYPE_CHOICES = [
        (MARRIAGE, 'Marriage'),
        (BIRTH, 'Birth'),
        (DEATH, "Death"),
        (BUSINESS, "Business"),
        (JOB, "Job")
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length=10, choices=TYPE_CHOICES)
    message = models.TextField(default="")
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f" {self.type_of_post} Post By {self.user.full_name}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"{self.user.full_name}'s Comment On {self.post.user.full_name}'s Post"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} Liked {self.post.user.full_name}'s Post"

class MatrimonialProfile(models.Model):
    SINGLE = 'Single'
    DIVORCEE = 'Divorcee'
    MARITAL_CHOICES = [
        (SINGLE, 'Single'),
        (DIVORCEE, 'Divorcee'),
    ]
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, default="")
    birth_date = models.DateField(default=None, null=False)
    age = models.IntegerField(default=None, null=False)
    current_address = models.TextField(default=None, null=False)
    native_address = models.TextField(default=None, null=False)
    gender = models.CharField(max_length=10, default="", choices=GENDER_CHOICES)
    mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999)], default=0)
    marital_status = models.CharField(default="", max_length=15 , choices=MARITAL_CHOICES)
    profile_picture = models.ImageField(upload_to='images/')
    height = models.FloatField(default=0)
    weight = models.IntegerField(default=0)
    education = models.CharField(max_length=255, default='')
    occupation = models.CharField(max_length=255, default='')
    occupation_detail = models.TextField(default="")
    hobby = models.JSONField(default=list)

    def __str__(self):
        return self.full_name