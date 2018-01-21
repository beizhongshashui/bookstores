from django.shortcuts import render 
from django.http import HttpResponse
import re
# Create your views here.

def register(request):



	return render(request,'users/register.html')

def  register_handle(request):

	if request.method =='post':
		username = request.POST.get('user_name')
		password = request.POST.get('pwd')
		email = request.POST.get('email')

		# 数据校验
		if not all([username,password,email]):
			return render(request,'user/register.html',{'errmsg':'参数不能为空'})
			#校验邮箱
		
	else :
		pass

	return HttpResponse('ok')
