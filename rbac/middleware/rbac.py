from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect,HttpResponse,render
import re

class RbacMiddleware(MiddlewareMixin):
    """
    权限控制的中间件
    """

    def process_request(self, request):
        """
        权限控制
        :param request:
        :return:
        """
        # 1. 获取当前请求URL
        current_url = request.path_info

        # 1.5 白名单处理
        # for reg in settings.VALID_URL:
        # for reg in ["/login/","/admin/","/image/code/"]:
            #if re.match(str(reg),str(current_url)):
            #if current_url == reg:
                # return

        if request.path_info in ["/login/","/image/code/","/register/","/not/found/"]:
            return
        if re.match('^/admin/.*',current_url):
            return

        # 2. 获取当前用户session中所有的权限
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_list:
            return redirect('/login/')

        # 3. 进行权限校验
        flag = False
        for item in permission_list:
            reg = "^%s" % item.get('permissions__url')
            if re.match(reg, current_url):
            #reg =item.get('permissions__url')
            #if reg == current_url:
                flag = True
                break
        if not flag:
            return render(request,'not_found.html')
