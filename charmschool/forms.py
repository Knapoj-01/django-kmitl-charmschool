from django import forms
from django.forms import widgets
from .models import GroupData
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
   
