from django.db.models import Count
from django.core.cache import cache
from athletes.models import Category

menu = [{'title': "О сайте", 'url_name': "about"},
        {'title': "Добавить статью", 'url_name': "add_page"},
        {'title': "Обратная связь", 'url_name': "contact"},
        ]


class DateMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('athletes'))
            cache.set('cats', cats, 60)
        context['cats'] = cats
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

# # Класс представление index
# class AthletesHome(DateMixin, ListView):
#     model = Athletes
#     template_name = 'athletes/index.html'
#     context_object_name = 'posts'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Главная страница")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_queryset(self):
#         return Athletes.objects.filter(is_published=True)
#
#
# class AthletesAddPage(CreateView):
#     form_class = AddPostForm
#     template_name = 'athletes/addpage.html'
#     success_url = reverse_lazy('home')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Добавление статьи')
#         return dict(list(context.items()) + list(c_def.items()))

#
#
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
#
# # Класс представление show_categories
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
#
# class AthletesShowPost(DetailView):
#     model = Athletes
#     template_name = 'athletes/post.html'
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'
#     # pk_url_kwarg =
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = context['post']
#         context['cat_selected'] = context['post'].cat_id
#         return context
