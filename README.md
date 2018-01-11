pillow 处理图片的包。

# 第3章 model设计和资源导入

1. 新建数据库 mxshop

        新建 apps, db_tools, extra_apps, media 
        右击 apps - mark as source root
        右击 extra_apps  - mark as resource root

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

    
    # settings.py
    AUTH_USER_MODEL = 'users.UserProfile'

