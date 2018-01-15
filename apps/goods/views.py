from django.views.generic import ListView
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .serializers import GoodsSerializer
from .models import Goods


class GoodsListView(ListCreateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

# class GoodsListView(APIView):
#     """
#     List all goods
#     """
#
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)
