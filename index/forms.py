from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Menu, FoodItem, FoodItemCategory

# user register form
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

# user login
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'



class MenuForm(forms.ModelForm):
    food_items = forms.ModelMultipleChoiceField(
        queryset=FoodItem.objects.all().order_by('food_item_category__name', 'name'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Menu
        fields = ['food_items']

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        # 获取所有分类
        categories = FoodItemCategory.objects.all().order_by('name')

        # 根据分类分组食物
        grouped_choices = []
        for category in categories:
            food_items = FoodItem.objects.filter(food_item_category=category).order_by('name')
            grouped_choices.append((category.name, [(item.id, item.name) for item in food_items]))

        self.fields['food_items'].choices = grouped_choices
