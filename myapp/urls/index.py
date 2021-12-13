from django.urls import path, include
from myapp.views.index import index, upload, showUpload, listFile, dbDemo, dbDemoAdd, parse, display, deleteAll
urlpatterns = [
    path('', index),
    path('upload/', upload, name="upload"),  # 用于发送文件上传请求
    path('showUpload/', showUpload, name="showUpload"),  # 用于加载模板视图
    path('listFile/', listFile),  
    path('dbDemo/', dbDemo),  # 数据库测试
    path('dbDemoAdd/', dbDemoAdd),   # 数据库添加测试
    path('parse/', parse),  # xml文件解析
    path('display/', display),  # 数据展示
    path('deleteAll', deleteAll),  # 删除表中所有数据
]
