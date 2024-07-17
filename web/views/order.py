from django.shortcuts import render,redirect,HttpResponse

from web import models
from web.utils.bootstrap import BootStrapModelForm
from web.utils.pagination import Pagination



class OrderBrokerModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        exclude = ["id","broker"]


def order_list_broker(request):
    data_dict = {}
    search_data = request.GET.get('search', "")  # 有值拿值，没有值返回空字符串，拿到的是右上角搜索框的返回的值
    if search_data:
        data_dict["title__contains"] = search_data
    broker_id = request.session["info"]["id"]
    queryset = models.Order.objects.filter(broker=broker_id,**data_dict).order_by("order_time")
    form = OrderBrokerModelForm()
    page_object = Pagination(request, queryset, page_size=8)
    context = {
        'search_data': search_data,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'order_list_broker.html', context)


class OrderConsumerModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        exclude = ["id","buyer"]


def order_list_consumer(request):
    data_dict = {}
    search_data = request.GET.get('search', "")  # 有值拿值，没有值返回空字符串，拿到的是右上角搜索框的返回的值
    if search_data:
        data_dict["title__contains"] = search_data
    buyer_id = request.session["info"]["id"]
    queryset = models.Order.objects.filter(buyer=buyer_id,**data_dict).order_by("-order_time")
    form = OrderConsumerModelForm()
    page_object = Pagination(request, queryset, page_size=6)
    context = {
        'search_data': search_data,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'order_list_consumer.html', context)