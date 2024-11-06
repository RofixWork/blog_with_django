from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Comment, Post


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
    message_success = request.COOKIES.get("success_message", None)
    return render(
        request,
        "posts/index.html",
        {
            "posts": posts,
            "count": current_user_posts.count(),
            "success_message": message_success,
        },
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
    response = render(request, "posts/create.html", {"form": form})
    response.set_cookie("success_message", "Post has been added successfully...", 5)
    return response


def update(request: HttpRequest, id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth.login"))

    post: Post = get_object_or_404(Post, id=id, user=request.user)
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("posts.index"))
    else:
        form = PostForm(instance=post)
    response = render(
        request, "posts/update.html", {"form": form, "post_image": post.image}
    )
    response.set_cookie("success_message", "Post has been updated successfully...", 5)
    return response


def delete(request: HttpRequest, id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth.login"))

    post = get_object_or_404(Post, id=id, user=request.user)
    if request.method == "POST":
        post.delete()
        response = HttpResponseRedirect(reverse("posts.index"))
        response.set_cookie(
            "success_message", "Post has been removed successfully...", 5
        )
        return response


def show(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=id)
    # save comment
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment: Comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse("posts.show", kwargs={"id": post.id}))
    else:
        form = CommentForm()
    return render(
        request,
        "posts/show.html",
        {
            "post": post,
            "form": form,
            "comments": post.comment_set.all().order_by("-id"),
        },
    )


def profile(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth.login"))

    page_number = request.GET.get("p", 1)
    current_user_posts = Post.objects.filter(user=request.user)
    posts = Paginator(current_user_posts.order_by("-updated_at"), 4).get_page(
        page_number
    )
    return render(
        request,
        "posts/profile.html",
        {"posts": posts, "count": current_user_posts.count()},
    )


def remove_comment(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST" and request.user.is_authenticated:
        comment: Comment = get_object_or_404(Comment, id=id, user=request.user)
        post_id = comment.post.id
        comment.delete()
        return HttpResponseRedirect(reverse("posts.show", kwargs={"id": post_id}))
