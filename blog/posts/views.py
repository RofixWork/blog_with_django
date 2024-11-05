from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import PostForm
from .models import Post


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    page_number = request.GET.get("p", 1)
    posts = Post.objects.all().order_by("-created_at")
    paginate_posts = Paginator(posts, 10).get_page(page_number)
    return render(
        request, "posts/home.html", {"posts": paginate_posts, "count": posts.count()}
    )


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth.login"))

    page_number = request.GET.get("p", 1)
    current_user_posts = Post.objects.filter(user=request.user)
    posts = Paginator(current_user_posts.order_by("-updated_at"), 4).get_page(
        page_number
    )
    return render(
        request,
        "posts/index.html",
        {"posts": posts, "count": current_user_posts.count()},
    )


def create(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth.login"))

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


def update(request: HttpRequest, id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth.login"))

    post: Post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("posts.index"))
    else:
        form = PostForm(instance=post)
    return render(
        request, "posts/update.html", {"form": form, "post_image": post.image}
    )


def delete(request: HttpRequest, id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth.login"))

    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse("posts.index"))


def show(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=id)
    print(post.tags.all())
    return render(request, "posts/show.html", {"post": post})
