from django import forms
from .models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'student_id', 'department', 'avatar']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.is_student():
            if 'student_id' in self.fields:
                del self.fields['student_id']
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
