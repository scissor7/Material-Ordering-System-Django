from django.conf import settings


def init_permission(request,user):
    """
    权限和菜单信息初始化，以后使用时，需要在登陆成功后调用该方法将权限和菜单信息放入session
    :param request:
    :param user:
    :return:
    """

    # 3. 获取用户信息和权限信息写入session,通过.values拿到的是每个角色对应的一个字典，如果有多个角色就有多个字典
    # 如：[{'permissions__url':'/index/','permissions__is_menu':False,'permissions__title':'主页'},
    #     {'permissions__url':'/merch/list/','permissions__is_menu':True,'permissions__title':'商品列表'}]
    #可以用for循环拿到每个字典
    permission_queryset = user.roles.filter(permissions__url__isnull=False).values('permissions__url',
                                                                                  'permissions__is_menu',
                                                                                  'permissions__title',
                                                                                  'permissions__icon',
                                                                                  ).distinct()

    #request.session

    menu_list = []
    permission_list = []

    for row in permission_queryset:
        permission_list.append({'permissions__url': row['permissions__url']})

        if row['permissions__is_menu']:
            menu_list.append(
                {'title': row['permissions__title'], 'icon': row['permissions__icon'], 'url': row['permissions__url']})

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_list