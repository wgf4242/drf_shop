pillow 处理图片的包。

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

5. create superuser admin/admin123
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
2. 而且 add_time 不能进行系列化
