from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, RegisterForm


User = get_user_model()


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    print("4", request)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print("1",request)
            username = request.POST.get("username")
            password = request.POST.get("password")
            print("2",username)
            print("3",password)
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect(reverse("login"))
            login(request, user)
            return redirect(reverse("index"))			
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse("index"))					
    return HttpResponseRedirect("/login")


@login_required
def user_list_view(request):
    users = User.objects.all()
    paginator = Paginator(users, 1)    #이전/다음 페이지 확인용
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "users.html", {"users": page_obj})