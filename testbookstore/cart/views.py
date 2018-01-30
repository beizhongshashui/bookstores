from django.shortcuts import render
from django.http import JsonResponse
from books.models import Books
from utils.decorators import login_required
from django_redis import get_redis_connection


@login_required
def cart_add(request):

	'''想购物车添加数据'''
	if not request.session.has_key('islogin'):
		return JsonResponse({'res':0,'errmsg':'请先登录'})

	

	#接收数据
	books_id =request.POST.get('books_id')
	books_count = request.POST.get('books_count')
	
	if not all([books_id,books_count]):
		return JsonResponse({'res':1,'errmsg':'数据不完整'})
	
	books =Books.objects.get_books_by_id(books_id=books_id)
	if books is None :
		return JsonResponse({'res':2,'errmsg':'商品不存在'})

	try:
		count =int(books_count)

	except Exception as e:
		return JsonResponse({'res':3,'errmsg':'商品数量必须是数字'})
	
	conn = get_redis_connection('default')
	cart_key = 'cart_%d' %request.session.get('passport_id')
	
	res =conn.hget(cart_key,books_id)
	
	if res is None:
		res = count 

	else:
		res = int(res) +count
	
	if res > books.stock:
        # 库存不足
		return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
	else:
		conn.hset(cart_key, books_id, res)

	return JsonResponse({'res':5})


@login_required
def cart_count(request):
    '''获取用户购物车中商品的数目'''
    
    # 计算用户购物车商品的数量
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')
    # res = conn.hlen(cart_key) 显示商品的条目数
    res = 0
    res_list = conn.hvals(cart_key)

    for i in res_list:
        res += int(i)

    # 返回结果
    return JsonResponse({'res': res})

@login_required
def cart_update(request):
    '''更新购物车商品数目'''
   
    # 接收数据
    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')

    # 数据的校验
    if not all([books_id, books_count]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

    try:
        books_count = int(books_count)
    except Exception as e:
        return JsonResponse({'res': 3, 'errmsg': '商品数目必须为数字'})

    # 更新操作
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')

    # 判断商品库存
    if books_count > books.stock:
        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

    conn.hset(cart_key, books_id, books_count)

    return JsonResponse({'res': 5})
@login_required
def cart_del(request):
    '''删除用户购物车中商品的信息'''
    
    # 接收数据
    books_id = request.POST.get('books_id')

    # 校验商品是否存放
    if not all([books_id]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res': 2, 'errmsg': '商品不存存'})

    # 删除购物车商品信息
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')
    conn.hdel(cart_key, books_id)

    # 返回信息
    return JsonResponse({'res': 3})

@login_required
def cart_show(request):
    '''显示用户购物车页面'''
    passport_id = request.session.get('passport_id')
    # 获取用户购物车的记录
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % passport_id
    res_dict = conn.hgetall(cart_key)

    books_list = []
    # 保存所有商品的总数
    total_count = 0
    # 保存所有商品的总价格
    total_price = 0

    # 遍历res_dict获取商品的数据
    for id, count in res_dict.items():
        # 根据id获取商品的信息
        books = Books.objects.get_books_by_id(books_id=id)
        # 保存商品的数目
        books.count = count

        # 保存商品的小计
        books.amount = int(count) * books.price
        # books_li.append((books, count))
        books_list.append(books)
        print('count:%s,books.price：%s' %(count,books.price))
        total_count += int(count)
        total_price += int(count) * books.price


    # 定义模板上下文
    context = {
        'books_list': books_list,
        'total_count': total_count,
        'total_price': total_price,
    }
    # print('books_list :%s,total_count :%d ,total: %s ' %(books_list,total_count,total_price))

    return render(request, 'cart/cart.html', context)


