from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork

class MoviesListApi(BaseListView):
    http_method_names = ['get']

    model = Filmwork

    def get_queryset(self):
        return  # Сформированный QuerySet

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        return JsonResponse({})