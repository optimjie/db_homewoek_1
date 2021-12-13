from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import time,os

# 导入
from myapp.models.place.place import Place

# 用于解析xml文件
from xml.dom.minidom import parse
import xml.dom.minidom





# def index(request):
#     return HttpResponse("网页")

# def tmp(request):
#     return HttpResponse("tmp")

def index(request):
    return render(request, "index.html")  # templates往下


def showUpload(request):
    """上传"""
    return render(request, 'upload.html')
 
 
def upload(request):
    if request.method == "POST":
        myfile = request.FILES.get('pic', None)
        try:
            suffix = str(myfile.name.split('.')[-1])
            times = str(time.time()).split('.').pop()   # 生成时间戳，取小数点后的值
            fil = str(myfile.name.split('.')[0])
            filename = fil + '.' + suffix
            filename_dir = settings.MEDIA_ROOT
            with open(filename_dir + filename, 'wb+') as destination:
                for chunk in myfile.chunks():
                    destination.write(chunk)
                destination.close()
        except:
            return HttpResponse("提交失败")
    else:
        return redirect('showUpdate')
    # return HttpResponse('上传成功')
    return render(request, 'list.html')

def listFile(request):
    ans = []
    for root, dirs, files in os.walk("/home/optimjie/db_homework_data"):

        for f in files:
            all_name = os.path.join(root, f)
            l = all_name.split('/')
            ans.append(l[len(l) - 1])
    
    return JsonResponse({
        'data': ans,
    })

# 以下为测试数据库
def dbDemo(request):
    return render(request, "dbDemo.html") 

def dbDemoAdd(request):
    if request.POST:
        Place.objects.create(placeName = request.POST['place_name'], placeId = request.POST['place_id'],
                             parent = request.POST['parent_id'])
    return HttpResponse('添加成功')


# 解析xml文件，将每条数据插入到数据库中
def parse(request):
    DOMTree = xml.dom.minidom.parse("/home/optimjie/db_homework_1/media/data.xml")
    root = DOMTree.documentElement

    provs = root.getElementsByTagName("prov")

    p_cnt = 0
    for prov in provs:
        if prov.getAttribute("text") == "":
            break
        p_cnt = p_cnt + 1
        p_id = ""
        if p_cnt < 10:
            p_id = "0" + str(p_cnt)
        else:
            p_id = str(p_cnt)
        # print("地方编号：" + p_id, "地方名称：" + prov.getAttribute("text"), "父id：" + "-1")
        Place.objects.create(placeName = prov.getAttribute("text"), placeId = p_id,
                             parent = "-1")
        citys = prov.getElementsByTagName("city")
        c_cnt = 0
        for city in citys:
            if city.getAttribute("text") == "":
                break
            c_cnt = c_cnt + 1
            c_id = p_id
            if c_cnt < 10:
                c_id = c_id + "0" + str(c_cnt)
            else:
                c_id = c_id + str(c_cnt)
            # print("  地方编号：" + c_id, "地方名称：" + city.getAttribute("text"), "父id：" + p_id)
            Place.objects.create(placeName = city.getAttribute("text"), placeId = c_id,
                             parent = p_id)
            countys = city.getElementsByTagName("county")
            co_cnt = 0
            for county in countys:
                if county.getAttribute("text") == "":
                    break
                co_cnt = co_cnt + 1
                co_id = c_id
                if co_cnt < 10:
                    co_id = c_id + "0" + str(co_cnt)
                else:
                    co_id = c_id + str(co_cnt)
                # print("    地方编号：" + co_id, "地方名称：" + county.getAttribute("text"), "父id：" + c_id)
                Place.objects.create(placeName = county.getAttribute("text"), placeId = co_id,
                             parent = c_id)

    return HttpResponse(provs.length)

class Node:
    label = ''
    children = []

    def __init__(self, label, children):
        self.label = label
        self.children = children

class NodeInDb:
    placeName = ''
    placeId = ''
    parent = ''

    def __init__(self, placeName, placeId, parent):
        self.placeName = placeName
        self.placeId = placeId
        self.parent = parent

# 展示数据页面
def display(request):
    # return render(request, 'display.html')
    res = []
    nodes = Place.objects.all()

    # 还考虑啥扩展性啊，直接暴力就完事了
    a = []  # 一级
    b = []  # 二级
    c = []  # 三级

    mp = {}

    # data是一个数组，每一个元素是包含下面的键值对
    data = [{'placeName': node.placeName, 'placeId': node.placeId, 'parent': node.parent} for node in nodes]
    """
    通过这种方式去获取值
    for v in data:
        print(v['placeName'])
    """
    for v in data:
        id_len = len(v['placeId'])
        placeName = v['placeName']
        placeId = v['placeId']
        parent = v['parent']
        mp[placeId] = placeName
        if id_len == 2:
            a.append(NodeInDb(placeName, placeId, parent))
        elif id_len == 4:
            b.append(NodeInDb(placeName, placeId, parent))
        else:
            c.append(NodeInDb(placeName, placeId, parent))
    
    for a_v in a:
        res.append({'label': a_v.placeName, 'children': []})

    for b_v in b:
        parentName = mp[b_v.parent]
        for res_v in res:
            if parentName == res_v['label']:
                res_v['children'].append({'label': b_v.placeName, 'children': []})
                break

    for c_v in c:
        parentName = mp[c_v.parent]
        for res_v in res:
            children = res_v['children']
            for children_v in children:
                if parentName == children_v['label']:
                    children_v['children'].append({'label': c_v.placeName, 'children': []})
                    break

    
    return JsonResponse({
        'data': res,
    })

# 返回树的json格式
def treeList(request):
    res = []

    nodes = Place.objects.all()
    
    return JsonResponse({
        'data': nodes,
    })

# 删除表中所有数据

def deleteAll(request):
    nodes = Place.objects.all()
    for node in nodes:
        id = node.id
        Place.objects.filter(id=id).delete()

    return JsonResponse({
        'message': 'success',
    })