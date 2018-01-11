pillow 处理图片的包。

# 第3章 model设计和资源导入
## 3-2 user models设计.mp4 

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

## 3-3 goods的model设计.mp4
通过一个model完成所有级别的类。定义从属关系，不定死关系。 指向自己这张表---`"self"`
    
    prarent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                         related_name="sub_cat") #related_name作用后边查询用


* 将 app 添加到 INSTALLED_APPS

    'DjangoUeditoro', 'users', 'goods', 'trace', 'user_operation'添加到 settings