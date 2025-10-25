from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role')
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'role': forms.Select(),  # adjust if role is a different field type
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' form-control').strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        # any extra processing (e.g. normalize email) can go here
        if commit:
            user.save()
        return user