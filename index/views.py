from anaconda_cloud_auth.client import login_required
from django.shortcuts import render
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from .forms import MenuForm
from .models import Menu
import openai
from openai import OpenAI
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


# ChatGPT generate menu

def generate_menu(food_items):
    """
    Generates a recipe using OpenAI based on the given food items.

    :param food_items: List of food item names selected by the user.
    :return: Generated recipe text from ChatGPT.
    """
    if not food_items:
        return "No food items selected. Please choose ingredients to generate a recipe."

    # Convert list of food items to a formatted string
    food_names = ', '.join(food_items)

    # Define the prompt for ChatGPT
    prompt = f"""
    I have the following ingredients: {food_names}. 
    Please generate a delicious recipe that includes:
    - A creative recipe name
    - A list of ingredients
    - Step-by-step cooking instructions
    - Cooking time and serving size (optional)
    - Any additional cooking tips or variations
    """

    try:
        # Call OpenAI API
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o for better response quality
            messages=[
                {"role": "system", "content": "You are a professional chef providing creative recipes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500  # Limit response length
        )

        # Extract generated content
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"ChatGPT API Error: {e}")
        return "Failed to generate the recipe. Please try again later."

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.user = request.user
            menu.save()
            form.save_m2m()

            # get selected food items
            selected_food_items = menu.food_items.all()
            food_names = [food.name for food in selected_food_items]

            # generate menu using ChatGPT
            menu.chatgpt_menu = generate_menu(food_names)
            menu.save()

            return redirect('view_menu', menu_id=menu.id)
    else:
        form = MenuForm()

    return render(request, 'index.html', {'form': form})


@login_required(login_url='/login/')
def view_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)

    if menu.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this menu.")

    return render(request, 'menu_detail.html', {'menu': menu})


@login_required(login_url='/login/')
def history(request):
    menus = Menu.objects.filter(user=request.user)
    return render(request, 'history.html', {'menus': menus})


# user authentication
@login_required(login_url='/login/')
def web_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})
