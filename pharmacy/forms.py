from django import forms
from .models import Medicine, StockTransaction, Prescription, PrescriptionItems

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        
        
        widgets = {
            "expiry_date": forms.DateInput(attrs={"type":"date"}),
            "description": forms.Textarea(attrs={"rows": 3 }),
        }
    
class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        
        fields = [
            "medicine",
            "transaction_type",
            "quantity",
            "remarks",
        ]

class PrescriptionForm(forms.ModelForm):
    
    class Meta:
        model = Prescription
        fields=[
            "patient",
            "doctor",
            "appointment",
            "notes"
        ]
    
    
class PrescriptionItemForm(forms.ModelForm):
    
    class Meta:
        model = PrescriptionItems
        fields =[
            "medicine",
            "quantity",
            "dosage",
            "duration",
            "instructions"
        ]
    