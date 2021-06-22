from chat_app.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import UserProfile
from .forms import UserForm
# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your Account has been created!")
            return redirect("register")
    else:
        form = UserForm()

    return render(request, "register.html", {"form": form})


def room(request, room_name):
    username = request.user
    User = get_user_model()
    users = User.objects.all()

    return render(request, "create_chat.html", {"room_name": room_name, "username": username, "users": users})
