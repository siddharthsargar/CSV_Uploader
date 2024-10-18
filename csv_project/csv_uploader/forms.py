from django import forms

class CSVUploadForm(forms.Form):
    #csv_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    csv_file = forms.FileField()