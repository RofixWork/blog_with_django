from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import RegsiterForm


# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    form = RegsiterForm()
    return render(request, "accounts/register.html", {"form": form})
