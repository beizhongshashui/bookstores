from django.shortcuts import render , redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import re
from user.models import Passport,Address
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.http import JsonResponse
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

		return redirect(reverse('books:index'))
		# return render(request,'uers/register.html',{'errmsg':'用户名已經存在。。。。'})

def login(request):
	username = ''
	checked = ''
	context = {

		'username' :username,
		'checked':checked,
	}
	return render(request,'users/login.html',context)

def login_check(request):
	'''进行用户检查'''
	username = request.POST.get('username')
	password = request.POST.get('password')
	remember = request.POST.get('remember')

	print(remember)
	print(password)
	print(password)
	if not all([username ,password,remember]):
		return JsonResponse({'res':2})

	passport = Passport.objects.get_one_passport(username=username,
		password=password)

	if passport:
		'''用户名正确'''
		#构建给前端的的数据
		next_url = request.session.get('url_path',reverse('books:index'))
		# next_url = reverse('books:index')
		
		jres = JsonResponse({'res':1,'next_url':next_url})

		if remember =='true':
			jres.set_cookie('username',username,max_age=7*24*3600)

		else :
			jres.delete_cookie('username')

		request.session['islogin'] = True
		request.session['username'] = username
		request.session['passport_id'] = passport.id

		return jres

	else:
		return JsonResponse({'res':0})
def logout(request):
    '''用户退出登录'''
    # 清空用户的session信息
    request.session.flush()
    # 跳转到首页
    return redirect(reverse('books:index'))


def user(request):
	'''用户中心'''
	passport_id =request.session.get('passport_id')

	addr = Address.objects.get_default_address(passport_id=passport_id)
	book_list = []
	context={
	'addr':addr,
	'book_list':book_list,
	'page':'user'
	}

	return render(request,'users/user_center_info.html',context)


