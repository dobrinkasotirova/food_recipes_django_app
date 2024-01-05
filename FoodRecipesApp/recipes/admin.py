from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Recipe, Review, Category, Ingredient, RecipeIngredient, Instruction
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'surname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


# admin.site.unregister(Group)
# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Instruction)
admin.site.register(Review)
