from django import forms
from .models import Farm, Statement, SiteVisit, FarmEmployeeStats, Notice


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


class FarmEmployeeStatsForm(forms.ModelForm):
    class Meta:
        model = FarmEmployeeStats
        # exclude auto fields and created_by which should be set server-side
        exclude = ("created_by", "created", "updated", "total_contribution_usd", "total_contribution_zwl")
        widgets = {
            "reporting_month": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "employment_type": forms.Select(attrs={"class": "form-control"}),
            "citizen_male": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
            "citizen_female": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
            "expatriate_male": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
            "expatriate_female": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
            "basic_pay_usd": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "basic_pay_zwl": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "employees_contribution_usd": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "employees_contribution_zwl": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "employers_contribution_usd": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "employers_contribution_zwl": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "arrears_usd": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "arrears_zwl": forms.NumberInput(attrs={"step": "0.01", "min": 0, "class": "form-control"}),
            "created_by": forms.HiddenInput(),
            "farm": forms.Select(attrs={"class": "form-control"}),
        }
        # set the logged-in user as the default in the form __init__, e.g.:
        # def __init__(self, *args, user=None, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     if user is not None:
        #         self.fields['created_by'].initial = user

    def __init__(self, *args, **kwargs):
        super(FarmEmployeeStatsForm, self).__init__(*args, **kwargs)
        # ensure consistent classes for any fields not covered by widgets
        for name, field in self.fields.items():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned = super().clean()
        # enforce non-negative counts/payments
        int_fields = ["citizen_male", "citizen_female", "expatriate_male", "expatriate_female"]
        dec_fields = ["basic_pay_usd", "basic_pay_zwl",
                      "employees_contribution_usd", "employees_contribution_zwl",
                      "employers_contribution_usd", "employers_contribution_zwl",
                      "arrears_usd", "arrears_zwl"]
        for f in int_fields:
            v = cleaned.get(f)
            if v is not None and v < 0:
                self.add_error(f, "Value cannot be negative.")
        for f in dec_fields:
            v = cleaned.get(f)
            if v is not None and v < 0:
                self.add_error(f, "Value cannot be negative.")
        return cleaned

    def save(self, commit=True, created_by=None):
        """
        Compute totals before saving. Accept optional created_by to set the creator.
        Usage in view: form.save(commit=True, created_by=request.user)
        """
        inst = super(FarmEmployeeStatsForm, self).save(commit=False)

        # compute totals (sum of contributions + arrears)
        inst.total_contribution_usd = (
            (inst.employees_contribution_usd or 0)
            + (inst.employers_contribution_usd or 0)
            + (inst.arrears_usd or 0)
        )
        inst.total_contribution_zwl = (
            (inst.employees_contribution_zwl or 0)
            + (inst.employers_contribution_zwl or 0)
            + (inst.arrears_zwl or 0)
        )

        if created_by and getattr(inst, "created_by", None) is None:
            try:
                inst.created_by = created_by
            except Exception:
                pass

        if commit:
            inst.save()
            self.save_m2m()
        return inst


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = [
            "title",
            "message",
            "issued_by"
        ]
        
    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"