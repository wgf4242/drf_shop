[TOC]

pillow 处理图片的包。

# TODO

保存密码这里有问题，createsuperuser后登录不了。

# FAQ

1. Model class MyModel doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS

        没有 mark as source root的原因。


# 第3章 model设计和资源导入
## 3-2 user model设计 

1. 新建数据库 mxshop

        新建 apps, db_tools, extra_apps, media 
        右击 apps - mark as source root
        右击 extra_apps  - mark as source root
        
        

2. settings.py 设置
        
        # settings.py 前面添加
        import sys
        sys.path.insert(0, BASE_DIR)
        sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
        sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
        加入后即可import 时不用从 app. 开始写，如 app.users直接写成users

3. PyCharm: Tools - Run manage.py Task, 创建以下app后移到apps下

    startapp users
    startapp goods
    startapp trade
    startapp user_operation

import的规范

    1 先引入系统包
    2 再引入第三方包
    3 最后自己的包

models相关

注意要用 `models.DateField(default=datetime.now)`，写成 `now()` 则是编译时的时间

* 替换系统用户

        # settings.py , UserProfile位置是在 users.models.UserProfile
        AUTH_USER_MODEL = 'users.UserProfile'

## 3-3 goods的model设计
通过一个model完成所有级别的类。定义从属关系，不定死关系。 指向自己这张表---`"self"`
    
    prarent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                         related_name="sub_cat") #related_name作用后边查询用


* 将 app 添加到 INSTALLED_APPS

    'DjangoUeditoro', 'users', 'goods', 'trace', 'user_operation'添加到 settings
    
## 3-4 trade交易的model设计

引入 user model 的方法

    from django.contrib.auth import get_user_model
    User = get_user_model()

## 3-5 用户操作的model设计

## 3-6 migrations原理及表生成

通过 appConfig进行配置。

    'users.apps.UsersConfig',                 
    'goods.apps.GoodsConfig',                 
    'trade.apps.TradeConfig',                 
    'user_operation.apps.UserOperationConfig',

生成数据库表

    python manage.py makemigrations
    python manage.py migrate
    
Django 如何知道我要运行哪个修改呢---记录在数据库的 django_migrationss 这张表。
 py
要想重新生成goods，按如下步骤：
    
1. 将 goods 表全部删除
2. 将 django_migrationss 表中关于 goods 的记录删除掉
3. 重新运行脚本

## 3-7 xadmin后台管理系统的配置

1. 将源的 xadmin 复制到 extra_apps 下
2. 将源码各apps下的adminx.py 复制到本项目相应的各apps中。
3. 配置 xadmin 到settings中
    
    'crispy_forms',
    'xadmin',

4. 安装 xadmin 的依赖包

        官方 github xadmin ，找到 requirements 依赖包
        https://github.com/sshwsfc/xadmin
        https://github.com/sshwsfc/xadmin/blob/master/requirements.txt
        pip install django-crispy-forms django-import-export django-reversion django-formtools future httplib2 six xlwt xlsxwriter

5. createsuperuser admin/admin123
6. 启动调试
7. 把xadmin的各app模块修改为中文显示
    
        # apps.py
        verbose_name = '商品'

## 3-8 导入商品类别数据

独立使用 django的model

    import sys
    import os
    
    pwd = os.path.dirname(os.path.relpath(__file__))
    sys.path.append(pwd + "../")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")
    
    import django
    django.setup()
    
    from goods.models import GoodsCategory
    from db_tools.data.category_data import row_data
    
    # 三级对象导入示例
    for lev1_cat in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.code = lev1_cat["code"]
    lev1_instance.name = lev1_cat["name"]
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_instance = GoodsCategory()
        lev2_instance.code = lev2_cat["code"]
        lev2_instance.name = lev2_cat["name"]
        lev2_instance.category_type = 2
        lev2_instance.parent_category = lev1_instance
        lev2_instance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_instance = GoodsCategory()
            lev3_instance.code = lev3_cat["code"]
            lev3_instance.name = lev3_cat["name"]
            lev3_instance.category_type = 3
            lev3_instance.parent_category = lev2_instance
            lev3_instance.save()


## 3-9 导入商品和商品类别数据-2

媒体文件，图片的访问配置。将media目录添加到至默认图片访问路径

1. settings 添加 MEDIA_ROOT

        MEDIA_URL = "/media/"
        MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    
2. url.py

        from MxShop.settings import MEDIA_ROOT
        from django.views.static import serve
        
        urlpatterns = [
            url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
        ]
                
# 第4章  vue的结构和restful api介绍\

## 4-1 restful api介绍.mp4

前后端分离
1. pc, app, pad 多端适应
2. SPA开发模式开始流行
3. 前后端开发职责不清
4. 开发效率问题，前后端互相等待
5. 前端一直配合着后端，能力受限
6. 后台开发语言放模板高度耦合，导致开发语言依赖严重。

前后端分离缺点
1. 前后端学习门槛增加
2. 数据依赖导致文档重要性增加
3. 前端工作量加大
4. SEO的难度加大
5. 后端开发模式迁移增加成本

restful api 目前是前后端分离最佳实践
1. 轻量，直接通过http，不需要额外的，post/get/put/delete操作
2. 面向资源，一目了然，具有自解释性
3. 数据描述简单，一般通过json或者xml进行通信
restful api 重要概念
1. 概念 http://www.ruanyifeng.com/blog/2011/09/restful.html
2. restful 实践 http://www.ruanyifeng.com/blog/2014/05/restful_api.html

HTTP动词：常用的HTTP动词有下面五个（括号里是对应的SQL命令）。

    GET（SELECT）：从服务器取出资源（一项或多项）。
    POST（CREATE）：在服务器新建一个资源。
    PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
    PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
    DELETE（DELETE）：从服务器删除资源。

状态码（Status Codes）
服务器向用户返回的状态码和提示信息，常见的有以下一些（方括号中是该状态码对应的HTTP动词）。

    200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
    201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
    202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
    204 NO CONTENT - [DELETE]：用户删除数据成功。
    400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
    401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
    403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
    404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
    406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
    410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
    422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
    500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
    
# 第5章 商品列表页

## 5-1 django的view实现商品列表页
    
    # url.py
    url(r'goods/')尽量用复数形式 

Chrome 下载 jsonview 插件

用django手动引入时
1. 需要指定 content_types HttpResponse(json.dumps(json_list), content_type="application/json") ， 大量时容易出错且麻烦
2. 而且 add_time 不能进行序列化

## 5-2 django的serializer序列化model

1. django.forms.models import model_to_dict 来转换为json对象，但仍然不能处理datefield
2. 使用serializers.serialize进行序列化

        from django.core import serializers
        json_data = serializers.serialize("json", goods)
        # return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(json_data, safe=False)
        
为什么还要用 REST Framwork？

    1. drf已经做好了 添加 media 前缀的功能
    2. 文档的生成
    3. 输入的检测

## 5-3 apiview方式实现商品列表页-1

1.pip install coreapi django-guardian 

pip install coreapi 如果出现了utf8错误。

    虚拟环境\Lib\site-packages\pip\compat\__init__.py 75行改为 s.decode('gbk')
    pip uninstall coreapi markupsafe
    pip install coreapi markupsafe

2.引入文档
    
    
    # urls.py
    from rest_framework.documentation import include_docs_urls
    url(r'docs/', include_docs_urls(title="生鲜Title")),

3.settings引入 'rest_framework',

    INSTALLED_APPS = [ 'rest_framework', ]

4.写view和serializers.py， 运行访问 http://127.0.0.1:8000/goods/
    
    如果运行过程中__str__ returned non-string (type NoneType) ，是因为 createsuperuser时没有 name 属性，于是报错
    或者在UesrProfile return self.username 
    
## 5-5 drf的modelserializer实现商品列表页功能

使用ModelSerializer，添加自定义字段category
    
    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = GoodsCategory
            fields = "__all__"
    class GoodsSerializer(serializers.ModelSerializer):
        category = CategorySerializer()
        class Meta:
            model = Goods
            fields = "__all__"

## 5-6 GenericView方式实现商品列表页和分页功能详解.mp4

1.ModelMixin, generic.GenericAPIView 实现, 这和ListAPIView源码是一样的

    class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
        queryset = Goods.objects.all()[:10]
        serializer_class = GoodsSerializer
        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

2.实现分页

