from django.contrib import admin
from .models import FoodItem
from .models import FoodItemCategory
from .models import Menu

admin.site.register(FoodItem)
admin.site.register(FoodItemCategory)
admin.site.register(Menu)

