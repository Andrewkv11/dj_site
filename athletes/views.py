from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Athletes, Category
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .utils import *

# Create your views here.
menu = [{'title': "О сайте", 'url_name': "about"},
        {'title': "Добавить статью", 'url_name': "add_page"},
        {'title': "Обратная связь", 'url_name': "contact"},
        {'title': "Войти", 'url_name': "login"},
        ]


# Без испольования тегов
# def index(request):
#     posts = Athletes.objects.all()
#     cats = Category.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cats': cats,
#         'cat_selected': 0,
#     }
#     return render(request, 'athletes/index.html', context=context)
#
#
# def show_category(request, cat_id):
#     posts = Athletes.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#
#     if len(posts) == 0:
#         raise Http404
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cats': cats,
#         'cat_selected': cat_id,
#     }
#     return render(request, 'athletes/index.html', context=context)

# С использованием тегов
# def index(request):
#     posts = Athletes.objects.all()
#     context = {
#         'posts': posts,
#         # 'menu': menu, вынесено в тег
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'athletes/index.html', context=context)

# def show_category(request, cat_slug):
#     posts = Athletes.objects.filter(cat__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404
#     context = {
#         'posts': posts,
#         # 'menu': menu, вынесено в тег
#         'title': 'Отображение по рубрикам',
#         'cat_selected': Category.objects.get(slug=cat_slug).pk,
#     }
#     return render(request, 'athletes/index.html', context=context)

# Класс представление index
# class AthletesHome(ListView):
#     model = Athletes
#     template_name = 'athletes/index.html'
#     # Указываем context_object_name чтобы в шаблоне не менять posts на object_name
#     context_object_name = 'posts'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['menu'] = menu  меню сделано через тег добавлять не нужно
#         context['title'] = 'Главная страница'
#         context['cat_selected'] = 0
#         return context
#
#     def get_queryset(self):
#         return Athletes.objects.filter(is_published=True)

# Класс на основе Mixinov
class AthletesHome(DateMixin, ListView):
    model = Athletes
    template_name = 'athletes/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Athletes.objects.filter(is_published=True).select_related('cat')


# Класс представление show_categories
# class AthletesShowCategory(ListView):
#     model = Athletes
#     template_name = 'athletes/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # if len(context['posts']) == 0: вместо этого строка allow_empty
#         #     raise Http404
#         context['title'] = 'Категория-' + str(context['posts'][0].cat)
#         context['cat_selected'] = context['posts'][0].cat_id
#         return context
#
#     def get_queryset(self):
#         return Athletes.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
#   Через mixin
class AthletesShowCategory(DateMixin, ListView):
    model = Athletes
    template_name = 'athletes/index.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория-' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Athletes.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


# До создания классов-моделей
# def about(request):
#     # contact_list = Athletes.objects.all()
#     # paginator = Paginator(contact_list, 3)
#     #
#     # page_number = request.GET.get('page')
#     # page_obj = paginator.get_page(page_number)
#     # return render(request, 'athletes/about.html', context={'title': 'О сайте', 'menu': menu, 'page_obj': page_obj})
#     return render(request, 'athletes/about.html', context={'title': 'О сайте', 'menu': menu})

class AboutPage(DateMixin, View):
    def get(self, request):
        return render(request, 'athletes/about.html', self.get_user_context(title='О сайте'))


# До создания формы связанной с моделью
# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 Athletes.objects.create(**form.cleaned_data)
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'athletes/addpage.html', context={'form': form, 'title': 'Добавление статьи'})

# Без класса представлений
# @login_required Для авторизации при переходе по url
# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'athletes/addpage.html', context={'form': form, 'title': 'Добавление статьи'})

# С классом представлений
# class AthletesAddPage(CreateView):
#     form_class = AddPostForm
#     template_name = 'athletes/addpage.html'
#     success_url = reverse_lazy('home')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Добавление статьи'
#         return context
# С миксином
class AthletesAddPage(LoginRequiredMixin, DateMixin, CreateView):
    form_class = AddPostForm
    template_name = 'athletes/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи', cat_selected=None)
        return dict(list(context.items()) + list(c_def.items()))


# def contact(request):
#     return HttpResponse("Обратная связь")

class ContactFormView(DateMixin, FormView):
    form_class = ContactForm
    template_name = 'athletes/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# def login(request):
#     return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# Без классов представлений
# def show_post(request, post_slug):
#     post = get_object_or_404(Athletes, slug=post_slug)
#     context = {
#         'post': post,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'athletes/post.html', context=context)

# Представление классов
# class AthletesShowPost(DetailView):
#     model = Athletes
#     template_name = 'athletes/post.html'
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'
#
#     # pk_url_kwarg =
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = context['post']
#         context['cat_selected'] = context['post'].cat_id
#         return context
#     Через Mixin
class AthletesShowPost(DateMixin, DetailView):
    model = Athletes
    template_name = 'athletes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    # pk_url_kwarg =

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DateMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'athletes/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DateMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'athletes/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    # Можно в settings.py указать внизу LOGIN _REDIRECT_URL
    # def get_success_url(self):
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
