from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import StudentRecord
from users.models import User
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# 判断是否为管理员

def is_admin(user):
    return user.is_authenticated and user.role == 1

# 数据列表（管理员可见）
@user_passes_test(is_admin)
def record_list(request):
    records = StudentRecord.objects.all()
    return render(request, 'data_manage/record_list.html', {'records': records})

# 数据导入（CSV/Excel，管理员可见）
@user_passes_test(is_admin)
def import_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        ext = os.path.splitext(file.name)[1]
        if ext in ['.csv', '.xlsx']:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            if ext == '.csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                StudentRecord.objects.create(
                    user=User.objects.get(username=row['username']),
                    study_hours=row['study_hours'],
                    homework_done=row['homework_done'],
                    interaction_count=row['interaction_count'],
                    test_score=row['test_score'],
                    date=row['date']
                )
            messages.success(request, '数据导入成功！')
            os.remove(file_path)
        else:
            messages.error(request, '仅支持CSV或Excel文件')
        return redirect('record_list')
    return render(request, 'data_manage/import_data.html')

# 数据导出（CSV，管理员可见）
@user_passes_test(is_admin)
def export_data(request):
    records = StudentRecord.objects.all().values()
    df = pd.DataFrame(records)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_records.csv"'
    df.to_csv(path_or_buf=response, index=False)
    return response
