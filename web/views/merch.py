import re
import random
from datetime import datetime

from django.shortcuts import render, redirect
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from web import models
from web.utils.bootstrap import BootStrapModelForm
from web.utils.pagination import Pagination


class MerchModelForm(BootStrapModelForm):
    class Meta:
        model = models.Merch
        fields = "__all__"
        # exclude = ["broker_id"]


def merch_list_broker(request):
    data_dict = {}
    search_data = request.GET.get('search', "")  # 有值拿值，没有值返回空字符串，拿到的是右上角搜索框的返回的值
    if search_data:
        data_dict["title__contains"] = search_data
    queryset = models.Merch.objects.filter(**data_dict).order_by("num")
    form = MerchModelForm()
    page_object = Pagination(request, queryset, page_size=7)
    context = {
        'search_data': search_data,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'merch_list_broker.html', context)


class MerchAddModelForm(BootStrapModelForm):
    class Meta:
        model = models.Merch
        fields = "__all__"
        exclude = ["broker"]


def merch_list_my(request):
    data_dict = {}
    search_data = request.GET.get('search', "")  # 有值拿值，没有值返回空字符串，拿到的是右上角搜索框的返回的值
    if search_data:
        data_dict["title__contains"] = search_data
    id = request.session['info']['id']
    queryset = models.Merch.objects.filter(broker_id=id, **data_dict).order_by("num")
    form = MerchAddModelForm()
    page_object = Pagination(request, queryset, page_size=7)
    context = {
        'search_data': search_data,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'merch_list_my.html', context)


@csrf_exempt
def merch_add(request):
    """增加商品"""
    form = MerchAddModelForm(data=request.POST)
    if form.is_valid():
        # 固定设置管理员ID，在当前登录的管理员账户的session中拿到
        form.instance.broker_id = request.session["info"]["id"]
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)


def merch_delete(request):
    """删除商品"""
    uid = request.GET.get("uid")
    exists = models.Merch.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    models.Merch.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def merch_detail(request):
    """点击编辑按钮，获取商品详细"""
    uid = request.GET.get("uid")
    # 用.values(字段名,字段名,字段名)拿到的不是对象，而是一个字典，json只能序列化基本的数据类型，不能序列化对象
    row_dict = models.Merch.objects.filter(id=uid).values('title', 'price', 'num', 'unit').first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    data_list = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(data_list)


@csrf_exempt
def merch_edit(request):
    """点击编辑对话框中的保存按钮"""
    # request.GET.get拿到的是url中?后面的参数，而request.POST.get拿到的是悄悄传递过来的数据，如表单提交，ajax请求时data属性传递过来的数据
    uid = request.GET.get("uid")
    row_object = models.Merch.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在,请刷新重试"})
    form = MerchAddModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)


class MerchBuyModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = ["num"]


def merch_list_consumer(request):
    """消费者看到的商品列表"""
    data_dict = {}
    search_data = request.GET.get('search', "")  # 有值拿值，没有值返回空字符串，拿到的是右上角搜索框的返回的值
    if search_data:
        data_dict["title__contains"] = search_data
    queryset = models.Merch.objects.filter(**data_dict).order_by("price")
    form = MerchBuyModelForm()
    page_object = Pagination(request, queryset, page_size=7)
    context = {
        'search_data': search_data,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'merch_list_consumer.html', context)


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"


@csrf_exempt
def merch_buy(request):
    """消费者点击购买商品"""
    uid = request.GET.get("uid")
    row_object = models.Merch.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在,请刷新重试"})
    buyer = request.session['info']['id']
    broker = row_object.broker.id
    buyer_address = request.session['info']['address']
    buyer_telephone = request.session['info']['telephone']
    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100, 999))
    order_time = datetime.now().strftime("%Y年%m月%d日%H时%M分%S秒")
    # 判断输入的数量是否符合要求
    # if not request.POST.get('num'):
    #     return JsonResponse({"status": False, "tips":"数量不能为空"})
    if not re.match('[+]?\d+$', request.POST.get('num')):
        return JsonResponse({"status": False, "tips": "请输入正整数"})
    num = int(request.POST.get('num'))
    if num > row_object.num or num == 0:
        return JsonResponse({"status": False, "tips": "库存不足"})
    result_num = row_object.num - num
    models.Merch.objects.filter(id=uid).update(num=result_num)
    models.Order.objects.create(title=row_object.title, price=row_object.price, num=num, unit=row_object.unit,
                                broker_id=broker, buyer_id=buyer, buyer_address=buyer_address,
                                buyer_telephone=buyer_telephone, order_id=order_id, order_time=order_time)
    return JsonResponse({"status": True})
    # data_dict = {"status": False, "error": form.errors}
    # return JsonResponse(data_dict)
    # data=[form.instance.title,form.instance.price,form.instance.num,form.instance.unit,form.instance.broker,
    #  form.instance.buyer,form.instance.buyer_address,form.instance.buyer_telephone,form.instance.order_id,form.instance.order_time]
    # data_dict = {"status": False, "data": data}
    # return JsonResponse(data_dict)
