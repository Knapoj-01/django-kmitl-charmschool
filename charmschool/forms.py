from django import forms
from django.forms import widgets
from .models import *
import json
defaultattr = {'class':'form-control'}
class AddGroupDataForm(forms.ModelForm):
    class Meta:
        model = GroupData
        fields = '__all__'
        exclude = ['group']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class':'form-control'}),
            'start_time': forms.TimeInput(attrs={'type':'time','class':'form-control'}),
            'end_time': forms.TimeInput(attrs={'type':'time','class':'form-control'}),
            'study_on' : forms.Select(attrs={'class':'form-select'}),
            'place' : forms.TextInput(attrs=defaultattr) 
        }
    name = forms.CharField(max_length=100, label='ชื่อกลุ่มเรียน', widget=forms.TextInput(attrs = defaultattr))
    field_order = ['name','description', 'study_on', 'start_time', 'end_time']

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Course_Comment
        fields=['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class':'form-control'}),
        }
        labels = {
            'content': 'ความคิดเห็น'
        }
    def save(self, request, content_pk):
        model =  super().save(commit=False)
        model.author = request.user
        model.subject = Course_Content.objects.get(pk=content_pk)
        model.save()
        return model

class AddClassWorkForm(forms.ModelForm):
    class Meta:
        model = Classwork
        fields = ['message','works']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class':'form-control'}),
            'works': forms.ClearableFileInput(attrs={'accept':'.pdf,.jpg,.jpeg','multiple': True})
        }
        labels= {
            'message': 'ข้อความ',
            'works': 'ไฟล์งานที่จะส่ง'
        }
    def save(self, request, assignment_pk, classwork_id_list = None):
        model =  super().save(commit=False)
        model.student = request.user.student
        model.assignment = Assignment.objects.get(pk=assignment_pk)
        if classwork_id_list: model.works = json.dumps(classwork_id_list)
        model.save()
        return model

class AddAssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_groups = kwargs.pop('user_groups_queryset')
        super().__init__(*args, **kwargs)
        self.fields['visible_by'].queryset = user_groups
    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ['author','pub_date']
        widgets = {
            'subject': forms.TextInput(attrs=defaultattr),
            'content': forms.Textarea(attrs={'rows': 10, 'class':'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'type':"datetime-local", 'class':'form-control'}),
            'max_score':forms.NumberInput(attrs={'rows': 3, 'class':'form-control', 'min':0}),
        }
        labels = {
            'subject': 'หัวข้อการบ้าน',
            'due_date': 'กำหนดส่ง',
            'content': 'เนื้อหาการบ้าน',
            'max_score': 'คะแนนเต็ม',
        }
    field_order = ['subject','due_date', 'visible_by', 'content', 'max_score']
    visible_by = forms.ModelMultipleChoiceField(
        queryset= None,
        widget=forms.CheckboxSelectMultiple,
        label = 'กลุ่มที่เข้าถึงได้'
    )

class AddContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_groups = kwargs.pop('user_groups_queryset')
        super().__init__(*args, **kwargs)
        self.fields['visible_by'].queryset = user_groups
        
    class Meta:
        model = Course_Content
        fields = '__all__'
        exclude = ['author','pub_date']
        widgets = {
            'subject': forms.TextInput(attrs=defaultattr),
            'content': forms.Textarea(attrs={'rows': 10, 'class':'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class':'form-control'}),
            'private' : forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'subject': 'หัวข้อเนื้อหา',
            'description': 'คำอธิบายเนื้อหา',
            'content': 'เนื้อหา',
            'private' : 'จำกัดสิทธิ์การเข้าถึง (เห็นได้เฉพาะผู้สอน)'
        }
    field_order = ['subject','description', 'visible_by', 'content', 'max_score']
    visible_by = forms.ModelMultipleChoiceField(
        queryset= None,
        widget=forms.CheckboxSelectMultiple,
        label = 'กลุ่มที่เข้าถึงได้'
    )
