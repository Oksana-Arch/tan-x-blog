from django.shortcuts import render, get_object_or_404
from .models import *
from .utils import *
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.template.context_processors import csrf
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.template import Context, loader

from .forms import *


# Create your views here.
# Виды для работы со статьями
def post_list(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)

    is_paginator = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_obj': page,
        'is_paginator': is_paginator,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'blog/post_list.html', context=context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug__iexact=slug)
    user = auth.get_user(request)
    comments = post.comments.filter(moderate=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author_id = user.id
            new_comment.save()
            return redirect(post)

    else:
        comment_form = CommentForm
    return render(request, 'blog/post.html', context={'post': post, 'comments': comments,
                                                      'new_comment': new_comment,
                                                      'comment_form': comment_form,
                                                      'admin_obj': post, 'detail': True}, )




class PostCreate(ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create.html'
    raise_exception = True


class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update.html'
    raise_exception = True


class PostDelete(ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    redirect_url = 'post_list_url'
    raise_exception = True


# Выды для работы с тегами

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag.html'


class TagCreate(ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = 'blog/tag_update.html'
    raise_exception = True


class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = "post_list_url"
    raise_exception = True


# Виды для работы с категориями
def categ_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/categories_list.html', context={'categories': categories})


class CategoryDetail(ObjectDetailMixin, View):
    model = Category
    template = 'blog/category.html'


class CategoryCreate(ObjectCreateMixin, View):
    form_model = CategoryForm
    template = 'blog/category_create.html'
    raise_exception = True


class CategoryUpdate(ObjectUpdateMixin, View):
    model = Category
    form_model = CategoryForm
    template = 'blog/category_update.html'
    raise_exception = True


class CategoryDelete(ObjectDeleteMixin, View):
    model = Category
    template = 'blog/category_delete.html'
    redirect_url = 'post_list_url'
    raise_exception = True


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recomends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', context={'post': post, 'form': form, 'sent': sent})

def post_search(request):
    form2 = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form2 = SearchForm(request.GET)
        if form2.is_valid():
            query = form2.cleaned_data['query']
            seach_vector = SearchVector('title', weight='A') + SearchVector('body', weight='C') + SearchVector(
                'comment', weight='B')
            seach_query = SearchQuery(query)
            results = Post.objects.annotate(search=seach_vector, rank=SearchRank(seach_vector, seach_query)).filter(
                rank__gte=0.1).order_by('-rank')
    return render(request, 'blog/search.html', {'form2': form2, 'query': query, 'results': results})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # subject = form.cleaned_data['subject']
            # message = form.cleaned_data['message']
            # copy = form.cleaned_data['copy']
            cd = form.cleaned_data
            recepients = ['jroofj@gmail.com']
            copy = cd['copy']
            subject = '{} sent you a message with a subject "{}"'.format(cd['name'], cd['subject'])
            message = '{} sent you a message: "{}" from email {}'.format(cd['name'], cd['message'], cd['email'])
            if copy:
                recepients.append(cd['email'])
            try:
                send_mail(subject, message, 'jroofj@gmail.com', recepients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponseRedirect('/blog/thanks/')
    else:
        form = ContactForm
    return render(request, 'blog/contact.html', context={'form': form})


def thanks(request):
    thanks = 'thanks'
    return render(request, 'blog/thanks.html', context={'thanks': thanks})


def archive(request):

    post = Post.objects.all().filter(status='draft')

    paginator = Paginator(post, 3)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)

    is_paginator = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_obj': page,
        'is_paginator': is_paginator,
        'next_url': next_url,
        'prev_url': prev_url,
        'post': post
    }

    return render(request, 'blog/archive.html', context=context)

def error404(request, exception):
    return render(request, '404.html')

def error404_test(request):
    return render(request, '404.html')

def markdown(request):
    return render(request, 'blog/markdown.html')

def index(request):
    posts = Post.published.all().order_by('-publish')[0:4]
    return render(request, 'blog/index.html', context={'posts': posts})
