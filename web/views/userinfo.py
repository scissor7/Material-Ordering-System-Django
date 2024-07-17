from django.shortcuts import render,redirect
from django import forms
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from rbac import models
from web.utils.bootstrap import BootStrapForm
from web.utils.bootstrap import BootStrapModelForm


class UserInfoListModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        exclude = ["name", "id", "password", "roles"]


def userinfo_list(request):
    """用户信息列表"""
    id = request.session.get('info')['id']
    name = request.session.get('info')['name']
    form = UserInfoListModelForm()
    queryset = models.UserInfo.objects.filter(id=id,name=name).first()
    return render(request,'userinfo_list.html',{'queryset':queryset,'form':form})


def userinfo_detail(request):
    """点击编辑按钮，获取用户信息详细"""
    uid = request.GET.get("uid")
    #用.filter拿到的是一个对象，对象不能Json序列化传给前端,
    #用.values(字段名,字段名,字段名)拿到的不是对象，而是一个字典，json只能序列化基本的数据类型，不能序列化对象
    row_dict = models.UserInfo.objects.filter(id=uid).values('telephone', 'address').first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    data_list = {
        "status": True,
        "data":row_dict
    }
    return JsonResponse(data_list)


@csrf_exempt  #免除csrf认证
def userinfo_edit(request):
    """点击编辑对话框中的保存按钮"""
    # request.GET.get拿到的是url中?后面的参数，而request.POST.get拿到的是悄悄传递过来的数据，如表单提交，ajax请求时data属性传递过来的数据
    uid = request.GET.get("uid")
    row_object = models.UserInfo.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在,请刷新重试"})
    form = UserInfoListModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status":True})
    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)


class UserInfoSafeModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.UserInfo
        fields = ["name","password","confirm_password"]
        #fields = "__all__"
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        #return md5(pwd)
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        #confirm = md5(self.cleaned_data.get("confirm_password"))
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        if len(txt_name) > 8 or len(txt_name) <2:
            # 验证不通过
            raise ValidationError("用户名必须大于2位小于8位")
        exists = models.UserInfo.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        if exists:
            raise ValidationError("用户名已被注册")
        return txt_name



def userinfo_safe(request):
    """编辑用户名和密码"""
    title = "账号安全"
    tip="block"
    id = request.session.get("info")["id"]
    row_object = models.UserInfo.objects.filter(id=id).first()
    if request.method == 'GET':
        form = UserInfoSafeModelForm(instance=row_object)
        dict={'form':form,'title':title,"attr_login":"none","attr_index":"block","tip":tip}
        return render(request,'change.html',dict)
    form = UserInfoSafeModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        request.session.clear()
        return redirect("/login/")
    dict={'form':form,'title':title,"attr_login":"none","attr_index":"block","tip":tip}
    return render(request,"change.html",dict)
