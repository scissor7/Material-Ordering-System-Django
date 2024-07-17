from django.db import models
from rbac.models import UserInfo


class Merch(models.Model):
    title = models.CharField(verbose_name="商品名称", max_length=64)
    # max_digits：总位数(不包括小数点和符号)
    price = models.DecimalField(verbose_name="价格(元)",max_digits=10,decimal_places=2,default=0)
    num = models.IntegerField(verbose_name="库存数量")
    unit = models.CharField(verbose_name="每件商品单位", max_length=32)
    broker = models.ForeignKey(verbose_name="卖家", to=UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    title = models.CharField(verbose_name="商品名称", max_length=64)
    price = models.DecimalField(verbose_name="价格(元)", max_digits=10, decimal_places=2, default=0)
    num = models.IntegerField(verbose_name="购买数量")
    unit = models.CharField(verbose_name="每件商品单位", max_length=32)
    broker = models.ForeignKey(verbose_name="卖家", to=UserInfo, on_delete=models.CASCADE,related_name="UserInfo_broker")
    buyer = models.ForeignKey(verbose_name="消费者", to=UserInfo, on_delete=models.CASCADE,related_name="UserInfo_buyer")
    order_time = models.CharField(verbose_name="下单时间", max_length=32)
    order_id = models.CharField(verbose_name="订单编号", max_length=64)
    buyer_address = models.CharField(verbose_name="买方收货地址", max_length=64)
    buyer_telephone = models.CharField(verbose_name="买方手机号码", max_length=32)

    def __str__(self):
        return self.title


class Demand(models.Model):
    title = models.CharField(verbose_name="商品名称", max_length=64)
    merch_choices = (
        (1, "蔬菜"),(2, "肉制品"),(3, "水果"),(4, "零食"),(5, "方便速食"),(6, "奶制品"),(7, "饮料"),(8, "纸巾"),
        (9, "酒类饮品"),(10, "洗浴用品"),(11, "一般药品"),(12, "果干"),(13, "清洁工具"),(14,"数码设备"),
        (15,"手机配件"),(16,"美妆"),(17,"服饰"),(18,"保健品"),(19,"母婴用品"),(20,"其他"),
    )
    category = models.SmallIntegerField(verbose_name="商品类别",choices=merch_choices)
    num = models.IntegerField(verbose_name="需求数量")
    unit = models.CharField(verbose_name="每件商品单位", max_length=32)
    buyer = models.ForeignKey(verbose_name="消费者", to=UserInfo, on_delete=models.CASCADE)