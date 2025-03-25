# zde budou formuláře
# tento import by měl sloužit k registraci uživatele
from django.contrib.auth.forms import UserCreationForm

# reports/forms.py
from django import forms
from .models import Paragraph, Chart, Table

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ['text']

class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = ['title', 'dataset'] #  možná upload pro dataset

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['title', 'data'] # Uložit data jako JSON
# zde bude formulář na založení sekce

# zde bude formulář na odstavec

# zde bude formulář na graf

# zde bude formulář na tabulku