from django.db import models


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)

    is_menu = models.BooleanField(verbose_name='是否可做菜单',default=False)
    icon = models.CharField(max_length=32,null=True,blank=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    telephone = models.CharField(verbose_name='手机号码', max_length=32,default=0)
    roles = models.ManyToManyField(verbose_name='身份', to='Role', blank=True)
    address = models.CharField(verbose_name='地址', max_length=64,default="未填写")

    def __str__(self):
        return self.name
