from django.db import models
from db.base_model import BaseModel
from hashlib import sha1

# Create your models here


def get_hash(str):
	sh = sha1()
	sh.update(str.encode('utf8'))

	return sh.hexdigest()

class PassportManager(models.Manager):
	def add_one_passport(self,username,password,email):
		'''添加账户信息'''

		passport = self.create(username = username,password=get_hash(password),email=email)

		return passport
	def get_one_passport(self,username,password):
		'''根据用户密码查询账户'''
		try:
			passport = self.get(username=username,password=get_hash(password))
		except self.model.DoesNotExist:
			'''账户不许存在'''
			passport = None
		return passport

	def check_passport(self, username):
		try:
			passport = self.get(username =username)
		except self.model.DoesNotExist:
			passport = None
		return  passport


class AddressManager(models.Manager):
	'''地址管理器'''
	def get_default_address(self,passport_id):
		try:
			addr = self.get(passport_id=passport_id)
		except self.model.DoesNotExist:
			addr = None
		
		return addr

	def add_new_address(self,passport_id,recipient_name,recipient_addr,
		recipient_phone,zip_code):
		'''添加新地址'''
		#判断是否有默认地址
		addr = self.get_default_address(passport_id=passport_id)

		if addr:
			is_default = False
		else :
			is_default = True

		addr = self.create(passport_id=passport_id,
			recipient_name=recipient_name,recipient_addr=recipient_addr,
			recipient_phone=recipient_phone,is_default=is_default)

		return addr

	#怎样修改默认地址
	def change_default_addr(self,change_addr_id):
		try:
			addr = self.filter(default=True).update(default=False)
		except self.model.DoesNotExist:
			addr = None
		self.get(id=change_addr_id).update(default=True)
		



class Passport(BaseModel):
	"""docstring for Passport"""
	username = models.CharField(max_length=20,verbose_name='用户名')
	password = models.CharField(max_length = 100,verbose_name='用户密码')
	email = models.EmailField(verbose_name='邮箱')
	is_avtive = models.BooleanField(default=False ,verbose_name = '激活状态')

	objects = PassportManager()
	class Meta:
		db_table = 's_user_accout'




class Address(BaseModel):
	'''地址模板类'''
	recipient_name = models.CharField(max_length=20,verbose_name='收件人')
	recipient_addr = models.CharField(max_length=256,verbose_name='收货地址')
	zip_code = models.CharField(max_length = 6,verbose_name = '邮政编码')
	recipient_phone = models.CharField(max_length=11,verbose_name='手机号码')
	is_default = models.BooleanField(default=False,verbose_name='是否默认')
	passport = models.ForeignKey('Passport',verbose_name='账户')

	objects = AddressManager()

	class Meta:
		db_table = 's_uer_adress'

