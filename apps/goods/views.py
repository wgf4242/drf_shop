from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Goods
# Create your views here.
from .serializers import GoodsSerializer


class GoodsListView(APIView):
    """
    List all goods
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)
