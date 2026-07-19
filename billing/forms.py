from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'
        
        
        
class BillPaymentForm(forms.ModelForm):
    
    class Meta:
        model = Bill
        fields = [
            "payment_status",
            "payment_method",
            "notes"
        ]
        
        widgets = {
            "payment_method": forms.Select(
                attrs={"class": "form-select"}
                
            ),
            "payment_status": forms.Select(
                attrs={"class": "form-select"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-select",
                    "rows": 3,
                }
            ),
        }