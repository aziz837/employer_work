from django.contrib import admin
# from .forms import ProfileForm
from .models import Category, Region, UserCategory

@admin.register(Category)
class CategoryAdmin (admin.ModelAdmin):
    list_display=('title', 'parend_id')
  

@admin.register(Region)
class RegionAdmin (admin.ModelAdmin):
    list_display=('id', 'title', 'parend_id')
@admin.register(UserCategory)
class UserCategoryAdmin (admin.ModelAdmin):
    list_display=('id', 'user_id')