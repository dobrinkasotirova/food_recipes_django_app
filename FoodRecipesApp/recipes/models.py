from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone


# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('a', 'Admin'),
        ('u', 'User')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, )

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    prep_time = models.PositiveIntegerField(default=0)  # overall recipe preparation time in minutes
    cook_time = models.PositiveIntegerField(default=0)  # time needed for cooking/baking
    servings = models.IntegerField(default=0)
    image = models.ImageField(upload_to="data/")

    def __str__(self):
        return f"{self.name}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.recipe} {self.ingredient}"


class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.IntegerField(default=0)
    description = models.TextField()


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField(default=0)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return f"For: {self.recipe}, by: {self.user}"
