from datetime import datetime

from django.forms import *

from core.erp.models import *
 

class PosteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Poste
        fields = '__all__'
        widgets = {

           
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'tipo_cruceta': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'tipo_abrazadera': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class PosteFormEdit(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for form in self.visible_fields():
        #    form.field.widget.attrs['class'] = 'form-control'
        #    form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].widget.attrs['readonly'] = True

     # Establ

    class Meta:
        model = Poste
        fields = '__all__'
        widgets = {

           
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'tipo_cruceta': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'tipo_abrazadera': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
            
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    


class ProyectoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {

           
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),

            'proveedor': SelectMultiple(
                                     attrs={
                                         'class': 'form-control select2',
                                         'style':'width: 100%',
                                         'multiple':'multiple'
                                     })
            
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProyectoFormEdit(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for form in self.visible_fields():
        #    form.field.widget.attrs['class'] = 'form-control'
        #    form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        #self.fields['name'].widget.attrs['readonly'] = True

     # Establ

    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {

           
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),

            'proveedor': SelectMultiple(
                                     attrs={
                                         'class': 'form-control select2',
                                         'style':'width: 100%',
                                         'multiple':'multiple'
                                     })
           
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
            
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    

class ProveedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {

           
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProveedorFormEdit(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for form in self.visible_fields():
        #    form.field.widget.attrs['class'] = 'form-control'
        #    form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        #self.fields['name'].widget.attrs['readonly'] = True

     # Establ

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {

           
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
           
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
            
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



from django.forms import ModelForm, Select
from .models import Diseno

class DisenoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proyecto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Diseno
        fields = '__all__'
        widgets = {
            'proyecto': Select(  # Cambiado de TextInput a Select
                attrs={
                    'placeholder': 'Seleccione un proyecto',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super(DisenoForm, self).save(commit=False)  # Asegúrate de llamar a super correctamente
        try:
            if self.is_valid():
                if commit:
                    form.save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class DisenoFormEdit(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proyecto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Diseno
        fields = '__all__'
        widgets = {
            'proyecto': Select(  # Cambiado de TextInput a Select
                attrs={
                    'placeholder': 'Seleccione un proyecto',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super(DisenoFormEdit, self).save(commit=False)  # Asegúrate de llamar a super correctamente
        try:
            if self.is_valid():
                if commit:
                    form.save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