* 在 settings.py 中进行设置, 可以在 rest_framework\settings.py中的 DEFAULTS 中查看全部的配置

        REST_FRAMEWORK = {
            'PAGE_SIZE': 10
        }
        
    访问 http://127.0.0.1:8000/goods/ 出现 next 字段，虽然next可以自己拼，但有一个好处，可以知道带了什么参数

* 如何定置分页，使用自定义的pagination_class,并取消settings中的设置
    
        class StandardResultsSetPagination(PageNumberPagination):
            page_size = 10
            page_size_query_param = 'page_size'
            page_query_param = "page"
            max_page_size = 100
        class GoodsListView(generics.ListAPIView):
            queryset = Goods.objects.all()
            serializer_class = GoodsSerializer
            pagination_class = StandardResultsSetPagination

    前台可以使用 page_size 来自定义每页大小

## 5-7 viewsets和router完成商品列表页

查看源码 viewsets.py, `GenericViewSet(ViewSetMixin, generics.GenericAPIView)`:在APIView上添加了ViewSetMixin，重写了 `as_view` 和 `initialize_request`。

initialize_request 中set了多个action，在动态设置 serializer 时有很多的好处。

* 使用 ViewSet


        class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet)
        # urls.py
        goods_list = GoodsListViewSet.as_view({ 'get': 'list', })
        urlpatterns = [url(r'goods/$', goods_list, name="goods-list"),]

* 使用 router 配置url


    router = DefaultRouter()
    router.register(r'goods', GoodsListViewSet)
    urlpatterns = [ url(r'^', include(router.urls)),]
    
## 5-8 drf的Apiview、GenericView、Viewset和router的原理分析
    
    GenericViewSet				-drf
        GenericAPIView			-drf
            APIView				-drf
                View			-django
    
    minxin
        CreateModelMixin
        ListModelMixin      --将get,list连接起来
        UpdateModelMixin
        RetrieveModelMixin
        DestroyModelMixin
    
rest_framework\generics.py 中查看源码了解各种View

ViewSet使用了ViewSetMixin，不通过 `def get, post `方法绑定，而通过 router 加 url 配置来绑定。而且 ViewSet 中绑定了多个 action。 

## 5-9 drf的request和response

Requests 的一些属性

    .data -- 只会将 POST 和 FILES 放进来
    .query_params get请求的参数
    .parsers 解析各种类型数据 android, ios
    .user
 
Responses 支持各种类型的返回
 
    data: 返回数据
    status: 状态码
    template_name: A template name to use if HTMLRenderer is selected.
    headers: A dictionary of HTTP headers to use in the response.
    content_type: The content type of the response. Typically, this will be set automatically by the renderer as determined by content negotiation, but there may be some cases where you need to specify the content type explicitly.

## 5-10 drf的过滤

通过get_queryset,中间可以加逻辑，和`queryset = Goods.objects.all()` 效果一样

    def get_queryset(self):
        return Goods.objects.filter(shop_price__gt=100)

手动添加逻辑来过滤结果

    def get_queryset(self):
        queryset = Goods.objects.all()
        price_min = self.request.query_params.get("price_min", 0)
        if price_min:
            queryset = queryset.filter(shop_price__gt=int(price_min))
        return queryset

http://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend

https://django-filter.readthedocs.io/en/master/guide/usage.html#the-model
1. 安装 django-filter, settings中添加 

        INSTALLED_APPS = ['django_filters']
        REST_FRAMEWORK = { 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',) } #默认就是，不添加也可以

        # 一个简单的使用默认的 Filter
        class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
            filter_backends = (DjangoFilterBackend,)
            filter_fields = ('name', 'shop_price')
    
2. 自定义Filter    

新建 filters.py, 添加filter_class = GoodsFilter

    class GoodsFilter(django_filters.rest_framework.FilterSet):
        price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gt')
        price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lt')
        class Meta:
            model = Goods
            fields = ['price_min', 'price_max']
            
    # views.py
    class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
        queryset = Goods.objects.all()
        serializer_class = GoodsSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = (DjangoFilterBackend,)
        filter_class = GoodsFilter
    
## 5-11 drf的搜索和排序

模糊搜索名字

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']

配置drf的搜索

http://www.django-rest-framework.org/api-guide/filtering/#searchfilter

SearchFilter    
    
    from rest_framework import filters
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'goods_brief', 'goods_desc')

    # search_fields
    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's MySQL backend.)
    '$' Regex search.
    
OrderingFilter

    class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
        queryset = Goods.objects.all()
        serializer_class = GoodsSerializer
        filter_backends = (filters.OrderingFilter,)
        ordering_fields = ('sold_num', 'add_time')

# 第6章  商品类别数据和vue展示
## 6-1 商品类别数据接口-1

类别两个接口
    
    1. 获取全部类别
    2. 获取某一类别
    
完善接口：要注意写文档，在drf生成文档时会比较友好


    class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
        """
        List:
            商品分类列表数据
        """
        
怎样通过一类拿到二类呢？怎样返过来拿

    # models.py
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                             on_delete=models.CASCADE, related_name="sub_cat")
    
用它的relate_name:sub_cat。serializers 里和 model里的名子是一致的。

    class CategorySerializer3(serializers.ModelSerializer):
        class Meta:...
    class CategorySerializer2(serializers.ModelSerializer):
        sub_cat = CategorySerializer3(many=True)
        class Meta:...
    class CategorySerializer(serializers.ModelSerializer):
        sub_cat = CategorySerializer2(many=True)
        class Meta:
            model = GoodsCategory
            fields = "__all__"

获取某一个 mixins.RetrieveModelMixin,
       
    class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

通常的写法 /zoos/id ， 现在drf router已经帮我们做好了，我们直接访问 http://127.0.0.1:8000/category/<id>/ 就可以了

## 6-3 vue展示商品分类数据

跨域问题(CORS)--常见问题

net:ERR_CONNECTION_REFUSED -- 通常是没有开启后台服务

https://github.com/ottoyiu/django-cors-headers

Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS)

Install from **pip**:

    pip install django-cors-headers

and then add it to your installed apps:
    
    INSTALLED_APPS = (
        ...
        'corsheaders',
        ...
    )
    
You will also need to add a middleware class to listen in on responses:

    MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
        ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    ]
    
Also if you are using `CORS_REPLACE_HTTPS_REFERER` it should be placed before Django's `CsrfViewMiddleware` (see more below). 

### CORS_ORIGIN_ALLOW_ALL
If `True`, the whitelist will not be used and all origins will be accepted. Defaults to `False`.

### 导航显示 Tab分类

model中的 `is_tab` 默认是 `False` 并不会显示, 在后台 是否导航勾选起来，在类别描述加上描述，保存。 在前台进行显示。

## 6-4 前端展示商品列表页数据
获取一级分类下的所有商品,用filter的method 来自定义过滤。
    
查找第一类别下的所有商品
    
    class GoodsFilter(django_filters.rest_framework.FilterSet):
        top_category = django_filters.NumberFilter(method='top_category_filter')
        def top_category_filter(self, queryset, name, value):
            return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
                category__parent_category__parent_category_id=value))

# 第7章 用户登录和手机注册
## 7-1 drf的token登录和原理-1.mp4
进入  rest_framework.urls 中的login，进入 LoginView 可以看到是有csrf验证的。访问 http://127.0.0.1:8000/api-auth/ F12，element中可以看到csrf。对表单进行安全验证的--防止跨站攻击。

由于前端有可能是移动端，android等肯定不是一个站点的-肯定跨站。

http://www.django-rest-framework.org/api-guide/authentication/

### Setting the authentication scheme
The default authentication schemes may be set globally, using the `DEFAULT_AUTHENTICATION_CLASSES` setting. For example.

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

### TokenAuthentication Token 验证模式
    
    INSTALLED_APPS = (
        ...
        'rest_framework.authtoken'
    )
    
makemigrations, migrate 后多出一张表 authtoken_token: key created user_id(外键)

在user创建之初时就应该创建好这个token， 一个user对应一个token。

我们新建一个用户看一下：
    
    python manage.py createsuperuser
    admin2
    hello123
    
并没有生成 token ， 代码方式生成的token

    from rest_framework.authtoken.models import Token
    
    token = Token.objects.create(user=...)
    print token.key

配置 url

    from rest_framework.authtoken import views
    urlpatterns += [
        url(r'^api-token-auth/', views.obtain_auth_token)
    ]
    
使用firefox 插件 HttpRequester 来测试

    url; http://127.0.0.1:8000/api-token-auth/
    content: 
    {
    "username":"admin",
    "password":"admin123"
    }
