from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "posts/index.html")
