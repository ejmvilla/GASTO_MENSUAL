from django import forms
from .models import Plantilla, Renglon, Registro
from django.core.exceptions import ValidationError

class RenglonForm(forms.ModelForm):
    class Meta:
        model=Renglon
        fields = ['plantilla', 'descripcion', 'dia', 'monto', 'activo']
        widgets = {
            'dia': forms.NumberInput(attrs={'min': 1, 'max': 31}),
        }


class RegistroForm(forms.ModelForm):
    class Meta:
        model=Registro
        fields = ['descripcion', 'fecha', 'monto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }         
    #Validacion para que el campo moto sea >=1000
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto < 1000:
            raise ValidationError('El monto debe ser mayor o igual a 1000.')
        return monto