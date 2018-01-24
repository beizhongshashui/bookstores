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

## 2，用户系统前端模板编写
接下来我们要将前端模板写一下，先建一个模板文件夹。
```
$ mkdir templates
```
我们第一个实现的功能是渲染注册页。将register.html拷贝到templates/users。
将js，css，images文件夹拷贝到static文件夹下。作为静态文件。
接下来我们将程序跑起来。看到了Django的欢迎页面。
```
$ python manage.py runserver 9000
```
然后呢？我们想把register.html渲染出来。我们先来看views.py这个视图文件。
```
# users/views.py
def register(request):
    '''显示用户注册页面'''
    return render(request, 'users/register.html')
```
然后我们将url映射做好。主应用的urls.py为
```
# bookstore/urls.py
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('users.urls', namespace='user')), # 用户模块
]
```
'^'表示只匹配user为开头的url。
然后在users app里面的urls配置url映射。
```
# users/urls.py
from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'), # 用户注册
]
```
将templates的路径写入配置文件中。
```
# settings.py
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # 这里别忘记配置！
        ...
    },
]
```
我们可以看到静态文件没有加载出来，所以我们要改一下html文件中的路径。将静态文件的路径前面加上'/static/'
然后在配置文件中加入调试时使用的静态文件目录。
```
# settings.py
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
] # 调试时使用的静态文件目录
```
好。我们渲染注册页的任务就完成了。



## 3，注册页面表单提交功能
接下来我们要编写注册页面的提交表单功能。
1，接受前端传过来的表单数据。
2，校验数据。
3，写入数据库。
4，返回注册页（因为还没做首页）。
```
# users/views.py
def register_handle(request):
    '''进行用户注册处理'''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    # 进行数据校验
    if not all([username, password, email]):
        # 有数据为空
        return render(request, 'users/register.html', {'errmsg':'参数不能为空!'})

    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'users/register.html', {'errmsg':'邮箱不合法!'})

    # 进行业务处理:注册，向账户系统中添加账户
    # Passport.objects.create(username=username, password=password, email=email)
    passport = Passport.objects.add_one_passport(username=username, password=password, email=email)

    # 注册完，还是返回注册页。
    return redirect(reverse('user:register'))
```
配置urls.py
```
# users/urls.py
url(r'^register_handle/$', views.register_handle, name='register_handle'), # 用户注册处理
```
前端使用Form来发送POST请求。
```
<form method="post" action="/user/register_handle/">
```
注意添加csrf_token以及错误信息
```
{% csrf_token %}
{{errmsg}}
```
然后就完成注册功能了。之后需要实现发送激活邮件。

