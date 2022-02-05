from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import F
from EIMS import settings
from .models import customer, inventory, Type
from .models import supplier, supply, agent, Productinfo, Sell
from User.models import admin_user,Booking
import os
from django.db import transaction
import django_excel
import logging
import xlrd
import xlwt
from django.core.files.base import ContentFile

# Create your views here.

def admin_view(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, '../templates/admin_index.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, '../templates/admin_index.html')
        return HttpResponseRedirect('/')


# 顾客首页
def cus(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'customer/cus.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'customer/cus.html')
        return HttpResponseRedirect('/')


# 添加查询客户
def input_cus_info(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'customer/input_cus_info.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'customer/input_cus_info.html')
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        if request.POST.get('whichform') =='1':
            name = request.POST.get('name')
            sex = request.POST.get('sex')
            age = request.POST.get('age')
            Idcard = request.POST.get('Idcard')
            mobile = request.POST.get('mobile')
            province = request.POST.get('province')
            city = request.POST.get('city')
            address = request.POST.get('address')
            note = request.POST.get('note')

            if not Idcard:
                return render(request, 'customer/input_cus_info.html', {"error": '身份证号不能为空'})
            exist_Idcard = customer.objects.filter(Idcard=Idcard)
            if exist_Idcard:
                return render(request, 'customer/input_cus_info.html', {'error': '客户已存在'})
            customer.objects.create(name=name, sex=sex, age=age, Idcard=Idcard, mobile=mobile, province=province, city=city,
                                address=address, note=note)
            response = {'success': '添加成功', 'name': name, 'age': age, 'sex': sex, 'Idcard': Idcard, 'mobile': mobile,
                    'province': province, 'city': city, 'address': address, 'note': note}
            obj = customer.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                customer.objects.filter(id=i.id).update(id=num)
            return render(request, 'customer/input_cus_info.html', response)
        elif request.POST.get('whichform') == '2':
            name = request.POST.get('name')
            Idcard = request.POST.get('Idcard')
            mobile = request.POST.get('mobile')
            # 都为空则全部查找
            if not name and not Idcard and not mobile:
                # 执行全部查找
                result = customer.objects.all()
                return render(request, 'customer/input_cus_info.html', {'result': result})
            # 根据某个条件查询
            if name:
                result = customer.objects.filter(name=name)
            elif Idcard:
                result = customer.objects.filter(Idcard=Idcard)
            elif mobile:
                result = customer.objects.filter(mobile=mobile)
            if not result:
                return render(request, 'customer/input_cus_info.html', {'error2': '查询失败'})
            return render(request, 'customer/input_cus_info.html', {'result': result})
        elif request.POST.get('whichform') == '3':
            if request.method == "POST":

                f = request.FILES['file']
                type_excel = f.name.split('.')[1]
                if 'xls' == type_excel:
                    # 开始解析上传的excel表格
                    wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
                    table = wb.sheets()[0]
                    nrows = table.nrows  # 行数
                    # ncole = table.ncols  # 列数
                    try:
                        with transaction.atomic():
                            for i in range(1, nrows):
                                rowValues = table.row_values(i)  # 一行的数据
                                customer.objects.create(name=rowValues[0], sex=rowValues[1], age=rowValues[2], Idcard=rowValues[3], mobile=rowValues[4], province=rowValues[5], city=rowValues[6],
                                address=rowValues[7], note=rowValues[8])
                    except Exception as e:
                        return render(request, 'customer/input_cus_info.html', {'error3': '上传成功'})
                    return render(request, 'customer/input_cus_info.html', {'success3': '上传成功'})
                return render(request, 'customer/input_cus_info.html', {'error3': '上传文件格式不是xls'})
            return render(request,'customer/input_cus_info.html',{'error3': '不是post请求'})
        elif request.POST.get('whichform') == '4':
            response = HttpResponse(content_type='application/ms-excel')
            # 设置文件名称
            response['Content-Disposition'] = 'attachment; filename="customer.xls"'
            # 创建工作簿
            wb = xlwt.Workbook(encoding='utf-8')
            # 创建表
            ws = wb.add_sheet('Menu')
            row_num = 0
            font_style = xlwt.XFStyle()
            # 二进制
            font_style.font.bold = True
            # 表头内容
            columns = ['ID', '姓名', '性别', '年龄','身份证号','联系方式','省','市','详细地址','备注']
            # 写进表头内容
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            # 获取数据库数据
            rows = customer.objects.values_list('id', 'name', 'sex', 'age','Idcard','mobile','province','city','address','note')
            # 遍历提取出来的内容
            for row in rows:
                row_num += 1
                # 逐行写入Excel
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            return response



# 查询客户信息
# def search_cus_info(request):
#     if request.method == 'GET':
#         username = request.session.get('username')
#         c_username = request.COOKIES.get('username')
#         if admin_user.objects.filter(username=username) and request.session.get('uid'):
#             return render(request, 'customer/search_cus_info.html')
#         c_uid = request.COOKIES.get('uid')
#         if admin_user.objects.filter(username=c_username) and c_uid:
#             request.session['username'] = c_username
#             request.session['uid'] = c_uid
#             return render(request, 'customer/search_cus_info.html')
#         return HttpResponseRedirect('/')
#     elif request.method == 'POST':
#         name = request.POST.get('name')
#         Idcard = request.POST.get('Idcard')
#         mobile = request.POST.get('mobile')
#         # 都为空则全部查找
#         if not name and not Idcard and not mobile:
#             # 执行全部查找
#             result = customer.objects.all()
#             return render(request, 'customer/search_cus_info.html', {'result': result})
#         # 根据某个条件查询
#         if name:
#             result = customer.objects.filter(name=name)
#         elif Idcard:
#             result = customer.objects.filter(Idcard=Idcard)
#         elif mobile:
#             result = customer.objects.filter(mobile=mobile)
#         if not result:
#             return render(request, 'customer/search_cus_info.html', {'error': '查询失败'})
#         return render(request, 'customer/search_cus_info.html', {'result': result})


# 更改客户信息
def alter_cus_info(request):
    if request.method == 'GET':
        all_id = customer.objects.all().values('id')
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'customer/alter_cus_info.html',{'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'customer/alter_cus_info.html',{'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        all_id = customer.objects.all().values('id')
        if request.POST.get('whichform') == '3':
            name = request.POST.get('name')
            Idcard = request.POST.get('Idcard')
            mobile = request.POST.get('mobile')
            # 都为空则全部查找
            if not name and not Idcard and not mobile:
                result = customer.objects.all()
                return render(request, 'customer/alter_cus_info.html', {'result': result,'all_id':all_id})
            # 根据某个条件查询
            if name:
                result = customer.objects.filter(name=name)
            elif Idcard:
                result = customer.objects.filter(Idcard=Idcard)
            elif mobile:
                result = customer.objects.filter(mobile=mobile)
            if not result:
                return render(request, 'customer/alter_cus_info.html', {'error3': '查询失败','all_id':all_id})
            return render(request, 'customer/alter_cus_info.html', {'result': result,'all_id':all_id})
        elif request.POST.get('whichform') == '1':
            id = request.POST.get('id')
            if id == 'kong':
                return render(request, 'customer/alter_cus_info.html', {'error': 'id不能为空','all_id':all_id})

            option = request.POST.get('option')
            alter = request.POST.get('alter')

            searchid = customer.objects.filter(id=id)
            if not searchid:
                return render(request, 'customer/alter_cus_info.html', {'error': '无效id','all_id':all_id})
            if not alter:
                return render(request, 'customer/alter_cus_info.html', {'error': '修改内容不能为空','all_id':all_id})
            if option == 'kong':
                return render(request, 'customer/alter_cus_info.html', {'error': '选项不能为空','all_id':all_id})
            if option == 'name':
                customer.objects.filter(id=id).update(name=alter)
            elif option == 'age':
                customer.objects.filter(id=id).update(age=alter)
            elif option == 'sex':
                customer.objects.filter(id=id).update(sex=alter)
            elif option == 'Idcard':
                customer.objects.filter(id=id).update(Idcard=alter)
            elif option == 'mobile':
                customer.objects.filter(id=id).update(mobile=alter)
            elif option == 'province':
                customer.objects.filter(id=id).update(province=alter)
            elif option == 'city':
                customer.objects.filter(id=id).update(city=alter)
            elif option == 'address':
                customer.objects.filter(id=id).update(address=alter)
            elif option == 'note':
                customer.objects.filter(id=id).update(note=alter)
            return render(request, 'customer/alter_cus_info.html', {'success': '修改成功','all_id':all_id})
        elif request.POST.get('whichform') == '2':
            id = request.POST.get('id')
            if id == 'kong':
                return render(request, 'customer/alter_cus_info.html', {'error2': 'id不能为空','all_id':all_id})
            searchid = customer.objects.filter(id=id)
            if not searchid:
                return render(request, 'customer/alter_cus_info.html', {'error2': '无效id','all_id':all_id})
            customer.objects.filter(id=id).delete()

            obj = customer.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                customer.objects.filter(id=i.id).update(id=num)
            id = request.POST.get('id')
            all_id = customer.objects.all().values('id')
            return render(request, 'customer/alter_cus_info.html', {'success2': '删除成功','all_id':all_id})


# 供货商信息
def suppier(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'suppier/sup.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'suppier/sup.html')
        return HttpResponseRedirect('/')


# 添加供货商信息
def input_sup_info(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'suppier/input_sup_info.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'suppier/input_sup_info.html')
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        if request.POST.get('whichform') == '1':
            suppier = request.POST.get('supplier')
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            type = request.POST.get('type')
            note = request.POST.get('note')
            if not suppier:
                return render(request, 'suppier/input_sup_info.html', {'error': '供货商不能为空'})
            exist_suppier = supplier.objects.filter(name=suppier)
            if exist_suppier:
                return render(request, 'suppier/input_sup_info.html', {'error': '供货商已存在'})
            supplier.objects.create(name=suppier, address=address, mobile=mobile, type=type, note=note)
            response = {'success': '添加成功', 'suppier': suppier, 'address': address, 'mobile': mobile, 'type': type,
                    'note': note}
            obj = supplier.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                supplier.objects.filter(id=i.id).update(id=num)
            return render(request, 'suppier/input_sup_info.html', response)
        elif request.POST.get('whichform') == '2':
            name = request.POST.get('name')
            if not name:
                result = supplier.objects.all()
                return render(request, 'suppier/input_sup_info.html', {'result': result})
            result = supplier.objects.filter(name=name)
            if not result:
                return render(request, 'suppier/input_sup_info.html', {'error': '查询失败'})
            return render(request, 'suppier/input_sup_info.html', {'result':result})
# 查询供货商信息
# def search_sup_info(request):
#     if request.method == 'GET':
#         username = request.session.get('username')
#         c_username = request.COOKIES.get('username')
#         if admin_user.objects.filter(username=username) and request.session.get('uid'):
#             return render(request, 'suppier/search_sup_info.html')
#         c_uid = request.COOKIES.get('uid')
#         if admin_user.objects.filter(username=c_username) and c_uid:
#             request.session['username'] = c_username
#             request.session['uid'] = c_uid
#             return render(request, 'suppier/search_sup_info.html')
#         return HttpResponseRedirect('/')
#     elif request.method == 'POST':
#         name = request.POST.get('name')
#         if not name:
#             result = supplier.objects.all()
#             return render(request, 'suppier/search_sup_info.html', {'result': result})
#         result = supplier.objects.filter(name=name)
#         if not result:
#             return render(request, 'suppier/search_sup_info.html', {'error': '查询失败'})
#         return render(request, 'suppier/search_sup_info.html', result)



# 修改供货商信息
def alter_sup_info(request):
    if request.method == 'GET':
        all_id = supplier.objects.all().values('id')
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'suppier/alter_sup_info.html',{'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'suppier/alter_sup_info.html',{'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        all_id = supplier.objects.all().values('id')

        if request.POST.get('whichform') == '1':
            id = request.POST.get('id')
            if not id:
                return render(request, 'suppier/alter_sup_info.html', {'error': 'id不能为空','all_id':all_id})

            option = request.POST.get('option')
            alter = request.POST.get('alter')

            searchid = supplier.objects.filter(id=id)
            if not searchid:
                return render(request, 'suppier/alter_sup_info.html', {'error': '无效id','all_id':all_id})
            if not alter:
                return render(request, 'suppier/alter_sup_info.html', {'error': '修改内容不能为空','all_id':all_id})
            if option == 'kong':
                return render(request, 'suppier/alter_sup_info.html', {'error': '选项不能为空','all_id':all_id})
            if option == 'name':
                supplier.objects.filter(id=id).update(name=alter)
            elif option == 'address':
                supplier.objects.filter(id=id).update(address=alter)
            elif option == 'mobile':
                supplier.objects.filter(id=id).update(mobile=alter)
            elif option == 'type':
                supplier.objects.filter(id=id).update(type=alter)
            elif option == 'note':
                supplier.objects.filter(id=id).update(note=alter)
            return render(request, 'suppier/alter_sup_info.html', {'success': '修改成功','all_id':all_id})
        elif request.POST.get('whichform') == '2':
            id = request.POST.get('id')
            if not id:
                return render(request, 'suppier/alter_sup_info.html', {'error2': 'id不能为空', 'all_id': all_id})
            searchid = supplier.objects.filter(id=id)
            if not searchid:
                return render(request, 'suppier/alter_sup_info.html', {'error2': '无效id', 'all_id': all_id})
            supplier.objects.filter(id=id).delete()

            obj = supplier.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                supplier.objects.filter(id=i.id).update(id=num)
            all_id = supplier.objects.all().values('id')
            return render(request, 'suppier/alter_sup_info.html', {'success2': '删除成功', 'all_id': all_id})
        elif request.POST.get('whichform') == '3':
            name = request.POST.get('name')
            # 为空则全部查找
            if not name:
                result = supplier.objects.all()
                return render(request, 'suppier/alter_sup_info.html', {'result': result, 'all_id': all_id})
            result = supplier.objects.filter(name=name)
            if not result:
                return render(request, 'suppier/alter_sup_info.html', {'error3': '查询失败', 'all_id': all_id})
            return render(request, 'suppier/alter_sup_info.html', {'result': result, 'all_id': all_id})

# 经销商信息
def Agent(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'agent/age.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'agent/age.html')
        return HttpResponseRedirect('/')


# 添加经销商信息
def input_age_info(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'agent/input_age_info.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'agent/input_age_info.html')
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        if request.POST.get('whichform') == '1':
            Agent = request.POST.get('agent')
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            type = request.POST.get('type')
            note = request.POST.get('note')
            if not Agent:
                render(request, 'agent/input_age_info.html', {'error': '经销商不能为空'})
            exist_agent = agent.objects.filter(name=Agent)
            if exist_agent:
                return render(request, 'agent/input_age_info.html', {'error': '供货商已存在'})
            agent.objects.create(name=Agent, address=address, mobile=mobile, type=type, note=note)
            response = {'success': '添加成功', 'agent': Agent, 'address': address, 'mobile': mobile, 'type': type, 'note': note}
            obj = agent.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                agent.objects.filter(id=i.id).update(id=num)
            return render(request, 'agent/input_age_info.html', response)
        elif request.POST.get('whichform') == '2':
            name = request.POST.get('name')
            if not name:
                result = agent.objects.all()
                return render(request, 'agent/input_age_info.html', {'result': result})
            result = agent.objects.filter(name=name)
            if not result:
                return render(request, 'agent/search_age_info.html', {'error2': '查询失败'})
            return render(request, 'agent/input_age_info.html', {'result': result})

# 查询经销商信息
# def search_age_info(request):
#     if request.method == 'GET':
#         # 验证？
#         username = request.session.get('username')
#         c_username = request.COOKIES.get('username')
#         if admin_user.objects.filter(username=username) and request.session.get('uid'):
#             return render(request, 'agent/search_age_info.html')
#         c_uid = request.COOKIES.get('uid')
#         if admin_user.objects.filter(username=c_username) and c_uid:
#             request.session['username'] = c_username
#             request.session['uid'] = c_uid
#             return render(request, 'agent/search_age_info.html')
#         return HttpResponseRedirect('/')
#     elif request.method == 'POST':
#         name = request.POST.get('name')
#         if not name:
#             result = agent.objects.all()
#             return render(request, 'agent/search_age_info.html', {'result': result})
#         result = agent.objects.filter(name=name)
#         if not result:
#             return render(request, 'agent/search_age_info.html', {'error': '查询失败'})
#         return render(request, 'agent/search_age_info.html', {'result': result})


# 修改经销商信息
def alter_age_info(request):
    if request.method == 'GET':
        all_id = agent.objects.all().values('id')
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'agent/alter_age_info.html',{'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'agent/alter_age_info.html',{'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        all_id = agent.objects.all().values('id')
        if request.POST.get('whichform') == '1':
            id = request.POST.get('id')
            if not id:
                return render(request, 'agent/alter_age_info.html', {'error': 'id不能为空','all_id':all_id})

            option = request.POST.get('option')
            alter = request.POST.get('alter')

            searchid = agent.objects.filter(id=id)
            if not searchid:
                return render(request, 'agent/alter_age_info.html', {'error': '无效id','all_id':all_id})
            if not alter:
                return render(request, 'agent/alter_age_info.html', {'error': '修改内容不能为空','all_id':all_id})
            if option == 'kong':
                return render(request, 'agent/alter_age_info.html', {'error': '选项不能为空','all_id':all_id})
            if option == 'name':
                agent.objects.filter(id=id).update(name=alter)
            elif option == 'address':
                agent.objects.filter(id=id).update(address=alter)
            elif option == 'mobile':
                agent.objects.filter(id=id).update(mobile=alter)
            elif option == 'type':
                agent.objects.filter(id=id).update(type=alter)
            elif option == 'note':
                agent.objects.filter(id=id).update(note=alter)
            return render(request, 'agent/alter_age_info.html', {'success': '修改成功','all_id':all_id})
        elif request.POST.get('whichform') == '2':
            id = request.POST.get('id')
            if not id:
                return render(request, 'agent/alter_age_info.html', {'error2': 'id不能为空', 'all_id': all_id})
            searchid = agent.objects.filter(id=id)
            if not searchid:
                return render(request, 'agent/alter_age_info.html', {'error2': '无效id', 'all_id': all_id})
            agent.objects.filter(id=id).delete()

            obj = agent.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                agent.objects.filter(id=i.id).update(id=num)
            all_id = agent.objects.all().values('id')
            return render(request, 'agent/alter_age_info.html', {'success2': '删除成功', 'all_id': all_id})
        elif request.POST.get('whichform') == '3':
            name = request.POST.get('name')
            # 为空则全部查找
            if not name:
                result = agent.objects.all()
                return render(request, 'agent/alter_age_info.html', {'result': result,'all_id':all_id})
            result = agent.objects.filter(name=name)
            if not result:
                return render(request, 'agent/alter_age_info.html', {'error3': '查询失败','all_id':all_id})
            return render(request, 'agent/alter_age_info.html', {'result': result,'all_id':all_id})



# 库存模块
def invent(request):
    if request.method == 'GET':
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'inventory/invent.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'inventory/invent.html')
        return HttpResponseRedirect('/')


# 库存情况
def storage_info(request):
    if request.method == 'GET':
        # 验证身份
        type = Type.objects.all()
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'inventory/storage_info.html', {'type': type})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'inventory/storage_info.html', {'type': type})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        alltype = Type.objects.all()
        type = request.POST.get('type')
        if type == 'kong':
            result = inventory.objects.all()
            return render(request, 'inventory/storage_info.html',
                          {'error': '型号不能为空', 'type': alltype, 'result': result})
        result = inventory.objects.filter(model=type)
        obj = inventory.objects.all()
        num = 0
        for i in obj:
            num = num + 1
            inventory.objects.filter(id=i.id).update(id=num)
        return render(request, 'inventory/storage_info.html', {'result': result, 'type': alltype})





# 型号信息
def type_info(request):
    if request.method == 'GET':
        all_id = Type.objects.all().values('id')
        # 身份验证
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'inventory/model_info.html',{'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'inventory/model_info.html',{'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        all_id = Type.objects.all().values('id')
        if request.POST.get('whichform') == '1':
            type = request.POST.get('type')
            note = request.POST.get('note')
            if not type:
                return render(request, 'inventory/model_info.html', {'error1': '型号不能为空','all_id':all_id})
            if Type.objects.filter(type=type):
                return render(request, 'inventory/model_info.html', {'error1': '型号已经存在','all_id':all_id})

            # 一旦创建该型号，则在库存中也创建
            inventory.objects.create(model=type, storage=0)

            Type.objects.create(type=type, note=note)
            obj = Type.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                Type.objects.filter(id=i.id).update(id=num)
            return render(request, 'inventory/model_info.html', {'success1': '录入成功','all_id':all_id})
        elif request.POST.get('whichform') == '2':
            result = Type.objects.all()
            return render(request, 'inventory/model_info.html', {'result': result,'all_id':all_id})
        elif request.POST.get('whichform') == '3':
            id =request.POST.get('id')
            if id == 'kong':
                return render(request,'inventory/model_info.html',{'error3':'id不能为空','all_id':all_id})
            Type.objects.filter(id=id).delete()
            #同时在库存中删除该型号
            # type = Type.objects.filter(id=id).values('model')
            # inventory.objects.filter(model=type).delete()

            obj = Type.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                Type.objects.filter(id=i.id).update(id=num)
            all_id = Type.objects.all().values('id')
            return render(request,'inventory/model_info.html',{'success3':'删除成功','all_id':all_id})

# 供货信息
def supply_info(request):
    if request.method == 'GET':
        all_id = supply.objects.all().values('id')
        TYPE = Type.objects.all()
        SUPPLIER = supplier.objects.all()

        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'inventory/supply_info.html', {'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'inventory/supply_info.html', {'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        all_id = supply.objects.all().values('id')
        TYPE = Type.objects.all()
        SUPPLIER = supplier.objects.all()
        if request.POST.get('whichform') == '1':
            ordernumber = request.POST.get('ordernumber')
            suppier = request.POST.get('suppier')
            supply_time = request.POST.get('supply_time')
            type = request.POST.get('type')
            number = request.POST.get('number')
            price = request.POST.get('price')
            totalprice = request.POST.get('totalprice')
            note = request.POST.get('note')
            if not number:
                return render(request, 'inventory/supply_info.html',
                              {'error': '供货数量不能为空', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
            if not ordernumber:
                return render(request, 'inventory/supply_info.html',
                              {'error': '订单编号不能为空', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
            if not type:
                return render(request, 'inventory/supply_info.html',
                              {'error': '订单类型不能为空', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
            if supply.objects.filter(ordernumber=ordernumber):
                return render(request, 'inventory/supply_info.html',
                              {'error': '该订单已存在', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
            supply.objects.create(ordernumber=ordernumber, supplier=suppier, supply_time=supply_time, type=type,
                                  number=number, price=price, totalprice=totalprice, note=note)

            inventory.objects.filter(model=type).update(storage=F('storage') + int(number))
            result = supply.objects.filter(ordernumber=ordernumber)
            obj = supply.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                supply.objects.filter(id=i.id).update(id=num)
            return render(request, 'inventory/supply_info.html',
                          {'result': result, 'success': '录入成功', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
        elif request.POST.get('whichform') == '2':
            result = supply.objects.all()
            return render(request, 'inventory/supply_info.html',
                          {'result': result, 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
        elif request.POST.get('whichform') == '3':
            id = request.POST.get('id')
            if not id:
                return render(request, 'inventory/supply_info.html',
                              {'error3': 'id不能为空', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
            if not supply.objects.filter(id=id):
                return render(request, 'inventory/supply_info.html',
                              {'error3': 'id不存在', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})

            # 获取要删除的对象，在库存表中删除该对象对应的数量
            delete = supply.objects.get(id=id)
            inventory.objects.filter(model=delete.type).update(storage=F('storage') - int(delete.number))

            supply.objects.filter(id=id).delete()

            obj = supply.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                supply.objects.filter(id=i.id).update(id=num)
            all_id = supply.objects.all().values('id')
            return render(request, 'inventory/supply_info.html',
                          {'success3': '删除成功，您的删除会导致库存的变化', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})

# 更改供货信息
# def alter_supply_info(request):
#     if request.method == 'GET':
#         all_id = supply.objects.all().values('id')
#
#         TYPE = Type.objects.all()
#         SUPPLIER = supplier.objects.all()
#
#         username = request.session.get('username')
#         c_username = request.COOKIES.get('username')
#         if admin_user.objects.filter(username=username) and request.session.get('uid'):
#             return render(request, 'inventory/alter_supply_info.html', {'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
#         c_uid = request.COOKIES.get('uid')
#         if admin_user.objects.filter(username=c_username) and c_uid:
#             request.session['username'] = c_username
#             request.session['uid'] = c_uid
#             return render(request, 'inventory/alter_supply_info.html', {'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
#         return HttpResponseRedirect('/')
#     elif request.method == 'POST':
#         all_id = supply.objects.all().values('id')
#         TYPE = Type.objects.all()
#         SUPPLIER = supplier.objects.all()
#         # 查询
#         if request.POST.get('whichform') == '2':
#             result = supply.objects.all()
#             return render(request, 'inventory/alter_supply_info.html',
#                           {'result': result, 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
#         # 修改
#         # elif request.POST.get('whichform') == '3':
#         #     id = request.POST.get('id')
#         #     if not id:
#         #         return render(request, 'inventory/alter_supply_info.html', {'error3': 'id不能为空','type':TYPE,'suppier':SUPPLIER})
#         #     option = request.POST.get('option')
#         #     alter = request.POST.get('alter')
#         #     suppier = request.POST.get('suppier')
#         #     type = request.POST.get('type')
#         #     supply_time = request.POST.get('supply_time')
#         #     if option=='kong':
#         #         return render(request,'inventory/alter_supply_info.html',{'error3':'选项不能为空','type':TYPE,'suppier':SUPPLIER})
#         #     if not alter and suppier=='kong' and type=='kong' and supply_time=='':
#         #         return render(request,'inventory/alter_supply_info.html',{'error3':'修改内容不能为空','type':TYPE,'suppier':SUPPLIER})
#         #     if option == 'ordernumber':
#         #         supply.objects.filter(id=id).update(ordernumber=alter)
#         #     elif option == 'suppier':
#         #         supply.objects.filter(id=id).update(supplier=suppier)
#         #     elif option == 'supply_time':
#         #         supply.objects.filter(id=id).update(supply_time=supply_time)
#         #     elif option == 'type':
#         #         supply.objects.filter(id=id).update(type=type)
#         #     elif option == 'number':
#         #
#         #         #首先对库存表进行更改，在对供货表更改
#         #         change = supply.objects.get(id=id)
#         #         storage = inventory.objects.get(model=change.type)
#         #         inventory.objects.filter(model=change.type).update(storage=int(storage.storage) - int(change.number) + int(alter))
#         #
#         #         supply.objects.filter(id=id).update(number=alter)
#         #     elif option == 'price':
#         #         supply.objects.filter(id=id).update(price=alter)
#         #     elif option == 'totalprice':
#         #         supply.objects.filter(id=id).update(totalprice=alter)
#         #     elif option == 'note':
#         #         supply.objects.filter(id=id).update(note=alter)
#         #     return render(request,'inventory/alter_supply_info.html',{'success3':'修改成功,您对数量的修改会导致库存的变化','type':TYPE,'suppier':SUPPLIER})
#         # 删除
#         elif request.POST.get('whichform') == '4':
#             id = request.POST.get('id')
#             if not id:
#                 return render(request, 'inventory/alter_supply_info.html',
#                               {'error4': 'id不能为空', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
#             if not supply.objects.filter(id=id):
#                 return render(request, 'inventory/alter_supply_info.html',
#                               {'error4': 'id不存在', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
#
#             # 获取要删除的对象，在库存表中删除该对象对应的数量
#             delete = supply.objects.get(id=id)
#             inventory.objects.filter(model=delete.type).update(storage=F('storage') - int(delete.number))
#
#             supply.objects.filter(id=id).delete()
#
#             obj = supply.objects.all()
#             num = 0
#             for i in obj:
#                 num = num + 1
#                 supply.objects.filter(id=i.id).update(id=num)
#             all_id = supply.objects.all().values('id')
#             return render(request, 'inventory/alter_supply_info.html',
#                           {'success4': '删除成功，您的删除会导致库存的变化', 'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})
#         return render(request, 'inventory/alter_supply_info.html', {'type': TYPE, 'suppier': SUPPLIER,'all_id':all_id})


# 销售管理
def sell(request):
    if request.method == 'GET':
        all_id = Sell.objects.all().values('id')
        all_type=Type.objects.all()

        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'sell/sell.html',{'all_type':all_type,'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'sell/sell.html',{'all_type':all_type,'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        all_id = Sell.objects.all().values('id')
        all_type = Type.objects.all()
        if request.POST.get('whichform') == '2':
            all_sale = Sell.objects.all()
            return render(request,'sell/sell.html',{'all_sale':all_sale,'all_type':all_type,'all_id':all_id})
        elif request.POST.get('whichform') == '1':
            name = request.POST.get('name')
            type = request.POST.get('type')
            number = request.POST.get('number')
            price = request.POST.get('price')
            payamount = request.POST.get('payamount')
            paymethods = request.POST.get('paymethods')
            arrearamount = request.POST.get('arrearamount')
            date = request.POST.get('date')
            note = request.POST.get('note')
            if not name:
                return render(request,'sell/sell.html',{'error':'姓名不能为空','all_type':all_type,'all_id':all_id})
            if type == 'kong':
                return render(request,'sell/sell.html',{'error':'类型不能为空','all_type':all_type,'all_id':all_id})
            Sell.objects.create(name=name,model=type,tradingamount=number,price=price,payamount=payamount,paymethods=paymethods,arrearamount=arrearamount,date=date,note=note)

            inventory.objects.filter(model=type).update(storage=F('storage') - int(number))

            obj = Sell.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                Sell.objects.filter(id=i.id).update(id=num)
            return render(request,'sell/sell.html',{'success':'添加成功','all_type':all_type,'all_id':all_id})
        elif request.POST.get('whichform') == '3':
            id = request.POST.get('id')

            delete = Sell.objects.get(id=id)
            inventory.objects.filter(model=delete.model).update(storage=F('storage') + int(delete.tradingamount))

            Sell.objects.filter(id=id).delete()

            obj = Sell.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                Sell.objects.filter(id=i.id).update(id=num)
            all_id = Sell.objects.all().values('id')
            return render(request,'sell/sell.html',{'success2':'删除成功','all_type':all_type,'all_id':all_id})

# 产品展示管理
def product(request):
    if request.method == 'GET':
        models = Type.objects.all()
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'productinfo/product.html')
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'productinfo/product.html')
        return HttpResponseRedirect('/')


# 添加产品信息
def add_alter_product(request):
    if request.method == 'GET':
        models = Type.objects.all()
        all_id = Productinfo.objects.all().values('id')
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'productinfo/inputalter_product.html', {'models': models,'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'productinfo/inputalter_product.html', {'models': models,'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        models = Type.objects.all()
        all_id = Productinfo.objects.all().values('id')
        if request.POST.get('whichform') == '1':
            model = request.POST.get('model')
            info = request.POST.get('info')
            picture = request.FILES['picture']
            release = request.POST.get('release')
            if model == "kong":
                return render(request, 'productinfo/inputalter_product.html', {'error': '型号不能为空', 'models': models,'all_id':all_id})
            if release == 'kong':
                return render(request, 'productinfo/inputalter_product.html', {'error': '发布选择不能为空', 'models': models,'all_id':all_id})
            Productinfo.objects.create(model=model, information=info, picture=picture, release=release)
            obj = Productinfo.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                Productinfo.objects.filter(id=i.id).update(id=num)
            return render(request, 'productinfo/inputalter_product.html', {'success': '添加成功', 'models': models,'all_id':all_id})
        elif request.POST.get('whichform') == '2':
            all_info = Productinfo.objects.all()
            return render(request, 'productinfo/inputalter_product.html',{'all_info': all_info,'all_id':all_id,'models': models})
        elif request.POST.get('whichform') == '3':
            id = request.POST.get('id')
            option = request.POST.get('option')
            if option == 'kong':
                return render(request, 'productinfo/inputalter_product.html', {'error3': '修改选项不能为空','all_id':all_id,'models': models})
            if option == 'info':
                info = request.POST.get('info')
                Productinfo.objects.filter(id=id).update(information=info)
            elif option == 'picture':
                picture = request.FILES['picture']
                model = Productinfo.objects.filter(id=id).values('model')
                info = Productinfo.objects.filter(id=id).values('information')
                release  = Productinfo.objects.filter(id=id).values('release')
                Productinfo.objects.create(model=model,information=info,picture=picture,release=release)
                Productinfo.objects.filter(id=id).delete()

                obj = Productinfo.objects.all()
                num = 0
                for i in obj:
                    num = num + 1
                    Productinfo.objects.filter(id=i.id).update(id=num)
            return render(request, 'productinfo/inputalter_product.html', {'success3': '修改成功','all_id':all_id,'models': models})
        elif request.POST.get('whichform') == '4':
            id= request.POST.get('id')
            if id == 'kong':
                return render(request,'productinfo/inputalter_product.html',{'error4':'删除的id不能为空','all_id':all_id,'models': models})
            Productinfo.objects.filter(id=id).delete()
            all_id = Productinfo.objects.all().values('id')
            obj = Productinfo.objects.all()
            num = 0
            for i in obj:
                num = num + 1
                Productinfo.objects.filter(id=i.id).update(id=num)
            return render(request,'productinfo/inputalter_product.html',{'success4':'删除成功','all_id':all_id,'models': models})


# 修改产品信息
# def alter_productinfo(request):
#     if request.method == 'GET':
#         all_id = Productinfo.objects.all().values('id')
#         username = request.session.get('username')
#         c_username = request.COOKIES.get('username')
#         if admin_user.objects.filter(username=username) and request.session.get('uid'):
#             return render(request, 'productinfo/alter_productinfo.html')
#         c_uid = request.COOKIES.get('uid')
#         if admin_user.objects.filter(username=c_username) and c_uid:
#             request.session['username'] = c_username
#             request.session['uid'] = c_uid
#             return render(request, 'productinfo/alter_productinfo.html',{'all_id':all_id})
#         return HttpResponseRedirect('/')
#     elif request.method == 'POST':
#         all_id = Productinfo.objects.all().values('id')
#         if request.POST.get('whichform') == '2':
#             all_info = Productinfo.objects.all()
#             return render(request, 'productinfo/alter_productinfo.html',{'all_info': all_info,'all_id':all_id})
#         elif request.POST.get('whichform') == '1':
#             id = request.POST.get('id')
#             option = request.POST.get('option')
#             if option == 'kong':
#                 return render(request, 'productinfo/alter_productinfo.html', {'error': '修改选项不能为空','all_id':all_id})
#             if option == 'info':
#                 info = request.POST.get('info')
#                 Productinfo.objects.filter(id=id).update(information=info)
#             elif option == 'picture':
#                 picture = request.FILES['picture']
#                 model = Productinfo.objects.filter(id=id).values('model')
#                 info = Productinfo.objects.filter(id=id).values('information')
#                 release  = Productinfo.objects.filter(id=id).values('release')
#                 Productinfo.objects.create(model=model,information=info,picture=picture,release=release)
#                 Productinfo.objects.filter(id=id).delete()
#
#                 obj = Productinfo.objects.all()
#                 num = 0
#                 for i in obj:
#                     num = num + 1
#                     Productinfo.objects.filter(id=i.id).update(id=num)
#             return render(request, 'productinfo/alter_productinfo.html', {'success': '修改成功','all_id':all_id})
#         elif request.POST.get('whichform') == '3':
#             id= request.POST.get('id')
#             if id == 'kong':
#                 return render(request,'productinfo/alter_productinfo.html',{'error2':'删除的id不能为空','all_id':all_id})
#             Productinfo.objects.filter(id=id).delete()
#             all_id = Productinfo.objects.all().values('id')
#             return render(request,'productinfo/alter_productinfo.html',{'success2':'删除成功','all_id':all_id})

#发布产品的信息
def search_release(request):
    if request.method == 'GET':
        all_id = Productinfo.objects.all().values('id')
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'productinfo/release_product.html', {'all_id':all_id})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'productinfo/release_product.html', {'all_id':all_id})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        if request.POST.get('whichform') == '1':
            all_id = Productinfo.objects.all().values('id')
            all_info = Productinfo.objects.all()
            return render(request, 'productinfo/release_product.html', {'all_id':all_id, 'all_info':all_info})
        elif request.POST.get('whichform') == '2':
            id = request.POST.get('ID')
            if id == 'kong':
                all_id = Productinfo.objects.all().values('id')
                all_info = Productinfo.objects.all()
                return render(request, 'productinfo/release_product.html',
                              {'all_id': all_id, 'all_info': all_info, 'error2':'id不能为空'})
            # if Productinfo.objects.filter(id=id).values('release') == '是':
            #     all_id = Productinfo.objects.all().values('id')
            #     all_info = Productinfo.objects.all()
            #     return render(request, 'productinfo/release_product.html',
            #               {'all_id': all_id, 'all_info': all_info, 'error': '该信息已发布'})
            Productinfo.objects.filter(id=id).update(release='是')
            all_id = Productinfo.objects.all().values('id')
            all_info = Productinfo.objects.all()
            return render(request, 'productinfo/release_product.html', {'all_id': all_id, 'all_info': all_info, 'success2': '发布成功'})
        elif request.POST.get('whichform') == '3':
            id = request.POST.get('ID')
            if id == 'kong':
                all_id = Productinfo.objects.all().values('id')
                all_info = Productinfo.objects.all()
                return render(request, 'productinfo/release_product.html',
                              {'all_id': all_id, 'all_info': all_info, 'error3':'id不能为空'})
            # if Productinfo.objects.filter(id=id).values('release') == '否':
            #     all_id = Productinfo.objects.all().values('id')
            #     all_info = Productinfo.objects.all()
            #     return render(request, 'productinfo/release_product.html',
            #               {'all_id': all_id, 'all_info': all_info, 'error2': '该信息未发布'})
            Productinfo.objects.filter(id=id).update(release='否')
            all_id = Productinfo.objects.all().values('id')
            all_info = Productinfo.objects.all()
            return render(request, 'productinfo/release_product.html', {'all_id': all_id, 'all_info': all_info, 'success3': '撤销成功'})

def booking(request):
    if request.method == 'GET':
        result = Booking.objects.all()
        all_id = Booking.objects.all().values('id')
        username = request.session.get('username')
        c_username = request.COOKIES.get('username')
        if admin_user.objects.filter(username=username) and request.session.get('uid'):
            return render(request, 'booking/booking_info.html', {'all_id': all_id,'result':result})
        c_uid = request.COOKIES.get('uid')
        if admin_user.objects.filter(username=c_username) and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return render(request, 'booking/booking_info.html', {'all_id': all_id,'result':result})
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        all_id = Booking.objects.all().values('id')
        result = Booking.objects.all()
        id = request.POST.get('id')
        if id == 'kong':
            return render(request,'booking/booking_info.html',{'all_id':all_id,'result':result,'error':'删除id不能为空'})
        Booking.objects.filter(id=id).delete()
        obj = Booking.objects.all()
        num = 0
        for i in obj:
            num = num + 1
            Booking.objects.filter(id=i.id).update(id=num)
        all_id = Booking.objects.all().values('id')
        return render(request, 'booking/booking_info.html', {'all_id': all_id, 'result': result, 'success': '删除成功'})

def logout(requset):
    auth.logout(requset)
    return HttpResponseRedirect('/')
