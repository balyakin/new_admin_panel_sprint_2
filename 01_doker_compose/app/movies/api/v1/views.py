from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return Filmwork.objects.prefetch_related('genres', 'person') \
            .values().all().annotate(genres=ArrayAgg('genres__name',
                                                     distinct=True),
                                     actors=ArrayAgg('persons__full_name',
                                                     filter=Q(personfilmwork__role__icontains='Actor'),
                                                     distinct=True),
                                     directors=ArrayAgg('persons__full_name',
                                                        filter=Q(personfilmwork__role__icontains='Director'),
                                                        distinct=True),
                                     writers=ArrayAgg('persons__full_name',
                                                      filter=Q(personfilmwork__role__icontains='Writer'),
                                                      distinct=True)
                                     )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        print(kwargs)
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        page_num = self.request.GET.get('page', 1)
        if page_num == 'last':
            page_num = paginator.num_pages

        results = paginator.page(page_num)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': results.previous_page_number() if results.has_previous() else None,
            'next': results.next_page_number() if results.has_next() else None,
            'results': list(results.object_list),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        id = kwargs['object'].get('id')
        queryset = self.get_queryset()
        result = queryset.filter(Q(id=id))
        print(result)
        return result.values()[0] if result else {}