点击post,  生成了一个token

    {"token":"d20a187a9301b84d8e32fde74965b9cb0e4a8c6f"}

在官方文档说明 添加 `Authorization` 到 HTTP header, 以Token前缀开头

    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    
我们在HttpRequester 点击 header，添加它 `Token d20a187a9301b84d8e32fde74965b9cb0e4a8c6f` 到 header, URL: `http://127.0.0.1:8000/goods/`  ，来测试是否能取到user，我们在 `ListModelMixin` 里打一个断点。

并没有取到 user, settings的问题，于是我们将 `TokenAuthentication` 添加到 REST_FRAMEWORK 配置中 
        
        'rest_framework.authentication.TokenAuthentication',

request.data -- 只会将 POST 和 FILES 放进来
request.auth -- 可以取到token值 

* `django.contrib.sessions.middleware.SessionMiddleware` 学习

拦截器 可以写加入 Middleware ,重载 process_request , 判断不是 Chrome返回一个response， Middleware 是从上向下载入， 从下向上返回 Response . 

`Middleware` 会对每一个 request 都会做一个处理的， `REST_FRAMEWORK` 中的auth是验证用户信息的。


`rest_framework.authtoken.views.ObtainAuthToken` 验证方式--取到 `request` 对象中的 `user`，然后 `Token.objects.get_or_create(user=user)` 没有则进行创建。

`TokenAuthentication` 中通过 get_authorization_header(request).split() 取到 token 的值
 
token验证方式的问题
1. 分布式的系统--需要将用户同步过去，比较麻烦。
2. 它没有一个过期时间。

## 7-3 viewsets配置认证类

token auth错误返回 401 错误--认证令牌无效。当用户登录时间过期时访问公众页，返回一个401错误。后端如何解决？

REST_FRAMEWORK 中取消 TokenAuthentication， 将 token 拿到 GoodsListViewSet 来做。(实际是不能配在列表页的)

    class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
        authentication_classes = (TokenAuthentication, )
        
## 7-4 json web token的原理

前后端分离之JWT用户认证

https://www.jianshu.com/p/180a870a308a
 
Json Web Token（JWT）

* Header 头部
头部包含了两部分，token 类型和采用的加密算法
    
    {
      "alg": "HS256",
      "typ": "JWT"
    }
    
它会使用 Base64 编码组成 JWT 结构的第一部分,如果你使用Node.js，可以用Node.js的包base64url来得到这个字符串。

Base64是一种编码，也就是说，它是可以被翻译回原来的样子来的。它并不是一种加密过程。

* Payload 负载

这部分就是我们存放信息的地方了，你可以把用户 ID 等信息放在这里，JWT 规范里面对这部分有进行了比较详细的介绍，常用的由 iss（签发者），exp（过期时间），sub（面向的用户），aud（接收方），iat（签发时间）。

    {
        "iss": "lion1ou JWT",
        "iat": 1441593502,
        "exp": 1441594722,
        "aud": "www.example.com",
        "sub": "lion1ou@163.com"
    }

同样的，它会使用 Base64 编码组成 JWT 结构的第二部分

* Signature 签名

前面两部分都是使用 Base64 进行编码的，即前端可以解开知道里面的信息。Signature 需要使用编码后的 header 和 payload 以及我们提供的一个密钥，然后使用 header 中指定的签名算法（HS256）进行签名。签名的作用是保证 JWT 没有被篡改过。三个部分通过.连接在一起就是我们的 JWT 了，它可能长这个样子，长度貌似和你的加密算法和私钥有关系。

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU3ZmVmMTY0ZTU0YWY2NGZmYzUzZGJkNSIsInhzcmYiOiI0ZWE1YzUwOGE2NTY2ZTc2MjQwNTQzZjhmZWIwNmZkNDU3Nzc3YmUzOTU0OWM0MDE2NDM2YWZkYTY1ZDIzMzBlIiwiaWF0IjoxNDc2NDI3OTMzfQ.PA3QjeyZSUh7H0GfE0vJaKW4LjKJuC3dVLQiY4hii8s

使用JWT后完全通过算法进行加密解密，不需要 token 和 session 表了。

而JWT方式将用户状态分散到了客户端中，可以明显减轻服务端的内存压力。除了用户id之外，还可以存储其他的和用户相关的信息，例如该用户是否是管理员、用户所在的分组等。虽说JWT方式让服务器有一些计算压力（例如加密、编码和解码），但是这些压力相比磁盘存储而言可能就不算什么了。具体是否采用，需要在不同场景下用数据说话。

实例：A用户关注了B用户，给B用户发了一个邮件，点击链接可让B用户关注A用户不需要进行登录。也便于做单点登录

单点登录：单点登录（Single Sign On），简称为 SSO，是目前比较流行的企业业务整合的解决方案之一。SSO的定义是在多个应用系统中，用户只需要登录一次就可以访问所有相互信任的应用系统。比如 *.taobao.com.

## 7-5 json web token方式完成用户认证

https://github.com/GetBlimp/django-rest-framework-jwt

### Installation

    pip install djangorestframework-jwt
    
### Usage
In your `settings.py`, add `JSONWebTokenAuthentication` to Django REST framework's `DEFAULT_AUTHENTICATION_CLASSES`.
    
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
    }

In your `urls.py` add the following URL route to enable obtaining a token via a POST included the user's username and password.

    from rest_framework_jwt.views import obtain_jwt_token
    urlpatterns += [
        url(r'^api-token-auth/', obtain_jwt_token),
    ]

在 HttpRequester 中测试
    
    URL: http://127.0.0.1:8000/jwt_auth/
    POST
    {
    "username":"admin",
    "password":"admin123"
    }
    $ http --json POST http://127.0.0.1:8000/jwt_auth/ username="admin" password="admin123"


Now in order to access protected api urls you must include the ` Authorization: JWT <your_token>` header.在HttpRequester ,headers添加 `Authorization , JWT <token> `测试。

    $ curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/

## 7-6 前端和jwt接口调试

如果 jwt 使用的是django的验证系统，如果我们想使用手机号登录是需要自定义的

https://docs.djangoproject.com/en/2.0/topics/auth/customizing/

    # settings.py
    AUTHENTICATION_BACKENDS = ['users.views.CustomBackend']
    # user.views.py    
    class CustomBackend(ModelBackend):
        def authenticate(self, request, username=None, password=None):
            try:
                user = get_user_model().objects.get(Q(username=username) | Q(mobile=username))
                if user.check_password(password):
                    return user
            except Exception as e:
                return None

http://getblimp.github.io/django-rest-framework-jwt/#additional-settings

JWT是有一个过期时间的，

    from datetime import datetime
    JWT_AUTH = {
        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
        'JWT_AUTH_HEADER_PREFIX': 'JWT',
    }

## 7-7 云片网发送短信验证码

使用request包发送数据

## 7-8 drf实现发送短信验证码接口-1

对VerifyCode表操作

SmsSerializer 为什么不用 model serializer? 

    因为 VerifyCode 中 code是必填字段，在 表单时只需要提交手机号码，并没有code ，会验证失败，所以我们自己写逻辑。

settings 添加

    REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d\{8}$"
    APIKEY = $efuih23u"

serializers.py

    class SmsSerializer(serializers.Serializer):
        mobile = serializers.CharField(max_length=11)
    
        def validate_mobile(self, mobile):
            # 验证手机号码
            # 手机是否注册
            if User.objects.filter(mobile=mobile).count():
                raise serializers.ValidationError("用户已存在")
    
            # 验证手机号码是否合法
            if re.match(REGEX_MOBILE, mobile):
                raise serializers.ValidationError("手机号码非法")
    
            # 验证码发送频率
            one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
            if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count() > 0:
                raise serializers.ValidationError("距离上一次发送未超过60s")
    
            return mobile
    
