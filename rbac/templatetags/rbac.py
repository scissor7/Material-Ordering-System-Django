from django.template import Library
from django.conf import settings
import re
register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    生成菜单
    :param request:
    :return:
    """

    menu_list = request.session.get(settings.MENU_SESSION_KEY)

    for item in menu_list:
        reg = "^%s$" % item['url']
        if re.match(reg,request.path_info):
            item['font'] = 'font-weight:bold;font-size:120%;color:000;'
            item['bk_gd'] = 'background-color:#E8E8E8;'
    return {'menu_list':menu_list}