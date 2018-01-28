from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

def login_required(view_func):
    '''登录判断'''
    def wapper(request,*args,**kwargs):
        if request.session.has_key('islogin'):
            return view_func(request,*args,**kwargs)
        else:
            return redirect(reverse('user:login'))
           