user.views.py 随机四位数字验证码，验证后保存到model，然后发送 201状态，失败发送400状态

    class SmsCodeGViewSet(CreateModelMixin, viewsets.GenericViewSet):
        serializer_class = SmsSerializer
        def generate_code(self):  # 生成四位数字的验证码
            seeds = "1234567890"
            random_str = []
            for i in range(4):
                random_str.append(choice(seeds))
            return "".join(random_str)
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            mobile = serializer.validated_data["mobile"]
            yun_pian = YunPian(APIKEY)
            code = self.generate_code()
            sms_status = yun_pian.send_sms(code=code, mobile=mobile)
            if sms_status["code"] != 0:
                return Response({
                    "mobile": sms_status["msg"]
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                code_record = VerifyCode(code=code, mobile=mobile)
                code_record.save()
                return Response({
                    "mobile": sms_status["msg"]
                }, status=status.HTTP_201_CREATED)

添加到路由
    
    router.register(r'codes', SmsCodeGViewSet, base_name='codes')

## 7-10,11 user serializer和validator验证

* 让mobile可以为空，前端传过来时自动添加到mobile里。这里为了演示让它可以为空。
* 比较好的方法是 username, mobile都传过来。

自定义序列化User UserSerializer

    # serializers.py
    class UserSerializer(serializers.ModelSerializer):
        code = serializers.CharField(max_length=4, min_length=4)
    
        def validate_code(self, code):
            # 前端传过来的值放在 initial_data里
            veryfy_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
            if veryfy_records:
                last_record = veryfy_records[0]
                five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
                if five_minutes_ago < last_record.add_time:
                    raise serializers.ValidationError("验证码过期")
                if last_record != code:
                    raise serializers.ValidationError("验证码错误")
            else:
                raise serializers.ValidationError("验证码错误")
        class Meta:
            model = User
            fields = ("username", "code", "mobile")
            # code 在userprofile里是没有的，是我们自己添加的

作用所有的字段上

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

* drf validator
http://www.django-rest-framework.org/api-guide/validators/

post后的返回是json格式， 通过 http_code 来确定请求成功失败。

    { 
        "<your_field1>" : ["<errorMessage1>", "<errorMessage2>" ... ] ,
        "<your_field2>" : ["<errorMessage1>", "<errorMessage2>" ... ] ,
    }

* views.py UserViewSet

        serializer_class = UserRegSerializer
    
* url.py

        router.register(r'users', UserViewSet, base_name='users')

## 7-12 django信号量实现用户密码修改

* 在后台添加验证码, 再添加用户测试

        报错：UserProfile' object has no attribute 'code'.

createMixins 里

http://www.django-rest-framework.org/api-guide/fields/#core-arguments
 
serializers.data 时进行序列化，实际上已经删除了， 

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

code --添加 write_only=True
 
添加 write_only 后，不会再序列化。就不会报错了。

password 给返回了，不合理，将它设置为write_only ， 数据库中密码为明文，再处理下

UserProfile(AbstractUser) , AbstractUser 中有set_password ，对密码进行处理。 重载create

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user 

另一种方式使用 signals -- pre_post, https://docs.djangoproject.com/en/1.11/topics/signals/ .

drf 中也提到在 authentication 中。
http://www.django-rest-framework.org/api-guide/authentication/#generating-tokens

* 在signals.py中添加
    
        User = get_user_model()
        @receiver(post_save, sender=User)
        def create_auth_token(sender, instance=None, created=False, **kwargs):
            if created:
                password = instance.password
                instance.set_password(password)
                instance.save()


最后在apps.py中添加signals ， 注释掉 def create 断点调试。

    def ready(self):
        import users.signals
        
signal分离性比较好， def create 更灵活。
 
 自定义信号量 https://docs.djangoproject.com/en/1.11/topics/signals/#defining-and-sending-signals
 
 
 ## 7-13 vue和注册功能联调
 
两种模式，1. 注册完成后登录 2. 注册完返回首页

UserViewSet 重载 create  和 perform_create (返回instance实例) , 跟踪jwt源码得到生成token的代码

    from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
 
前端退出：将cookie的token和name清空，跳转到登录页面。

# 第8章 商品详情页功能

## 8-1 viewsets实现商品详情页接口

商品详情：左侧轮播图，右侧详情，下面副文本。

* serializers.py

        class GoodsImageSerializer(serializers.ModelSerializer):
            class Meta:
                model = GoodsImage
                fields = ("image",)
        
## 8-2 热卖商品接口实现

后端添加 is_hot 过滤条件

* filters.py

        class GoodsFilter(django_filters.rest_framework.FilterSet):
            class Meta:
                model = Goods
                fields = ['price_min', 'price_max', 'is_hot']
        

前端
    
    <hot-sale>
    传递了一个is_hot过滤条件
    
## 8-3 用户收藏接口实现

* vies.py
        
        class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
            queryset = UserFav.objects.all()
            serializer_class = UserFavSerializer
    

现在问题是不应该可选择用户，来进行收藏的，需要的是当前用户。

http://www.django-rest-framework.org/api-guide/validators/#currentuserdefault

获取当前用户, 用 user 覆盖掉, 如果需要删除则要把 id 返回回来. 将 `id` 添加到`fields`.

    class UserFavSerializer(serializers.ModelSerializer):
        user = serializers.HiddenField(
            default=serializers.CurrentUserDefault()
        )
    
        class Meta:
            model = UserFav
            fields = ("user", "goods", "id")

获取到的 goods 有时候需要名称,以后再说.

* 删除的功能如何来做?

http://127.0.0.1:8000/userfavs/1/ 发送 `delete` 方法,返回 `204 no content`, 表示删除是成功的.

* 不严谨的地方--收藏的地方create上

`serializers` 中有些地方要验证,反复收藏同一个商品时,会生成多条记录---不合理的.

用到 django.model 里的设置 在meta 里设置 unique_together

https://docs.djangoproject.com/en/1.11/ref/models/options/#unique-together

    unique_together = ("user", "goods")

清空表，再进行makemigration, migrate ， 防止出错。

收藏2次时报错为

    { "non_field_errors": [ "字段 user, goods 必须能构成唯一集合。" ] }
    
可以用drf的uniqueTogetherValidator来自定义信息，  validators可以作用于每个字段上的，也可以作用于meta里。

* user_operation.serializsers.UserFavSerializer

        class Meta:
            validators = [UniqueTogetherValidator(queryset=UserFav.objects.all(), fields=('user', 'goods'))]
            
## 8-4 drf的权限验证

没有配置权限产生的问题：可以删除其他用户的收藏记录


http://www.django-rest-framework.org/api-guide/permissions/#examples

user是否是当前用户
    
    class IsOwnerOrReadOnly(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
    
            return obj.user == request.user

只获取当前用户的 userfav  重载 getqueryset
    
    class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
        def get_queryset(self):
            return UserFav.objects.filter(user=self.request.user)
    
    
jwt token 最好是配置到需要的view 里，全局配置时，如果每个都加token，当token过期时，在访问goods 商品的列表这种不需要登录的都看不了。

测试： 通过login获取token ， 再把token设置到header里 JWT <token> ，然后进行delete请求。 

比对 user not owner时， 如果false就会发送一个404的错误。

修改数据库 userfav id值来测试 get_queryset() 是否正常工作。

## 8-5 用户收藏功能和vue联调

lookup_field 搜索哪个字段， 默认是pk。 我们修改为 goods_id (userfav表里看)。提高可用性，

进入商品详情页，用户查询goods有没有被收藏，可以直接填写goods的id进行查询，不需要知道数据库中原来的id是什么。

    class UserFavViewSet
        lookup_field = "goods_id"
        
详情页：如果用户以未登录状态访问页面时，肯定是未收藏的状态。此时无法获取用户的。

前端

    created() {
        this.productId = this.$route.params.productId;
        var productId = this.productId;
        if(cookie.getCookie('token')) {
            getFav(productId).then((response) => {
                this.hasFav = true
            }).catch(function (error) { console.log(error) } );
        }
        this.getDetails();
    }
    
    <a v-if="hasFav" class"graybtn" @click="deleteCollect"><i class="iconfont>&#xe613;</i>已收藏</a>
    <a v-else class="graybtn" @click="addCollect"><i = class"iconifont">&#xe613;</i>收藏</a>
    
    deleteCollect() {
        delFav(this.productId).then((response) => {
            console.log(response.data);
            this.hasFav = false;
        }).catch(function (error) { console.log(error) } );
    
    addCollect() { //加入收藏
        addFav({
            goods: this.productId
        }).then((resopnse) => {
            console.log(response.data);
            this.hasFav = true;
            alert('已成功加入收藏夹');
        }).catch(function (error) { console.log(error) } );
    }
    
    
lookup_field 是否会查询出所有的goods_id相关的用户呢？

lookup_field 是在queryset结果里做的， 不是在all里做的。所以已经是当前用户的内容了。

# 第9章 个人中心功能开发

## 9-1 drf的api文档自动生成和功能详解

http://www.django-rest-framework.org/topics/documenting-your-api/

http://127.0.0.1:8000/docs/

点击下面的 source_code - javascript,  直接就会在右侧显示相关的 js代码，前端可以直接使用。 python , shell 脚本也可以直接使用。

usefavs 的 create  给goods 添加 description 

* 方法1 
    
        # models.py
        goods = models.ForeignKey(Goods, help_text="商品id")

* 方法2 在 serializers 中添加 help_text

        class UserRegSerializer(serializers.ModelSerializer):
            code = serializers.CharField(help_text="验证码")
    
* 方法3 在 filter 中添加 help_text 中添加

对于需要登录和验证的方法怎样调试？

在左下authentication 中，进行登录，可选token。  Scheme：JWT, Token填实际的token。也可以用session登录测试session相关的API。

goods-list 中像排序是没有下拉列表的，所以结合 django-filter使用更方便。

## 9-2 动态设置serializer和permission获取用户信息

用户中心：包含修改姓名、出生日期、性别、电子邮件---包括一个邮件验证，手机默认灰色不可改

使用retrieve时，进入个人中心的时候并不知道用户id的,那么在凑url时凑不出一个id。

解决方法1：创建时返回id

解决方法2：重载get_object方法

    def get_object(self):
        return self.request.user

权限问题：获取当前用户时必须是登录的状态

但用户注册时不可能在登录的状态下，不能用IsAuthenticated来完成。

如果是注册状态是 AllowAny, 或者是一个空数组。

动态设置权限：用户注册时没有权限，get_object时一个Authentic状态。研究源码：根据GenericAPIView。

找到 `rest_framework.views.APIView#get_permissions` ，我们可以重载这个函数, `self.action` 只有使用 `ViewSet` 才有 `action` 这个好处。

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

添加了 `JSONWebTokenAuthentication` 就不会再弹登录框了。

使用 `http://127.0.0.1:8000/docs/` 的 `Authentication#token, Scheme`填JWT，对user/1进行测试，返回了user mobile,

我们在返回用户的时候希望用另一个serializer进行序列化，

    class UserDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("name", "birthday", "gender", "mobile", "mail")

如果使用这个接口进行用户注册的话，会对上面的字段逐一验证，这个连用户名和密码都没有，所以不能用这个序列化。


动态获取serializer：重载 get_serializer_class(跟进源码查到)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

## 9-3 vue和用户接口信息联调

`vue: views/member/userinfo.vue`

`/user/1`

## 9-4 用户个人信息修改

给 `UserViewSet` 添加 `mixins.UpdateModelMixin` 。支持 `put,patch` 操作。

    vue: return axios.patch(`$(local_host}/users/1/`, params)

## 9-5 用户收藏功能

	#useroperation/views.py
	class UserFavDetailSerializer(serializers.ModelSerializer):
	    goods = GoodsSerializer()

	    class Meta:
		model = UserFav
		fields = ("goods", "id")

`lookup_field` --- 前端要删除时也要传递 `goods_id`

    class UserFavViewSet
        lookup_field = "goods_id"
        def get_serializer_class(self):
            if self.action == "list":
                return UserFavDetailSerializer
            elif self.action == "create":
                return UserFavSerializer
            return UserFavSerializer

##　9-6 用户留言功能

需要注意添加id，删除的时候需要使用。

再添加个 "add_time"，但我们不想写这个时间，并格式化它

    	add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

		class LeavingMessageSerializer(serializers.ModelSerializer):
		    user = serializers.HiddenField(
			default=serializers.CurrentUserDefault()
		    )

		    class Meta:
			model = UserLeavingMessage
			fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


		#views.py
		class LeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
					    viewsets.GenericViewSet):
		    """
		    list:
			获取用户留言
		    create:
			添加留言
		    delete:
			删除留言
		    """
		    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
		    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
		    serializer_class = LeavingMessageSerializer

		    def get_queryset(self):
			return UserLeavingMessage.objects.filter(user=self.request.user)


* 前端代码

	delMessage = messageId => {return axios.delete(`${local_host}/messages`)
		deleteMessage(id) {
			alert("删除成功")
		}).catch(function (error) {console.log(error); });
	}
	export const addMessage = params  => {return asxios.post(`$(local_host}/messages/`, params, {headers: {'Content-Type': 'multipart/form-data' }})}
	submitMessage() {
		const formData = new FormData();
		formData.append('file', this.file);
		formData.append('subject', this.subject);
		formData.append('message', this.message);
		formData.append('message_type', this.message_type);
		addMessage(formData).then((response) => {
			this.getMessage();
		}).catch(function (error) {console.log(error); });
	}

* drf 是怎样解析的呢？

http://www.django-rest-framework.org/api-guide/parsers/#multipartparser

.media_type: multipart/form-data

* user_operation.models.UserLeavingMessage

      file = models.FileField(upload_to="message/images/", verbose_name="上传的文件", help_text="上传的文件")


## 9-7 用户收货地址列表页接口开发

*  修改model(这时是为了简单)， makemigration, migrate

        # UserAddress
        province = models.CharField(max_length=100, default="", verbose_name="省")
        city = models.CharField(max_length=100, default="", verbose_name="市")
        district = models.CharField(max_length=100, default="", verbose_name="区域")
    
    
        # user_operation.serializsers.AddressSerializer
        class AddressViewSet(viewsets.ModelViewSet):
            permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
            authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
            serializer_class = AddressSerializer
            def get_queryset(self):
                return UserAddress.objects.filter(user=self.request.user)
    
* serializers 这里可以添加一些验证的

        # user_operation.serializsers.AddressSerializer
        class AddressSerializer(serializers.ModelSerializer):
            user = serializers.HiddenField(
                default=serializers.CurrentUserDefault()
            )
            add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
            class Meta:
                model = UserAddress
                fields = ("id", "user", "province", "city", "district", "address", "signer_name", "signer_mobile", "add_time")
    
* 在router中注册

        # urls.py
        router.register(r'address', AddressViewSet, base_name='address')

## 9-8 vue和收货地址接口联调

members/receive.vue

	export const delAddress = addressId => {return axios.delete(`{host}/address/`)}
	export const updateAddress = {addressId, params} => {return axios.patch(`{host}/address/`)}
	export const getAddress = () => {return axios.get(`{host}/address/`)}


	created() {
		this.getReceiveInfo();
	}

	getReceiveInfo() {
		getAddress().then((response) => {
			console.log(response.data);
			this.receiveInfoArr = response.data;
		}).catch(function (error) {console.log(error)})
	}

	updateProvince(data) {
		this.receiveInfoArr[this.currentIndex].province = data.value;
	}
	updateCity(data) {
		this.receiveInfoArr[this.currentIndex].city = data.value;
	}
	updateDistrict(data) {
		this.receiveInfoArr[this.currentIndex].district = data.value;
	}

# 第10章 购物车、订单管理和支付功能

## 10-1 购物车功能需求分析和加入到购物车实现


页面结构

	购物车商品列表
		购物车已存在的商品，再次添加时增加数量。后台直接更新数量。
		删除=>直接删除商品
	金额
	配送地址

	购物车已存在的商品，再次添加时增加数量。后台直接更新数量。

* 更新 model 的 meta创建联合主键

	class ShoppingCart(models.Model):
	    class Meta:
	        unique_together = ("user", "goods")


* 不用 ModelSerializers原因： 我们需要的是数量加一，下面在 is_valid 时unique_together 就报错了，即使重写serializer的create方法也无效，所以用底层的seriailizer。

		class CreateModelMixin(object):
		    def create(self, request, *args, **kwargs):
		        serializer = self.get_serializer(data=request.data)
		        serializer.is_valid(raise_exception=True)
		        self.perform_create(serializer)
		        headers = self.get_success_headers(serializer.data)
		        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


不在view层做：无文档，代码分离效果差。最好是在serializers来做，会有文档。代码分离性也好。

* validated_data 是验证过的，它之前的叫initial_data 是未验证过的

* 重载 Serializer 的 create 方法,使购物车已存在的商品，再次添加时增加数量。后台直接更新数量。

        class ShopCartSerializer(serializers.Serializer):
            def create(self, validated_data):
                user = self.context["request"].user
                nums = validated_data["nums"]
                goods = validated_data["goods"]
                existed = ShoppingCart.objects.filter(user=user, goods=goods)

	        if existed:
	            existed = existed[0]
	            existed.nums += nums
	            existed.save()
	        else:
	            existed = ShoppingCart.objects.create(**validated_data)

* urls.py

        router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')

* trade/views.py

        class ShoppingCartViewSet(viewsets.ModelViewSet):
            permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
            authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
            serializer_class = ShopCartSerializer
           
            def get_queryset(self):
                return ShoppingCart.objects.filter(user=self.request.user)
        

## 10-2 修改购物车数量


我们希望传递goods_id 来处理事务， 而不是本身的id。

	trade.views.ShoppingCartViewSet
	lookup_field = "goods_id"

* rest_framework.serializers.Serializer 继承 BaseSerializer , update方法会 raise not implements。所以需要我手动重载这些方法。

* rest_framework.serializers.ModelSerializer 会重载这些方法。

        class ShopCartSerializer(serializers.Serializer):
            def update(self, instance, validated_data):
                # 修改商品数量
                instance.nums = validated_data["nums"]
                instance.save()
                return instance

## 10-3 vue和购物车接口联调

购物车页面需要获取商品的详情。

前端相关代码

	export const getShopCarts = params => {return axios.get(`${host}/shopcarts/`)}
	export const addShopCart = params => {return axios.get(`${host}/shopcarts/`), params}
	export const updateShopCart = {goodsId, params} => {return axios.patch(`${host}/shopcarts/`)}
	export const deleteShopCart = goodsId => {return axios.delete(`${host}/shopcarts/`)}

	addShoppingCart() { //加入购物车
		goods: this.productId, //商品id
		nums: this.buyNum, //购买数量
	}).then((response) => {
		this.$refs.model.setShow();
		// 更新 store 数据
		this.$store.dispatch('setShopList');
	}).catch(function (error)) {console.log(error)}

	deleteGoods(index, id) { //移除购物车
		deleteShopCart(id).then((response) => {
			console.log(response.data);
			this.goods_list.splice(index, 1);

			//更新store数据
			this.$store.dispatch('setShopList');
		}).catch(function (error)) {console.log(error)}
	}

	computed: {
		...mapGetters({
			goods_list: 'goods_list',
			userInfo: 'userInfo'
		})
	}

	created() {
		//请求购物车商品
		getShopCarts().then((response) => {
			//更新store数据
			state.goods_list.goods_list = response.data;
			console.log(response.data)
			var totalPrice = 0
			response.data.forEach(function(entry) {
				totalPrice += entry.goods.shop_price*entry.nums
			});
			state.goods_list.totalPrice = totalPrice;
		}).catch(function (error)) {console.log(error)}
		this.getAllAddr()
	}

	reduceCartNum(index, id) { //删除数量
		if(this.goods_list.goods_list[index].nums<=1) {
			this.deleteGoods(index, id)
		}else{
			updateShopCart(id, {
				nums: this.goods.goods_list[index].nums-1
			}).then((response) => {
				this.goods.goods_list[index].nums = this.goods.goods_list[index].nums-1
				// 更新store数据
				this.$store.dispatch('setShopList');
				// 更新总价
				this.setTotalPrice();
			}).catch(function (error)) {console.log(error)}
		}
	}

	getAllAddr() { //获得所有配送地址
		getAddress().then((response) => {
			this.addrInfo = response.data;
		}).catch(function (error)) {console.log(error)}
	}

## 10-4,5 订单管理接口

`order_sn` 订单号是由后台生成的， `model` 如果不设置会验证，先设置为空。

* trade.models.OrderInfo

    	order_sn = models.CharField(null=True, blank=True)
	

`makemigrations, migrate`

`address` 不要用外键，我们要保存订单当时填写的地址。

* serializers.py

不允许提交用户，订单状态，订单号，交易号。支付时间。

		
		class OrderSerializer(serializers.ModelSerializer):
		    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
		    pay_status = serializers.CharField(read_only=True)
		    trade_no = serializers.CharField(read_only=True)
		    order_sn = serializers.CharField(read_only=True)
		    pay_time = serializers.DateTimeField(read_only=True)
		    add_time = serializers.DateTimeField(read_only=True)

		    def generate_order_sn(self):
		        # 当前时间+userif+随机数
		        from random import Random
		        random_ins = Random()
		        order_sn = "{time_str}{user_id}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
		                                                        user_id=self.context["request"].user.id,
		                                                        ranstr=random_ins.randint(10, 99))
		        return order_sn

		    def validate(self, attrs):
		        attrs["order_sn"] = self.generate_order_sn()
		        return attrs

		    class Meta:
		        model = OrderInfo
		        fields = "__all__"


