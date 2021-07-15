from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import *
defaultattr = {'class':'form-control'}
class AddGroupDataForm(forms.ModelForm):
    class Meta:
        model = GroupData
        fields = '__all__'
        exclude = ['group']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class':'form-control'}),
            'start_time': forms.TimeInput(attrs=defaultattr),
            'end_time': forms.TimeInput(attrs=defaultattr),
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
