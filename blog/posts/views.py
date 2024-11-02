from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PostForm
from .models import Post


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "posts/index.html")


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("posts.index"))
    else:
        form = PostForm()
    return render(request, "posts/create.html", {"form": form})