* urls.py

		# 订单相关
		router.register(r'orders', OrderViewSet, base_name='orders')


* views.py

不允许修改订单，所以这里不用 `ModelViewSet`

删除时希望把相关的 `goods` 信息也删除，测试了一下，是自动删除的。满足了要求。

		class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

		    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
		    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
		    serializer_class = OrderSerializer

		    def get_queryset(self):
		        return OrderInfo.objects.filter(user=self.request.user)

		    def perform_create(self, serializer):  # 这里是调用 serializer 的 save
		        order = serializer.save()
		        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
		        for shop_cart in shop_carts:
		            order_goods = OrderGoods()
		            order_goods.goods = shop_cart.goods
		            order_goods.nums = shop_cart.nums
		            order_goods.order = order
		            order_goods.save()

		            shop_cart.delete()
		        return order


## 10-6 vue个人中心订单接口调试

订单详情-序列化时应该显示出商品列表

`OrderGoods` 和 `OrderInfo` 通过 `order` 来连接，添加 `related_name` .

    class OrderGoods(models.Model):
        order = models.ForeignKey(OrderInfo, verbose_name="订单信息", on_delete=models.CASCADE, related_name="goods")


    class OrderGoodsSerializer(serializers.ModelSerializer):
        goods = GoodsSerializer(many=False)

    class OrderDetailSerializer(serializers.ModelSerializer):
        goods = OrderGoodsSerializer(many=True)

    class OrderViewSet
        def get_serializer_class(self):
            if self.action == "retrieve":
                return OrderDetailSerializer
            return OrderSerializer

