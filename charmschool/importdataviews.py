from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
import tablib
from import_export import resources
from .models import Student
from django.contrib.auth.models import Group
from .forms import AddGroupDataForm
from .mixins import SuperuserRequiredMixin
from io import TextIOWrapper
from django.shortcuts import redirect
from django.contrib import messages
import copy

def import_data(dataset, group_pk = 0 ,check=False):
    event_resource = resources.modelresource_factory(model=Student)()
    if check == True:
        confilctset = []
        for el in dataset:
            db = Student.objects.filter(student_id = el[0])
            if len(db) != 0:
                confilctset.append(r'<li>{}</li>'.format(" ".join(el)))
        return confilctset
    dataset.append_col(
        col=tuple(f'{el[0]}@kmitl.ac.th' for el in dataset),
        header='email_ref'
    )
    dataset.append_col(
        col=tuple(group_pk for _ in dataset),
        header='group_ref'
    )
    result = event_resource.import_data(dataset, dry_run=True)  # Test the data import
    if not result.has_errors():
        event_resource.import_data(dataset, dry_run=False) 
        return True
    return False

class AddGroupView(SuperuserRequiredMixin, View):
    def post(self,request,*args, **kwargs):   
        form = AddGroupDataForm(request.POST)
        if form.is_valid:
            file = TextIOWrapper(request.FILES['datacsv'].file, encoding='utf-8-sig', errors='replace')
            dataset = tablib.Dataset(
                headers=['student_id', 'gender', 'name', 'surname']
                ).load(file.read(), format='csv')
            conflictset = import_data(dataset, check=True)
            if conflictset:
                messages.error(request, 
                    r'<b>พบข้อผิดพลาด:</b> ข้อมูลที่พยายามนำเข้าต่อไปนี้ <ul>{}</ul> ซ้ำกับข้อมูลนักศึกษาที่มีอยู่แล้ว'.format(''.join(conflictset))
                )
                return redirect('dashboard')
            group = Group(name = request.POST['name'])
            group.save()
            gd = form.save(commit=False)
            request.user.groups.add(group)
            gd.group = group
            gd.save()
            status = import_data(dataset,group.pk)
            if status:
                messages.success(request, r'<b>สำเร็จ:</b> สร้างกลุ่มเรียน และบันทึกข้อมูลนักศึกษาเรียบร้อย')
            else:   
                messages.error(request, 
                    r'<b>พบข้อผิดพลาด:</b> สร้างกลุ่มเรียนสำเร็จ แต่ไม่สามารถบันทึกข้อมูลนักศึกษา โปรดตรวจสอบไฟล์ .csv ของท่าน หรือติดต่อผู้ดูแลระบบ'
                )
        else:
            messages.error(request, 
                    r'<b>พบข้อผิดพลาด:</b> ไม่สามารถประมวลผลข้อมูลได้ โปรดตรวจสอบข้อมูลของท่าน'
                )
        return redirect('dashboard')
    
    
