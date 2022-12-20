from django import template
from athletes.models import *

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('athletes/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.simple_tag()
def get_menu():
    menu = [{'title': "О сайте", 'url_name': "about"},
            {'title': "Добавить статью", 'url_name': "add_page"},
            {'title': "Обратная связь", 'url_name': "contact"},
            {'title': "Войти", 'url_name': "login"},
            ]
    return menu


@register.inclusion_tag('athletes/show_menu.html')
def show_menu():
    menu = [{'title': "О сайте", 'url_name': "about"},
            {'title': "Добавить статью", 'url_name': "add_page"},
            {'title': "Обратная связь", 'url_name': "contact"},
            {'title': "Войти", 'url_name': "login"},
            ]
    return {'menu': menu}
