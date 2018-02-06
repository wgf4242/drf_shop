[TOC]

pillow 处理图片的包。

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
