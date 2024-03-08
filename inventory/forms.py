# Create a form to handle CSV file uploads

from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')
