from django.contrib import messages
# from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all().order_by('-id')
    p = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    # try:
    #     page_obj = p.get_page(page_number)
    # except PageNotAnInteger:
    #     page_obj = p.page(1)
    # except EmptyPage:
    #     page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    return render(request, 'index.html', context)


def post_detail(request, id):
    post = Post.objects.get(id=id)
    comments = post.comment_set.all().order_by('-id')
    if request.method == "POST":
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.post = post
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully post comment")
            return redirect(request.path_info)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Post created successfully")
            return redirect('index')
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {'form': form})


@login_required(login_url='login')
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post edited successfully")
            return redirect('post_detail', id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/edit_post.html", {'form': form, 'post': post})


@login_required(login_url='login')
def delete_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post Deleted successfully")
        return redirect('index')
    return render(request, "blog/delete_post.html", {'post': post})


@login_required(login_url='login')
def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    rid = comment.post.id
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment edited successfully")
            return redirect('post_detail', id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/edit_comment.html", {'form': form, 'rid': rid})


@login_required(login_url='login')
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    rid = comment.post.id
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully")
        return redirect('post_detail', id=rid)
    return render(request, "blog/delete_comment.html", {'rid': rid})
