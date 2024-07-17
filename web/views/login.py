from io import BytesIO

from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse

from rbac import models
from rbac.service.init_permission import init_permission
# from web.utils.encrypt import md5
from web.utils.code import check_code
from web.utils.bootstrap import BootStrapForm
from web.utils.bootstrap import BootStrapModelForm


class LoginForm(BootStrapForm):
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    # def clean_password(self):
    #     pwd = self.cleaned_data.get("password")
    #     return md5(pwd)


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # form.is_valid()用于验证用户填入的信息不为空,并且会把转义字符当作自身，防止sql注入语句
        user_input_code = form.cleaned_data.pop('code')  # 将用户输入的验证码字母赋值到user_input_code中，并把code从form中删除
        code = request.session.get('image_code', "")
        # 验证用户输入的验证码和session中储存的验证码是否相同
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        admin_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        roles_queryset = []
        for row in admin_object.roles.all():
            roles_queryset.append(row.title)
        dict = {'id': admin_object.id,
                'name': admin_object.name,
                'address': admin_object.address,
                'telephone': admin_object.telephone,
                'role': roles_queryset}
        request.session['info'] = dict
        init_permission(request, admin_object)
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/index/')
    return render(request, 'login.html', {"form": form})


def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数，生成图片
    img, code_string = check_code()
    # 将验证码写入自己的session中，(以便于后续获取验证码再进行校验)
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(120)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')


class UserInfoModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.UserInfo
        # fields = ["name","password","confirm_password","role","telephone","address"]
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # return md5(pwd)
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        # confirm = md5(self.cleaned_data.get("confirm_password"))
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        if len(txt_name) > 8 or len(txt_name) < 2:
            # 验证不通过
            raise ValidationError("用户名必须大于2位小于8位")
        exists = models.UserInfo.objects.filter(name=txt_name).exists()
        if exists:
            raise ValidationError("用户名已被注册")
        return txt_name


def register(request):
    """注册用户"""
    title = "注册"
    tip = "none"
    if request.method == 'GET':
        form = UserInfoModelForm()
        dict = {"form": form, "title": title, "attr_login": "block", "attr_index": "none", "tip": tip}
        return render(request, 'change.html', dict)
    form = UserInfoModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login/')
    # return render(request, 'change.html')
    dict = {"form": form, "attr_login": "block", "attr_index": "none", "tip": tip}
    return render(request, 'change.html', dict)
