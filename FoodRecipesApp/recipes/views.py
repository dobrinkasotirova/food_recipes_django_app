import datetime

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from .forms import CustomAuthenticationForm, CustomerRegistrationForm, AddRecipeForm, EditRecipeForm, ReviewForm
from .models import *
# Create your views here.

def index(request):
    recipes = Recipe.objects.all()[:6]
    return render(request, "index.html", context={"recipe1": recipes[0], "recipe2": recipes[1], "recipe3": recipes[2], "recipes": recipes})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Redirect to the login page after successful registration
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

def all_recipes(request):
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "recipes.html", context)


def details(request, recipe_id=None):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    categories = Category.objects.all()
    reviews = Review.objects.filter(recipe=recipe).all()
    total_review = 0
    if reviews:
        total = 0
        for review in reviews:
            total += review.rating
        total_review = total/len(reviews)*1.0
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Review instance, but don't save it to the database yet
            new_review = form.save(commit=False)
            # Now you can set the additional fields on the new_review object
            new_review.recipe = recipe
            new_review.user = request.user
            new_review.date_posted = timezone.now()  # It's better to use Django's timezone.now()
            # Save the new_review instance to the database
            new_review.save()
            return redirect('details', recipe_id=recipe_id)

    context = {
        'recipe': recipe,
        'categories': categories,
        'reviews': reviews,
        'form': form,
        'total_review': total_review
    }
    return render(request, 'details.html', context=context)


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    # Redirect to the book list page or any other appropriate URL
    return redirect('/recipes')


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the book details page or any other appropriate URL
            return redirect('/recipes')
    else:
        form = AddRecipeForm()

    return render(request, 'add_recipes.html', {'form': form})


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = EditRecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            if 'image' not in request.FILES:  # No new photo uploaded
                form.fields['image'].required = False
            form.save()
            # Redirect to the book details page or any other appropriate URL
            return redirect('details', recipe_id=recipe_id)
        else:
            print(form.errors)
    else:
        form = EditRecipeForm(instance=recipe)

    return render(request, 'details.html', {'form': form})


def for_you(request):
    return render(request, "for_you.html")

# def recipe_review(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     reviews = Review.objects.filter(recipe=recipe)
#     form = ReviewForm()
#     if request.method == 'POST':
#         form = ReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.recipe = recipe
#             review.user = request.user
#             review.save()
#             return redirect('details', recipe_id=recipe_id)
#     return render(request, 'details.html', {'recipe': recipe, 'reviews': reviews, 'form': form})

def contact(request):
    return render(request, "contact.html")