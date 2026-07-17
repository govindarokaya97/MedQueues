from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Medicine, StockTransaction, Prescription, PrescriptionItem

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
            "notes",
        ]
    
    
class PrescriptionItemForm(forms.ModelForm):
    
    class Meta:
        model = PrescriptionItem
        fields =[
            "medicine",
            "quantity",
            "dosage",
            "duration",
            "instructions"
        ]
        
    def clean(self):
        clean_data = super().clean()
        
        medicine = clean_data.get("medicine")
        quantity = clean_data.get("quantity")
        
        if medicine and quantity:
            if quantity > medicine.stock_quantity:
                raise forms.ValidationError(
                    f"Only {medicine.stock_quantity} units of {medicine.name} are available."
                )
                
        return clean_data
        

class BasePrescriptionItemFormSet(BaseInlineFormSet):
    
    def clean(self):
        super().clean()
        
        medicines =[]
        
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE"):
                continue
            
            medicine = form.cleaned_data.get("medicine")
            
            if medicine:
                if medicine in medicines:
                    raise forms.ValidationError(
                        f"{medicine.name} has been selected more than once."
                    )
                medicines.append(medicine)
                


PrescriptionItemFormSet = inlineformset_factory(
    Prescription,
    PrescriptionItem,
    form=PrescriptionItemForm,
    formset= BasePrescriptionItemFormSet,
    extra=1,
    can_delete=True,
)
