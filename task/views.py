from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User



def home(request):
    context = {}
    return render(request, "home.html", context)