from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.utils import timezone

# Create your models here.

# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self.create_user(username, email, password, **extra_fields)
#
#
# class CustomUser(AbstractUser):
#     name = models.CharField(max_length=100)
#     surname = models.CharField(max_length=100)
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return f"{self.name} {self.surname}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    prep_time = models.PositiveIntegerField(default=0)  # overall recipe preparation time in minutes
    cook_time = models.PositiveIntegerField(default=0)  # time needed for cooking/baking
    servings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} {self.ingredient}"

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.IntegerField(default=0)
    description = models.TextField()

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField(default=0)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return f"For: {self.recipe}, by: {self.user}"
