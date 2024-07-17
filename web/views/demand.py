from django.shortcuts import render, redirect
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse

from web import models
from web.utils.bootstrap import BootStrapModelForm
from web.utils.pagination import Pagination


class DemandAddModelForm(BootStrapModelForm):
    class Meta:
        model = models.Demand
        fields = "__all__"
        exclude = ["buyer"]


def demand_list_consumer(request):
    data_dict = {}
    search_data = request.GET.get('search', "")  # 有值拿值，没有值返回空字符串，拿到的是右上角搜索框的返回的值
    if search_data:
        data_dict["title__contains"] = search_data
    id = request.session['info']['id']
    queryset = models.Demand.objects.filter(buyer_id=id, **data_dict).order_by("num")
    form = DemandAddModelForm()
    page_object = Pagination(request, queryset, page_size=7)
    context = {
        'search_data': search_data,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'demand_list_consumer.html', context)


@csrf_exempt
def demand_add(request):
    """增加商品"""
    form = DemandAddModelForm(data=request.POST)
    if form.is_valid():
        # 固定设置管理员ID，在当前登录的管理员账户的session中拿到
        form.instance.buyer_id = request.session["info"]["id"]
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)


def demand_delete(request):
    """删除商品"""
    uid = request.GET.get("uid")
    exists = models.Demand.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    models.Demand.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def demand_detail(request):
    """点击编辑按钮，获取商品详细"""
    uid = request.GET.get("uid")
    # 用.values(字段名,字段名,字段名)拿到的不是对象，而是一个字典，json只能序列化基本的数据类型，不能序列化对象
    row_dict = models.Demand.objects.filter(id=uid).values('title', 'category', 'num', 'unit').first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    data_list = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(data_list)


@csrf_exempt
def demand_edit(request):
    """点击编辑对话框中的保存按钮"""
    # request.GET.get拿到的是url中?后面的参数，而request.POST.get拿到的是悄悄传递过来的数据，如表单提交，ajax请求时data属性传递过来的数据
    uid = request.GET.get("uid")
    row_object = models.Demand.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在,请刷新重试"})
    form = DemandAddModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)


class DemandBrokerModelForm(BootStrapModelForm):
    class Meta:
        model = models.Demand
        fields = "__all__"
        # exclude = [""]


def demand_list_broker(request):
    data_dict = {}
    search_data = request.GET.get('search', "")  # 有值拿值，没有值返回空字符串，拿到的是右上角搜索框的返回的值
    if search_data:
        data_dict["title__contains"] = search_data
    queryset = models.Demand.objects.filter(**data_dict).order_by("id")
    form = DemandBrokerModelForm()
    page_object = Pagination(request, queryset, page_size=6)
    context = {
        'search_data': search_data,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'demand_list_broker.html', context)
