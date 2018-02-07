import django_filters
from django.db.models import Q
from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte', help_text="最低价格")
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    # name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter', label="根据id查找类别下的所有商品")

    def top_category_filter(self, queryset, name, value):
        """
        查找第一类别下的所有商品
        """
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot']
