from django import forms
from .models import Farm


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = [
            "name",
            "email",
            "address",
            "size_in_hectares",
            "telephone",
            "account_number",
            "sector",
        ]
          
    def __init__(self,  *args, **kwargs):
        super(FarmForm, self).__init__(*args, **kwargs) 
#        self.fields["site"].widget = HiddenInput()
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"