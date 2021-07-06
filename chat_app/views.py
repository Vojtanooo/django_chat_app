from chat_app.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm


def register_page(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your Account has been created!")
            return redirect("register")
    else:
        form = UserForm()

    return render(request, "register.html", {"form": form})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("room", room_name="Chat")
        else:
            messages.error(request, f"Username or Password is incorect!")

    return render(request, "login.html")


def room(request, room_name):
    username = request.user
    User = get_user_model()
    users = User.objects.all()

    dict_of_users_href = {}
    for user in users:
        if not user == username:
            dict_of_users_href[f"{user}"] = "chat{}_{}".format(
                *sorted([username.id, user.id]))

    room_user_list = str(room_name).strip("chat").split("_")
    if str(username.id) in room_user_list:
        room_user_list.remove(str(username.id))

    room_user_name = User.objects.get(id=room_user_list[0])

    return render(request, "create_chat.html", {
        "room": dict_of_users_href,
        "room_name": room_name,
        "username": username, "users": users,
        "room_user_name": room_user_name
    })
