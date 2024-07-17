from django.contrib import admin
from django.urls import path
from web.views import index,login,merch,order,userinfo,demand,chart,tips




urlpatterns = [
    #admin后台管理
    path('admin/', admin.site.urls),
    #登录页面
    path('login/', login.login),
    path('logout/',login.logout),
    path('image/code/',login.image_code),
    path('register/',login.register),
    #无权访问
    path('not/found/',tips.not_found),
    #用户信息管理
    path('userinfo/list/',userinfo.userinfo_list),
    path('userinfo/detail/',userinfo.userinfo_detail),
    path('userinfo/edit/',userinfo.userinfo_edit),
    path('userinfo/safe/',userinfo.userinfo_safe),
    #主页
    path('index/', index.index),
    #商品管理
    path('merch/list/broker/', merch.merch_list_broker),
    path('merch/list/my/',merch.merch_list_my),
    path('merch/add/',merch.merch_add),
    path('merch/detail/',merch.merch_detail),
    path('merch/edit/',merch.merch_edit),
    path('merch/delete/',merch.merch_delete),
    path('merch/list/consumer/',merch.merch_list_consumer),
    path('merch/buy/',merch.merch_buy),
    #订单管理
    path('order/list/broker/', order.order_list_broker),
    path('order/list/consumer/',order.order_list_consumer),
    #消费者需求管理
    path('demand/list/consumer/',demand.demand_list_consumer),
    path('demand/add/',demand.demand_add),
    path('demand/detail/',demand.demand_detail),
    path('demand/edit/',demand.demand_edit),
    path('demand/delete/',demand.demand_delete),
    path('demand/list/broker/',demand.demand_list_broker),
    #图表数据分析
    path('chart/pie/',chart.chart_pie),
    path('chart/word_cloud/',chart.chart_word_cloud),
]
