from web import models
from django import forms
from django.core.validators import RegexValidator    # 验证数据方法一:正则表达式
from django.core.exceptions import ValidationError   # 验证数据方法二:定义成员函数（钩子方法）
from web.utils.bootstrap import BootStrapModelForm



# 增删改用户所需要的类
class UserModelForm(BootStrapModelForm):
    # 做更多的字段校验
    name = forms.CharField(min_length=2,label="用户名")
    password = forms.CharField(min_length=6,max_length=14,label="密码")

    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","depart","gender"]
        # widgets = {"name":forms.TextInput(attrs={"class":"form-control"}) }


#靓号增加所需要的类，增加手机号时校验数据库中是否已存在手机号码
class PrettyModelForm(BootStrapModelForm):
    #验证数据方法一:重写字段，用正则表达式
    #mobile = forms.CharField(
        #label="手机号",
        #validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号必须以1开头，第二位在3-9之间，由11位数字组成'),],
    #)
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
        #fields = "__all__"   #表示所有字段
        # exclude = ['level'] 排除某个字段

    # 验证数据方法二：定义成员函数（钩子方法）
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("手机号位数必须为11位")
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile


#靓号编辑所需要的类，编辑时校验手机号码是否存在需排除自己本身
class PrettyEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
    # 验证数据方法二：定义成员函数（钩子方法）
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("手机号位数必须为11位")
        # self.instance.pk 是当前编辑那行的主键
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

