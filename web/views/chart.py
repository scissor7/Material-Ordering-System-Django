import jieba
import operator

from django.http import JsonResponse

from web import models


def chart_pie(request):
    # list_a = []
    db_data_dict = {}
    db_data_list = []
    objects = models.Demand.objects.all()
    for object in objects:
        key = object.get_category_display()
        num = object.num
        db_data_dict[key] = db_data_dict.get(key, 0) + object.num
    # for item in db_data_dict.values():
    #     list_a.append(item)
    # list_a.sort(reverse=True)
    sort_val_dict = dict(sorted(db_data_dict.items(), key=operator.itemgetter(1), reverse=True))  # 将字典按值排序

    for name in sort_val_dict.keys():
        dict_item = {}
        dict_item["value"] = sort_val_dict[name]
        dict_item["name"] = name
        db_data_list.append(dict_item)

    result = {
        "status": True,
        "data": db_data_list
        # "data": db_data_dict
    }
    return JsonResponse(result, safe=False)


def chart_word_cloud(request):
    db_data_str = ""
    db_data_list = []
    objects = models.Demand.objects.all()
    for object in objects:
        dict_object = []
        for i in range(0, object.num):
            dict_object.append(object.title)
        db_data_str = db_data_str + ",".join(dict_object)
    words = jieba.lcut(db_data_str)
    db_data_dict = {}
    for word in words:
        if len(word) == 1:
            continue
        db_data_dict[word] = db_data_dict.get(word, 0) + 1
    for name in db_data_dict.keys():
        dict_item = {}
        dict_item["value"] = db_data_dict[name]
        dict_item["name"] = name
        db_data_list.append(dict_item)

    result = {
        "status": True,
        "data": db_data_list
        # "data": words
    }
    return JsonResponse(result, safe=False)
