from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login/', user_login, name="login"),
    path('register/', register_customer),
    path('logout/', logout_view, name='logout'),
    path('recipes/', all_recipes),
    path('recipes/<int:recipe_id>/', details, name="details"),
    path('delete-recipe/<int:recipe_id>/', delete_recipe, name='delete_recipe'),
    path('add-recipe/', add_recipe, name='add_recipe'),
    path('recipe/edit/<int:recipe_id>/', edit_recipe, name='edit_recipe'),
    path('for-you/', for_you, name="for_you"),
    path('contact/', contact, name="contact"),
    path('contact-form/', contact_form_submission, name='contact_form_submission')
    # path('recipe/<int:recipe_id>/', recipe_review, name='recipe_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
