from django import forms


class TaskForm(forms.Form):
    task_name = forms.CharField(max_length=30)
    header_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    source_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
