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
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'editor',  # musí odpovídat v JS
                'placeholder': 'Zadejte text odstavce…'
            }),
        }


class ChartForm(forms.ModelForm):
    chart_type = forms.ChoiceField(choices=[
        ('line', 'Spojnicový'),
        ('bar', 'Sloupcový'),
        ('pie', 'Koláčový')
    ])
    color = forms.CharField(required=False, help_text="Hex kód nebo název barvy")
    data_x = forms.CharField(widget=forms.Textarea, help_text="Čárkou oddělené roky, např. 2010,2011,...")
    data_y = forms.CharField(widget=forms.Textarea, help_text="Čárkou oddělené hodnoty, např. 12.5,13.0,...")

    class Meta:
        model = Chart
        fields = ['title']
        
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['title', 'data'] # Uložit data jako JSON
# zde bude formulář na založení sekce

# zde bude formulář na tabulku