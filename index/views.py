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

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.user = request.user
            menu.save()
            form.save_m2m()  # 保存多对多关系
            return redirect('history')
    else:
        form = MenuForm()

    return render(request, 'menu_form.html', {'form': form})


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


