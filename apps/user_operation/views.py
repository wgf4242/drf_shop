from rest_framework.authentication import SessionAuthentication

from user_operation.models import UserFav
from django.shortcuts import render
from rest_framework import mixins, viewsets

# Create your views here.
from user_operation.serializsers import UserFavSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.permissions import IsAuthenticated

from utils.permisstions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
