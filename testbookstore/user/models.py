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
	def get_ont_passport(self,username,password):
		'''根据用户密码查询账户'''
		try:
			passport = self.get(username=username,password=get_hash(password))
		except self.model.DoseNotExist:
			'''账户不许存在'''
			passport = None
		return passport

		


class Passport(BaseModel):
	"""docstring for Passport"""
	username = models.CharField(max_length=20,verbose_name='用户名')
	password = models.CharField(max_length = 20,verbose_name='用户密码')
	email = models.EmailField(verbose_name='邮箱')
	is_avtive = models.BooleanField(default=False ,verbose_name = '激活状态')

	objects = PassportManager()
	class Meta:
		db_table = 's_user_accout'