前端

    export const gerOrders = () => {return axios.get(`${host}/orders`)}
    export const delOrder = orderId => {return axios.delete(`${host}/orders` + orderId)}
    export const createOrder = params => {return axios.post(`${host}/orders`, params)}
    export const getOrderDetail = orderId => {return axios.get(`${host}/orders` + orderId)}

    selectAddr(id) { //选择配送地址
        this.addressActive = id;;
        var cur_address = '';
        var cur_name = '';
        var cur_mobile = '';
        this.addrInfo.forEach(function(addrItem) {
            if(addrItem.id == id){
                cur_address = addrItem.province + addrItem.city + addrItem.district + addrItem.detail;
                cur_name = addrItem.signer_name;
                cur_mobile = addrItem.signer_mobile;
            }
        })
        this.address = cur_address;
        this.signer_mobile = cur_mobile;
    }

    checkout() {
        if(this.addrInfo.length == 0) {
            alert("请选择收货地址")
        } else {
            createOrder({
                post_script: htis.post_script,
                address: this.address,
                signer_name: this.signer_name,
                signer_mobile: this.signer_mobile,
                order_mount: this.totalPrice
            }).then((response) => {
                alert("订单创建成功")
            }).catch(function(error) {console.log(error); })
        }
    }

    getOrder() {
        getOrders().then((response) => {
            this.orders = response.data;
        }).catch(function(error) {console.log(error); })
    },
    cancelOrder(id) {
        alert('您确认要取消该订单么？取消后此订单将视为无效订单');
        delOrder(id).then((response) => {
            alert('订单删除成功')
        }).catch(function(error) {console.log(error); })
    }
    getOrderInfo() {
        getOrderDetail(this.orderId).then((response) => {
            this.orderInfo = response.data;
            var totalPrice = 0;
            response.data.goods.forEach(function (entry) {
                totalPrice += entry.goods_num*entry.goods.shop_price
            });
            this.totalPrice = totalPrice;
            alert(this.totalPrice)
        }).catch(function(error) {console.log(error); })
    }

## 10-7 pycharm远程代码调试

第三方服务API的回调函数，都是远程的，需要远程调试远程服务器。

将代码上传到服务器中。

Tools - Deployment - 添加一个sftp服务器 name:mxshop

ssh

	mkdir projects
	cd projects

pycharm sftp:

* Connection

		host: 47.92.87.172
		user name:
		password:

* Mapping

		/root/project/mxshop

点击 Tools - Deployment - Upload 进行上传

* 工具： winSCP(flashfxp一样), 使用sftp连接。

* 建立虚拟环境

http://projectsedu.com/2017/08/15/centos7-下通过nginx-uwsgi部署django应用/

maridb 和 mysql 是一致的。配置好权限及阿里云安全组规则。

