from django.db import models
from tinymce.models import HTMLField 
from books.enums import *
from db.base_model import BaseModel
class HeroInfo(models.Model):
    hconrent =HTMLField()



class BooksManager(models.Manager):
    '''商品模型管理类'''
    def get_books_by_type(self,type_id,limit=None,sort='default'):
        '''根据商品类型id查询商品信息'''
        if sort =='new':
            order_by=('-create_time',)
        elif sort == 'hot':
            order_by=('-sales',)
        elif sort =='price':
            order_by = ('price',)
        else:
            order_by = ('-pk',)#按照primary key 降顺排序

        books_li = self.filter(type_id = type_id).order_by(*order_by)

        if limit:
            books_li =books_li[:limit]
        return books_li

    def get_books_by_id(self,books_id):
        '''根据商品id获取商品信息'''
        try:
            books = self.get(id=books_id)
        except self.model.DoesNotExist:
            books =None
        return books
    def add_book(self,type_id,name,desc,unit,price,stock,sales,detail,image,status):
        
        book = self.create(type_id=type_id,name=name,desc=desc,unit=unit,price=price,
            stock =stock,sales =sales,detail=detail,image=image,status=status)

        return book

  



class Books(BaseModel):
    '''商品模型类'''
    books_type_choices = ((k,v) for k,v in  BOOKS_TYPE.items())
    status_choices = ((k,v) for k,v in STATUS_CHOICE.items())
    type_id = models.SmallIntegerField(default=PYTHON,choices = books_type_choices,verbose_name='商品种类')
    name = models.CharField(max_length=20,verbose_name='商品名称')
    desc= models.CharField(max_length=128,verbose_name = '商品简介')
    unit = models.CharField(max_length = 20,verbose_name = '商品单位')
    price = models.DecimalField(max_digits = 10,decimal_places=2,verbose_name='商品价格')
    stock = models.IntegerField(default=1,verbose_name = '商品库存')
    sales = models.IntegerField(default=0,verbose_name= '商品销量')
    detail = HTMLField(verbose_name='商品详情')
    image = models.ImageField(upload_to='books',verbose_name='商品照片')
    status = models.SmallIntegerField(default = ONLINE,choices=status_choices,verbose_name='商品状态')

    objects = BooksManager()

    class Meta:
        db_table = 's_books'

