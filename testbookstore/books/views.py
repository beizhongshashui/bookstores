from django.shortcuts import render
from books.models import Books
from books.enums import *
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator


def index(request):
    python_new = Books.objects.get_books_by_type(PYTHON, 3, sort='new')
    python_hot = Books.objects.get_books_by_type(PYTHON, 4, sort='hot')
    javascript_new = Books.objects.get_books_by_type(JAVASCRIPT, 3, sort='new')
    javascript_hot = Books.objects.get_books_by_type(JAVASCRIPT, 4, sort='hot')
    algorithms_new = Books.objects.get_books_by_type(ALGORITHMS, 3, sort='new')
    algorithms_hot = Books.objects.get_books_by_type(ALGORITHMS, 4, sort='hot')
    machinelearning_new = Books.objects.get_books_by_type(MACHINELEARNING, 3, sort='new')
    machinelearning_hot = Books.objects.get_books_by_type(MACHINELEARNING, 4, sort='hot')
    operatingsystem_new = Books.objects.get_books_by_type(OPERATINGSYSTEM, 3, sort='new')
    operatingsystem_hot = Books.objects.get_books_by_type(OPERATINGSYSTEM, 4, sort='hot')
    database_new = Books.objects.get_books_by_type(DATABASE, 3, sort='new')
    database_hot = Books.objects.get_books_by_type(DATABASE, 4, sort='hot')

    context = {
    'python_new': python_new,
    'python_hot': python_hot,
    'javascript_new': javascript_new,
    'javascript_hot': javascript_hot,
    'algorithms_new': algorithms_new,
    'algorithms_hot': algorithms_hot,
    'machinelearning_new': machinelearning_new,
    'machinelearning_hot': machinelearning_hot,
    'operatingsystem_new': operatingsystem_new,
    'operatingsystem_hot': operatingsystem_hot,
    'database_new': database_new,
    'database_hot': database_hot,
    }

    return render(request,'books/index.html',context)

def detail(request,books_id):
    '''显示商品详情'''
    books = Books.objects.get_books_by_id(books_id=books_id)

    if books is None :
        return redirect(reverse('books:index'))

    books_list = Books.objects.get_books_by_type(type_id=books.type_id,limit=2,sort='new')

    context = {'books':books,'books_list':books_list}
    # print('books_list',books_list)
    return render(request,'books/detail.html',context)


