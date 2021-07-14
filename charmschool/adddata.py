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

def import_data(request, group_pk, clear_old_data = False):
    event_resource = resources.modelresource_factory(model=Student)()
    file = TextIOWrapper(request.FILES['datacsv'].file, encoding='utf-8-sig', errors='replace')
    dataset = tablib.Dataset(
        headers=['student_id', 'gender', 'name', 'surname']
    ).load(file.read(), format='csv')
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
        if clear_old_data:
            Student.objects.filter(group_ref = group_pk).delete()
        event_resource.import_data(dataset, dry_run=False) 
        return True
    return False

class AddGroupView(SuperuserRequiredMixin, View):
    def post(self,request,*args, **kwargs):   
        form = AddGroupDataForm(request.POST)
        if form.is_valid:
            group = Group(name = request.POST['name'])
            group.save()
            gd = form.save(commit=False)
            request.user.groups.add(group)
            gd.group = group
            gd.save()
            status = import_data(request, group.pk)
            if status:
                messages.success(request, r'<b>สำเร็จ:</b> สร้างกลุ่มเรียน และบันทึกข้อมูลนักศึกษาเรียบร้อย')
            else:   
                messages.error(request, 
                    r'<b>พบข้อผิดพลาด:</b> สร้างกลุ่มเรียนสำเร็จ แต่ไม่สามารถบันทึกข้อมูลนักศึกษา โปรดตรวจสอบไฟล์ .csv ของท่าน หรือติดต่อผู้ดูแลระบบ'
                )
        return redirect('dashboard')
    
    
