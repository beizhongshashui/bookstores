from django.shortcuts import render , redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import re
from user.models import Passport
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Create your views here.s

def register(request):



	return render(request,'users/register.html')

def  register_handle(request):

	# if request.method =='POST':
		username = request.POST.get('user_name')
		password = request.POST.get('pwd')
		email = request.POST.get('email')

		# 数据校验
		if not all([username,password,email]):
			return render(request,'users/register.html',{'errmsg':'参数不能为空'})
			#校验邮箱
		if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
			return render(request,'users/register.html',{'errmsg':'邮箱不合法！'})

		# p = Passport.objects.check_passport(username=username)

		# if p :
		# 	return render(request,'uers/register.html',{'errmsg':'用户名已經存在'})
		
		#进行业务注册
		passport = Passport.objects.add_one_passport(username=username,password=password,email=email)

		return redirect(reverse('user:register'))
		# return render(request,'uers/register.html',{'errmsg':'用户名已經存在。。。。'})


	# else :
	# 	pass

	# return HttpResponse('ok')
