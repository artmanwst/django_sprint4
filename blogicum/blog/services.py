
from django.core.paginator import Paginator, Page
from django.db.models.query import QuerySet
from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def get_posts() -> QuerySet[Post]:
    '''Отправляет запрос в БД формата:
    Вход - None
    Возвращает - QuerySet[Post]
    '''
    return Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def queryset_annotate(querset: QuerySet[Post]) -> QuerySet[Post]:
    '''Добавляет аннотацию для подсчета количества комментариев
    '''
    return (querset
            .annotate(comment_count=Count('comment'))
            .order_by('-pub_date')
            )


def get_paginator(objects: QuerySet,
                  page_number: int,
                  posts_on_page: int) -> Page:
    '''Пагинатор:
    Вход - objects: QuerySet
    Возвращает - Page
    '''
    paginator = Paginator(objects, posts_on_page)
    return paginator.get_page(page_number)
