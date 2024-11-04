from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RegsiterForm


# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegsiterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("auth.login"))
    else:
        form = RegsiterForm()
    return render(request, "accounts/register.html", {"form": form})


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/login.html")
