from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.context_processors import request
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import FavouritePost, Post

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    favourite_post = None
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    try:
        if request.user.is_authenticated:
            favourite_post = FavouritePost.objects.get(
                user=request.user, post=post
            )
    except FavouritePost.DoesNotExist:
        pass
    return render(
        request,
        'blog/post/detail.html',
        {
            'is_favourite': favourite_post is not None,
            'post': post
        }
    )

def add_favourite(request, id):
    """ A view to add a post to favourites. Redirects to post detail when favourite added. """
    post = get_object_or_404(Post, id=id)
    FavouritePost.objects.get_or_create(
        user=request.user, post=post
    )
    return HttpResponseRedirect(post.get_absolute_url())

@login_required
def favourites(request):
    """ A view to list all favourite posts. """
    favourite_posts = Post.objects.filter(
        id__in=FavouritePost.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)
    )
    return render(
        request,
        'blog/post/favourites.html',
        {'favourite_posts': favourite_posts}
    )

def post_share(reqeust,post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
        }
    )




















