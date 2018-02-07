from user_operation.models import UserFav
from django.shortcuts import render
from rest_framework import mixins, viewsets

# Create your views here.
from user_operation.serializsers import UserFavSerializer


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
