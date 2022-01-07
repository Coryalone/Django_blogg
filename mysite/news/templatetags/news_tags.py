from django import template
from django.core.cache import cache

from django.db.models import Count, F

from news.models import Category

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(cnt=Count('news', filter=(F('news__is_published')))).filter(cnt__gt=0)
        cache.set('categories', categories, 30)
    return {'categories': categories}
