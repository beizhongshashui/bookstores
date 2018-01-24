# 目录
- [1，新建项目](#1)
- [2，用户系统开发](#2)
- [3，书籍商品模块](#3)
- [4，用户中心实现](#4)
- [5，购物车功能](#5)
- [6，订单页面的开发](#6)
- [7，使用缓存](#7)
- [8，评论功能](#8)
- [9，发送邮件功能实现](#9)
- [10，登陆验证码功能实现](#10)
- [11，全文检索的实现](#11)
- [12，用户激活功能实现](#12)
- [13，用户中心最近浏览功能](#13)
- [14，过滤器功能实现](#14)
- [15，部署](#15)


# <a id="1">1，新建项目</a>

## 1，新建项目
```
$ django-admin startproject bookstore
```

## 2，将需要用的包添加进来
```
# wq保存
$ vim requirements.txt
```
安装包文件如下:
```
# requirements.txt
amqp==2.2.2
billiard==3.5.0.3
celery==4.1.0
Django==1.8.2
django-haystack==2.6.1
django-redis==4.8.0
django-tinymce==2.6.0
itsdangerous==0.24
jieba==0.39
kombu==4.1.0
olefile==0.44
Pillow==4.3.0
pycryptodome==3.4.7
PyMySQL==0.7.11
python-alipay-sdk==1.4.0
pytz==2017.2
redis==2.10.6
uWSGI==2.0.15
vine==1.1.4
Whoosh==2.7.4
```
安装环境（在虚拟环境中）
```
$ pip install -r requirements.txt
```
## 3，修改项目配置文件，将默认sqlite改为mysql
```
# bookstore/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookstore',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
```
# <a id="2">2，用户系统开发</a>
## 1，用户系统的开发
新建users这个app，也就是用户app，先从注册页做起。
```
$ python manage.py startapp users
```
我们建好users app后，需要将它添加到配置文件中去。
```
bookstore/settings.py
INSTALLED_APPS = (
    ...
    'users', # 用户模块
)
```
然后我们需要设计表结构，我们要思考一下，这个users数据表结构应该包含哪些字段？
我们需要先抽象出一个BaseModel，一个基本模型，什么意思呢？因为数据表有共同的字段，我们可以把它抽象出来，比如create_at（创建时间），update_at（更新时间），is_delete（软删除）。
```
# bookstore/base_model.py
from django.db import models

class BaseModel(models.Model):
    '''模型抽象基类'''
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=TabError, verbose_name='更新时间')

    class Meta:
        abstract = True
```
然后我们针对Users设计一张表出来。
```
class Passport(BaseModel):
    '''用户模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名称')
    password = models.CharField(max_length=40, verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False, verbose_name='激活状态')

    # 用户表的管理器
    objects = PassportManger()

    class Meta:
        db_table = 's_user_account'
```
接下来我们在PassportManager()中实现添加和查找账户信息的功能，这样抽象性更好。
```
# Create your models here.
class PassportManger(models.Manager):
    def add_one_passport(self, username, password, email):
        '''添加一个账户信息'''
        passport = self.create(username=username, password=get_hash(password), email=email)
        # 3.返回passport
        return passport

    def get_one_passport(self, username, password):
        '''根据用户名密码查找账户的信息'''
        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            # 账户不存在
            passport = None
        return passport
```
我们这里有一个get_hash函数，这个函数用来避免存储明文密码。所以我们来编写这个函数。
```
# bookstore/users/models.py
from hashlib import sha1

def get_hash(str):
    '''取一个字符串的hash值'''
    sh = sha1()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()
```
接下来我们将Users的表映射到数据库中去。
```
mysql> create database bookstore;
$ python manage.py makemigrations users
$ python manage.py migrate
```
