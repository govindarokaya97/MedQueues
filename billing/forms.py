from django.forms import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        felds = '__all__'