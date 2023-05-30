from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from . models import Category,Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def allProductCat(request, c_slug=None):
    c_page = None
    products_list = None
    products = None
    paginator = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.all().filter(category=c_page, available=True)
        paginator = Paginator(products_list, 6)
    else:
        products_list = Product.objects.all().filter(available=True)
        paginator = Paginator(products_list, 6)

    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        products = paginator.page(1)

    return render(request, "category.html", {'category': c_page, 'products': products})


def productDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    # except Expection as e:
    #     raise e
    except Product.DoesNotExist:
        # Handle the case when the product does not exist
        raise Http404("Product does not exist")

    return render(request,'product.html',{'product':product})
