from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

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

    def get_context_data(self, *, object_list=None, **kwargs):
        page_num = int(kwargs.get('page', '1'))
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        results = paginator.page(page_num)
        context = {
            'count': paginator.count,
            'pages': paginator.num_pages,
            'prev': results.previous_page_number() if results.has_previous() else 0,
            'next': results.next_page_number() if results.has_next() else 0,
            'results': list(results.object_list),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
