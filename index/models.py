from django.db import models
from django.contrib.auth.models import User

# All food items
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    food_item_category = models.ForeignKey('FoodItemCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FoodItemCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Menu(models.Model):
    # foreign key to user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='menu')

    # created at
    created_at = models.DateTimeField(auto_now_add=True)

    # food items
    food_items = models.ManyToManyField(FoodItem)

    # ChatGPT generated menu
    chatgpt_menu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Menu"