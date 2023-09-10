from django_filters import FilterSet
from .models import Server
from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class ServerFilter(FilterSet):
    class Meta:
        model = Server
        fields = {
            'title': ['icontains'],
            'owner__username': ['icontains'],
            'description': ['icontains'],
            'category__title': ['icontains'],
            'category__description': ['icontains'],
        }


class ServerFilterCount(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        q = request.query_params.get('q', None)
        if q:
            return queryset[:int(q)]
        return queryset


class IsOwnerOrMemberFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        by_user = request.query_params.get('by_user') == 'true'
        if by_user:
            return queryset.filter(Q(owner=request.user) | Q(members=request.user.id))
        return queryset


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
