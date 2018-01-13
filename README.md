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
                
