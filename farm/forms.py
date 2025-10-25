from django import forms
from .models import Farm, Statement, SiteVisit


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
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class StatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = [
            "farm",
            "period_start",
            "period_end",
            "currency",
            "total_expenses",
            "total_sales"
        ]
        widgets = {
            "period_start": forms.DateInput(attrs={"type": "date"}),
            "period_end": forms.DateInput(attrs={"type": "date"}),
        }
 
    def __init__(self, *args, **kwargs):
        super(StatementForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

class SiteVisitForm(forms.ModelForm):
    class Meta:
        model = SiteVisit
        fields = [
            "purpose",
            "farm",
            "agent",
            "visit_date",
            "notes",
            "status",
            "resolution_notes"
        ]
        widgets = {
            "visit_date": forms.DateInput(attrs={"type": "date"}),
        }
 
    def __init__(self, *args, **kwargs):
        super(SiteVisitForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"