使用navicat连接到服务器，新建数据库，然后将本地数据库传输上去.

navicat 如果上传失败：

    navicat菜单： 工具-监控-服务器变量 搜索 package, max_allow_packet 改大一些。

本地 settings.py 设置,  

	DATABASES = {
	    'default': {
	        'HOST': '47.x.x.x',
	    }
	}


这条语句有'%' ,不会添加localhost的权限,需要另添加一条语句到 localhost.

    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '123456' WITH GRANT OPTION;
    本机可用localhost，%通配所有远程主机；

* PyCharm 上传某个文件

左侧先点击settings.py,再点击 Deployment-upload 上传.

* 远程服务器端 python manage.py runserver

PyCharm 配置服务器的解释器，Settings - Project Interpreter, Add remote - SSH Credentials, 填写好服务器相关信息。

Run - Debug, 会启动服务器端的调试。

## 10-9 支付宝公钥、私钥和沙箱环境的配置

[蚂蚁金服开放平台](https://docs.open.alipay.com/)

1. 开发者中心-开发服务-沙箱应用-设置公钥
2. 开发者中心-文档中心-电脑网站支付
3. API列表-统一收单下单并支付页面接口
4. 生成RSA密钥-非JAVA适用版本，2048。生成。
5. 填写好公钥。（保存好公钥私钥）

        前后加上 begin privite key ,end privite key .保存到项目中，
        private_2048.txt
        pub_2048.txt

6. 把支付宝的公钥复制出来。保存到项目中 alipay_key_2048.txt.

## 10-10 支付宝开发文档解读

把项目 Interpreter 改为本地。

biz_content, sign, sign_type 比较重要

在virtualenv中安装 `pip install pycryptodome`

将写好的 alipay.py 放到 utils中。

    https://github.com/liyaopinner/mxshop_sources/blob/master/alipay.py

自实现签名 https://docs.open.alipay.com/291/106118

## 10-11 支付宝支付源码解读

pip install pycryptodome

## 10-13 django集成支付宝notify_url和return_url接口

修改后将代码上传到服务器，再进行调试。


* 交易状态

|枚举名称|枚举说明|
|---|---|
WAIT_BUYER_PAY | 交易创建，等待买家付款
TRADE_CLOSED   | 未付款交易超时关闭，或支付完成后全额退款
TRADE_SUCCESS  | 交易支付成功
TRADE_FINISHED | 交易结束，不可退款


```python
# trade.views.AliPayView
class AliPayView(APIView):

    def post(self, request):
        # 处理支付宝的notify_url
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016091200495873",
            app_notify_url="http://47.92.87.172:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=alipay_pub_key_path,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")

# urls.py
url(r'^alipay/return/', AliPayView.as_view(), name="alipay"),

# settings.py
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
alipay_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/ali_pub.txt')



```

## 10-15 支付宝接口和vue联调

支付宝支付的url放到serializer中，可以重构create方法或将字段设到serializer中--SerializerMethodField，
http://www.django-rest-framework.org/api-guide/fields/#serializermethodfield

复制到order detail中，立即支付需要使用。

创建订单成功后，跳转到alipay支付，希望支付后跳转回自己的页面。但是现在是已经不在我们的页面了。

解决方法1：前端思路：请求支付宝时直接返回一张图片。直接返回给vue进行显示。自己再写个url不断后台查询是否完成支付。

解决方法2：后端思路：用django代理页面请求，新建static目录，请build出来的文件放在static目录下。设置settings.py。设置staticfiles_dir

```python

class trade.views.AliPayView(APIView):
    def get(self, request):
        ...
        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016091200495873",
            app_notify_url="http://47.92.87.172:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=alipay_pub_key_path,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/alipay/return/"
        )

        verify_re = ...
        for ...

            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=2)
            return response
        else:
            response = redirect("index")
            return response

class trade.serializers.OrderSerializer(serializers.ModelSerializer):
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(...)
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

#settings.py
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

#urls.py
url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
```

https://docs.open.alipay.com/270/alipay.trade.page.pay

qr_pay_mode=4：订单码 ，全部在前端完成体验比较好。

# 第11章 首页、商品数量、缓存、限速功能开发

## 11-1  轮播图接口实现和vue调试

本地调试，PyCharm 中 Interpreter 改成本地的虚拟环境。settings.py 改成本地的数据库

## 11-2  新品功能接口开发

front_end:

```ts
getOpro(){
    getGoods({
        "is_new":true
        })
        .then((response) => {
            //跳转到首页 response.body 页面
            this.newopro = response.data.results
        })
        .catch(function (error) {
            console.log(error)
        })
}
```

## 11-3  首页商品分类显示功能


Goods - category 指向的是第三级，我们在 indexgoods 中取到的第一级，需要手动处理添加代码后 `makemigrations` , `migrate`.

```python

# views.py
class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerSerializer
    class Meta:
        model = Banner
        fields = "__all__"
class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer

# serializers.py
class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(goods_ins, many=False, context={'request': self.context['request']}).data
            return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True)
        # rest_framework.mixins.ListModelMixin 用法相似
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"

# models.py
class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, related_name='category', verbose_name="商品类目", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, related_name='goods')

```

`xadmin` 中品牌只能选一级，怎样选2级呢？

```python
class GoodsBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]
    def get_context(self):
        context = super(GoodsBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context
```


__在 Serializer 嵌套 Serializer 产生的问题：__

这时 json 对象的 image 字段没有域名显示为 `"/media/goods/images/xxxxx.jpg"`

    goods_json = GoodsSerializer(goods_ins, many=False).data

需要添加一个参数 `context={'request': self.context['request']}`
    
    goods_json = GoodsSerializer(goods_ins, many=False, context={'request': self.context['request']}).data

源码中 image 字段序列化时 会判断 request ，如果有会添加域名, 在上下文中使用，view中会自动添加request，仅在 Serializer 中嵌套使用时会有这个问题。

## 11-5 商品点击数、收藏数修改

方法1 user_operation.views.UserFavViewSet perform_create
方法2 信号量来解决

```python

# 商品点击数 +1
class GoodsListViewSet(...):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
# user_operation/signals.py 商品收藏数加1
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()

# user_operation.apps.UserOperationConfig
class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = '用户操作管理'

    def ready(self):
        import user_operation.signals
```

## 11-6  商品库存和销量修改

新增商品到购物车
修改购物车数量
删除购物车记录

```python

# trade/views.py
class ShoppingCartViewSet(viewsets.ModelViewSet):
    ...
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

# 支付成功后修改售出记录
class AliPayView(APIView):
    def get(self, request):
        ...
        for existed_order in existed_orders:
                order_goods = existed_orders.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()
                    ...

```

## 11-7 drf的缓存设置

[django 缓存](https://docs.djangoproject.com/en/1.11/topics/cache/)

drf 缓存 -- drf-extensions

https://github.com/chibisov/drf-extensions

[docs](http://chibisov.github.io/drf-extensions/docs/)

[CacheResponseMixin](http://chibisov.github.io/drf-extensions/docs/#cacheresponsemixin)

尽量个人数据不缓存，公共数据缓存

It is common to cache standard viewset `retrieve` and `list` methods.

CacheResponseMixin 添加到继承列表最前面

    from rest_framework_extensions.cache.mixins import CacheResponseMixin
    class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

设置缓存时间

    REST_FRAMEWORK_EXTENSIONS = {
        'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
    }

## 11-8  drf配置redis缓存

[django-redis](https://github.com/niwinz/django-redis), [Docs](http://django-redis-chs.readthedocs.io/zh_CN/latest/)

`pip install django-redis`

配置redis缓存 要把redis启动

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

使用 redis client, `keys *`

不同参数传递时，都会生成不一样的key，保证不同过滤规则产生不同的key，不让数据取错。

## 11-9  drf的throttle设置api的访问速率

ip 限速问题： 防止爬虫无节制的访问。

[Throttling](http://www.django-rest-framework.org/api-guide/throttling/)

    # settings
    REST_FRAMEWORK = {
        'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle'
        ),
        'DEFAULT_THROTTLE_RATES': {
            'anon': '100/day',
            'user': '1000/day'
        }
    }

GoodsListViewSet

    from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
    class GoodsListViewSet():
        throttle_classes = (UserRateThrottle, AnonRateThrottle,)

## 12-1 第三登录开发模式以及oauth2.0简介

[微博登录](http://open.weibo.com/),[微信登录](https://open.weixin.qq.com/),[QQ登录](http://open.qq.com/) -- 跳转到第三方应用进行登录，再进行回调。 

进入上面的微博开放平台， 应用信息-高级信息-设置回调地址。 保存AppKey, 

[OAuth2.0授权认证](http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E)

## 12-2 oauth2.0获取微博的access_token

```python
def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = ""
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=123,
                                                                                            redirect_uri=redirect_uri)
    print(auth_url)


# http://open.weibo.com/wiki/Oauth2/access_token
def get_access_token(code="11111"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": 2222333,
        "client_secret": "2c60bxxxxx",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://47.x.x.x/complete/weibo"
    })

    # '{access_token="xxx", uid="yyy"}


def get_user_info(token, uid):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(token=token, uid=uid)
    print(user_url)


if __name__ == "__main__":
    get_auth_url()
    get_access_token(code="11111")
    get_user_info(access_token="xxxxx", uid="yyyyy")
```


## 12-3 social_django集成第三方登录

https://github.com/python-social-auth/social-app-django

http://python-social-auth.readthedocs.io/en/latest/configuration/django.html

    #settings.py
    INSTALLED_APPS = [
        ...
        'social_django',
    ]

./manage.py migrate

以前做过的部分： 提醒 mysql 默认用是的 MyISAM , database 记得加 innodb

/site-packages/social_core/backends/weibo.py

    AUTHENTICATION_BACKENDS = [
        ...
        'social_core.backends.weibo.WeiboOAuth2',
        'social_core.backends.qq.QQOAuth2',
        'social_core.backends.weixin.WeixinOAuth2',
        'django.contrib.auth.backends.ModelBackend',
                               ]

Add URLs entries:

    urlpatterns = patterns('',
        ...
        url('', include('social_django.urls', namespace='social'))
        ...
    )

Template Context Processors

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                ...
                'context_processors': [
                    ...
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect',
                    ...
                ]
            }
        }
    ]


__本地调试__

urls.py
    
    url(r'^login/$', obtain_jwt_token), #添加一个$符号，不然和下面的login冲突
    url('', include('social_django.urls', namespace='social'))

授权回调页设置为本机 `127.0.0.1/complete/weibo`

为什么支付宝不能本机调试， weibo可以呢？ 微博这个是浏览器请求redirct 完成的，支付宝 notify_url 到达率很高, return_url(关闭页面后的异步回调)不高。

trade/view.py notify_url 是支付宝向我们发起的一个post请求，不是给浏览器发送的redirect，隔一段时间发送一个post请求。所以必须是一个外部的地址。

__配置key和secret__

    SOCIAL_AUTH_WEIBO_KEY = 'foobar'
    SOCIAL_AUTH_WEIBO_SECRET = 'bazqux'

    SOCIAL_AUTH_QQ_KEY = 'foobar'
    SOCIAL_AUTH_QQ_SECRET = 'bazqux'

    SOCIAL_AUTH_WEIXIN_KEY = 'foobar'
    SOCIAL_AUTH_WEIXIN_SECRET = 'bazqux'

http://127.0.0.1/login/weibo/

提示用户登录，成功后怎样跳转？

    SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'

跳转后我们的网站并没有登录---它是为django做的不是为drf做的。需要手动修改源码实现。

把social-core复制出来。 `extra_apps.social_core.actions.do_complete` 最后面

    ...
    response = backend.strategy.redirect(url)
    payload = jwt_payload_handler(user)
    response.set_cookie("name", user.name if user.name else user.username, max_age=24 * 3600)
    response.set_cookie("token", jwt_encode_handler(payload), max_age=24 * 3600)
    return response

## 13-1 sentry的介绍和通过docker搭建sentry

https://www.cnblogs.com/yu-hailong/p/7629120.html

https://github.com/getsentry/sentry

https://sentry.io 小项目可以使用在线的服务。大项目/敏感信息 自己搭建。

错误日志 import!

    logging 
    登录到服务器查看文件
    我们主动去查询， web 系统，
    立即知道错误--邮件 -- 邮件特别多 bug>100
    无法集中管理bug 有些公司在用jira 通过测试来提bug

    sentry
    分配bug > bobby
    项目管理， 多个项目


### CentOS 7 安装 sentry

sudo yum remove docker docker-common docker-selinux docker-engine
安装依赖包
    
    $ sudo yum install -y yum-utils device-mapper-persistent-data lvm2
    
添加稳定的源

    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

__安装 docker ce__

更新yum包

    sudo yum makecache fast

安装 docker ce

    sudo yum install docker-ce

启动docker

    sudo yum start docker

测试docker
    
    sudo docker run hello-world

__安装方法二__

下载安装包 https://download.docker.com/linux/centos/7/x86_64/stable/Packages/ 下载对应的安装包后

    sudo yum install docker-ce-17.03.0.ce-1.el7.centos.x86_64.rpm

安装 docker-compose

    sudo yum install epel-release
    sudo yum install -y python-pip
    sudo pip install -y docker-compose

安装 docker ce 
    
    sudo yum install docker-ce

__2. sentry__

安装 git

    sudo yum install git
    mkdir -p data/{sentry,postgres}

下载 docker 镜像并构建容器

https://github.com/getsentry/onpremise

    git clone https://github.com/getsentry/onpremise.git
    cd onepremise
    docker-compose run --rm web config generate-secret-key
    # 这时显示了 key xxxxxxxx
    vim docker-compose.yml
    # 修改 SENTRY_SECRET_KEY = xxxxxx
    docker-compose run --rm web upgrade
    docker-compose up -d
    docker ps

Access your instance at `localhost:9000!` 阿里云需要修改安全组

或

    git clone https://github.com/getsentry/onpremise.git
    cd onepremise
    sudo make build

在xshell中无法回退时，按住Ctrl键再按退格就可以删除了。

## 13-2 sentry的功能

Project, Team, Members.

新建一个project， name:mxshop. 创建项目。

Get your DSN. 复制出来。在mxshop 中新建 test目录。新建 sentry_test.py , dsn = xxxxxxxx

在 浏览器中点击 Python ，

    pip install raven --upgrade

示例 `sentry_test.py`

```python
from raven import Client

dsn = "xxx"

client = Client(dsn)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
```

Project settings 里设置 用户可见性，及邮件的 Subject Prefix 便于筛选。

Alert - Rules, 设置邮件发送频率。

Sentry 功能强大，最常用的错误栈及发送邮件。

支持同步到 github，jira 等等等。

自己部署的支持 Web API ，支持 代码方式进行各种操作。

## 13-3,4 sentry 集成到django rest framework中

登录后 左下角 账户，设置好时区 Asia/Shanghai 24小时制

大坑:

左下角-管理。设置 sentry 邮件 ，发送设置。 host地址，用户名密码。发送一封测试邮件。测试之后还会出现一个timeout，

    vim sentry.conf.py
    复制出来
    vim docker-compose.yml

    SENTRY_POSTGRES_HOST: postgres #写在这行下面
    SENTRY_EMAIL_HOST: 'smtp.sina.com'
    SENTRY_EMAIL_USER: 'mymail32@sina.com'
    SENTRY_SERVER_EMAIL: 'mymail32@sina.com'  #和user 保持一致
    SENTRY_EMAIL_PASSWORD': 'mypwd'

重启应用
    
    $ docker-compose up -d

发送测试邮件时 在阿里云服务器出现timeout。

阿里云 禁用了 25 端口仅支持465端口(ssl协议的更安全)， sina没有提供 25端口。

sentry不支持 ssl 支持 tls。先用本地虚拟机测试发送邮件。

docker ps , 找出他们的id

    id1 onpremise_worker
    id2 onpremise_web
    id3 onpremise_cron

    $docker stop id1,id2,id3

    $docker start worker,cron,web
    按这个顺序启动

项目-项目设置 警报-规则，当事件第一次出现时发送邮件-编辑规则

把虚拟机中的dsn配置到 tests/sentry_test.py。在邮箱里看一下-点击view on sentry.

配置到 Django RestFramework中

右下角-文档-django

### Setup

Using the Django integration is as simple as adding raven.contrib.django.raven_compat to your installed apps:

```python
INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
)
```

Additional settings for the client are configured using the RAVEN_CONFIG dictionary:

```python
import os
import raven

RAVEN_CONFIG = {
    'dsn': 'https://<key>:<secret>@sentry.io/<project>',
    # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)), #这行git相关不用了
}
```

Once you’ve configured the client, you can test it using the standard Django management interface:

    python manage.py raven test

setry 支持集成各种语言，是一个前后端分离的技术，便于集成。