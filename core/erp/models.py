from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel


###############################################################################################
class TipoCruceta(models.Model):

    name = models.CharField(max_length=20, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
class TipoAbrazadera(models.Model):

    name = models.CharField(max_length=20, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    

class TipoPoste(models.Model):

    name = models.CharField(max_length=20, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Proveedor(models.Model):

    name = models.CharField(max_length=20, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item     


class Proyecto(models.Model):

    name = models.CharField(max_length=20, verbose_name='Nombre', unique=True)
    contacto = models.IntegerField(verbose_name= 'Telefono', null=True, blank=True)
    mail = models.CharField(max_length=100, verbose_name= 'Correo', null=True, blank=True)
    direccion = models.CharField(max_length=100, verbose_name= 'Dirección', null=True, blank=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    proveedor = models.ManyToManyField(Proveedor, verbose_name='Proveedores', blank=True)
    soti = models.BooleanField(default=False, verbose_name='¿Sala soti?')
    shaft = models.BooleanField(default=False, verbose_name='¿shaft?')
    cant_departamentos = models.IntegerField(verbose_name= 'Cantidad de departamentos', null=True, blank=True)
    cant_casas = models.IntegerField(verbose_name= 'Cantidad de casas', null=True, blank=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = list(self.proveedor.values('id', 'name'))
        return item



class Poste(models.Model):
    
   
    name = models.CharField(max_length=150, verbose_name='Nombre')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='Proyecto', null=True, blank=True)
    tipo_poste = models.ForeignKey(TipoPoste, on_delete=models.CASCADE, verbose_name='Tipo Poste')
    tipo_cruceta = models.ForeignKey(TipoCruceta, on_delete=models.CASCADE, verbose_name='Altura')
    tipo_abrazadera = models.ForeignKey(TipoAbrazadera, on_delete=models.CASCADE, verbose_name='Transformador')


   
    remate = models.BooleanField(default=False, verbose_name='¿Tiene remate?')

    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    obs = models.CharField(max_length=500, null=True, blank=True, verbose_name='Observaciones')

    latitud = models.FloatField(verbose_name='Latitud', null=True, blank=True)
    longitud = models.FloatField(verbose_name='Longitud', null=True, blank=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['proyecto'] = self.proyecto.toJSON() if self.proyecto else None
        item['tipo_cruceta'] = self.tipo_cruceta.toJSON()
        item['tipo_abrazadera'] = self.tipo_abrazadera.toJSON()
        item['tipo_poste'] = self.tipo_poste.toJSON()
        item['image'] = self.get_image()
        
    
        return item
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Poste'
        verbose_name_plural = 'Postes'
        ordering = ['id']


