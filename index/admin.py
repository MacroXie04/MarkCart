from django.contrib import admin
from .models import FoodItem
from .models import FoodItemCategory

admin.site.register(FoodItem)
admin.site.register(FoodItemCategory)

