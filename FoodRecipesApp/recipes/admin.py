from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Recipe, Review, Category, Ingredient, RecipeIngredient, Instruction, CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


# Register your models here.

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role',)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('role',)
        })
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('User Roles', {
            'fields': ('role',)
        })
    )
    add_form = CustomUserCreationForm


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Instruction)
admin.site.register(Review)
