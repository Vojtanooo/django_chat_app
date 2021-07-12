from chat_app.models import User, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from .forms import UserForm, UserUpdateForm, ProfileUpdateForm


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
            return redirect("room", room_name="Welcome")
        else:
            messages.error(request, f"Username or Password is incorect!")

    return render(request, "login.html")


@login_required()
def room(request, room_name):
    username = request.user
    User = get_user_model()
    users = User.objects.all()

    dict_of_users_href = {}
    for user in users:
        if not user == username:
            dict_of_users_href[user] = "chat{}_{}".format(
                *sorted([username.id, user.id]))

    if room_name == "Welcome":
        room_user_name = "Welcome"
    else:
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


def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Yout Account has been updated!")
            return redirect("room", room_name="Welcome")
        else:
            print(u_form.errors.as_data())
            print(p_form.errors.as_data())
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }

    return render(request, "profile.html", context)
