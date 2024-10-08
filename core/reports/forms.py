from django import forms
from core.erp.models import Proyecto

class ReportForm(forms.Form):
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        empty_label="Selecciona un proyecto",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%',
        })
    )