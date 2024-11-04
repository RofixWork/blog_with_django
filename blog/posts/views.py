from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PostForm
from .models import Post


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "posts/home.html")


def index(request: HttpRequest) -> HttpResponse:
    current_user_posts = Post.objects.filter(user=request.user)
    posts = Paginator(current_user_posts.order_by("-updated_at"), 2).get_page(2)
    print(posts)
    return render(
        request,
        "posts/index.html",
        {"posts": posts, "count": current_user_posts.count()},
    )


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
