from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, mixins, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Server
from .serializer import ServerSerializer
from .filters import ServerFilter, ServerFilterCount, IsOwnerOrMemberFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


# Create your views here.

class ServerList(mixins.ListModelMixin, GenericAPIView):
    queryset = Server.objects.all()

    serializer_class = ServerSerializer
    # authentication_classes = [JWTAuthentication, SessionAuthentication]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['category__title', 'category__description']
    ordering_fields = ['category__title', 'title']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class ServerListApi(ListAPIView):
#     queryset = Server.objects.all()
#     serializer_class = ServerSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = ServerFilter

class ServerListApi(ListAPIView):
    """Returns a List of servers
    """
    model = Server
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # ServerFilterCount should be last because it slices the query which causes an error
    filter_backends = [SearchFilter, OrderingFilter, IsOwnerOrMemberFilter, ServerFilterCount, ]

    # search param can be divided in url by comma => api/?search=red,bruh,wood
    search_fields = ['category__title', 'category__description']
    ordering_fields = ['category__title', 'title']

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases
    #     for the currently authenticated user.
    #     """
    #     user = self.request.user
    #     return Server.objects.filter(purchaser=user)

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases for
    #     the user as determined by the username portion of the URL.
    #     """
    #     username = self.kwargs['username']
    #     return Server.objects.filter(purchaser__username=username)

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = Purchase.objects.all()
    #     username = self.request.query_params.get('username')
    #     if username is not None:
    #         queryset = queryset.filter(purchaser__username=username)
    #     return queryset

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = Server.objects.all()
    #     q = self.request.query_params.get('q')
    #     if q is not None:
    #         queryset = queryset[:int(q)]
    #     return queryset


class ServerRetrieve(RetrieveAPIView):
    model = Server
    lookup_field = 'pk'
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, IsOwnerOrMemberFilter]
