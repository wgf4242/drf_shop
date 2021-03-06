"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet, AliPayView
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from users.views import SmsCodeGViewSet, UserViewSet

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置category的url
router.register(r'categorys', CategoryViewSet, base_name='category')

router.register(r'codes', SmsCodeGViewSet, base_name='codes')

router.register(r'users', UserViewSet, base_name='users')

# 收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')

# 留言
router.register(r'messages', LeavingMessageViewSet, base_name='messages')

# 收货地址
router.register(r'address', AddressViewSet, base_name='address')

# 购物车
router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')

# 订单相关
router.register(r'orders', OrderViewSet, base_name='orders')

# 轮播图url
router.register(r'banners', BannerViewSet, base_name='banners')

# 首页商品系列数据
router.register(r'indexGoods', IndexCategoryViewSet, base_name='indexGoods')

# router.register(r'hotsearchs', HotSearchViewset, base_name='hotsearchs')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 商品列表页
    url(r'^', include(router.urls)),

    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    url(r'docs/', include_docs_urls(title="生鲜Title")),

    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt 认证接口
    # url(r'^jwt_auth/', obtain_jwt_token),
    url(r'^login/$', obtain_jwt_token),
    # url(r'^api/authenticate/', obtain_jwt_token),\
    url(r'^alipay/return/', AliPayView.as_view(), name="alipay"),

    url('', include('social_django.urls', namespace='social'))

]
