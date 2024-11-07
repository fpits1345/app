from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel


###############################################################################################

    
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
    adm = models.CharField(max_length=500, null=True, blank=True, verbose_name='Administrador')
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

class Diseno(models.Model):


    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='proyecto', default=1)
    olt = models.IntegerField(default=False, verbose_name='OLT')
    odf = models.IntegerField(default=False, verbose_name='ODF')
    hilo = models.CharField(max_length=100, verbose_name= 'Hilo', null=True, blank=True)
    slot = models.CharField(max_length=100, verbose_name= 'slot', null=True, blank=True)
    pon = models.CharField(max_length=100, verbose_name= 'pon', null=True, blank=True)

    nap8 = models.IntegerField(verbose_name= 'Cuantas nap de 8', null=True, blank=True)
    nap16 = models.IntegerField(verbose_name= 'Cuantas nap de 16', null=True, blank=True)


    m1 = models.IntegerField(verbose_name= 'Cantidad de Mufa M1', null=True, blank=True)
    m2 = models.IntegerField(verbose_name= 'Cantidad de Mufa M2', null=True, blank=True)

    sp2 = models.IntegerField(verbose_name= 'Cuantos splitter de 2', null=True, blank=True)
    sp4 = models.IntegerField(verbose_name= 'Cuantos splitter de 4', null=True, blank=True)
    sp8 = models.IntegerField(verbose_name= 'Cuantos splitter de 8', null=True, blank=True)
    sp16 = models.IntegerField(verbose_name= 'Cuantos splitter de 16', null=True, blank=True)



    odf1 = models.IntegerField(verbose_name= 'odf puertos', null=True, blank=True)
    odf2 = models.IntegerField(verbose_name= 'odf puertos', null=True, blank=True)
    odf3 = models.IntegerField(verbose_name= 'odf puertos', null=True, blank=True)
    
    cable4 = models.IntegerField(verbose_name= 'metros de cable 4', null=True, blank=True)
    cable8 = models.IntegerField(verbose_name= 'metros de cable 8', null=True, blank=True)
    cable12= models.IntegerField(verbose_name= 'Metros de cable 12', null=True, blank=True)
    cable24= models.IntegerField(verbose_name= 'Metros de cable 24', null=True, blank=True)
    cable48= models.IntegerField(verbose_name= 'Metros de cable 48', null=True, blank=True)
    cable96= models.IntegerField(verbose_name= 'Metros de cable 96', null=True, blank=True)
    

    hp = models.IntegerField(verbose_name= 'HP', null=True, blank=True)
    obs = models.TextField(verbose_name= 'Conclusión', null=True, blank=True)


    def __str__(self):
        return self.proyecto.name

    def toJSON(self):
        item = model_to_dict(self)
    # Acceder a los campos del objeto relacionado proyecto
        item['proyecto'] = {
            'id': self.proyecto.id,
            'name': self.proyecto.name
        }
        return item



class Potencia(models.Model):
    # Definir opciones para el campo tipo
    TIPO_CHOICES = [
        ('mufa', 'Mufa'),
        ('nap', 'NAP'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='proyecto', default=1)
    tipo = models.CharField(max_length=100, verbose_name='Tipo', choices=TIPO_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Nombre', null=True, blank=True)
    potencia = models.FloatField(verbose_name='Potencia', null=True, blank=True)  # Corregí el nombre a 'potencia'
    obs = models.CharField(max_length=100, verbose_name='Observación', null=True, blank=True)

    def __str__(self):
        return self.proyecto.name

    def toJSON(self):
        item = model_to_dict(self)
        # Acceder a los campos del objeto relacionado proyecto
        item['proyecto'] = {
            'id': self.proyecto.id,
            'name': self.proyecto.name
        }
        return item


class Poste(models.Model):
    
   
    name = models.CharField(max_length=150, verbose_name='Nombre')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='Proyecto', null=True, blank=True)
    tipo_poste = models.ForeignKey(TipoPoste, on_delete=models.CASCADE, verbose_name='Tipo Poste')
    tipo_abrazadera = models.ForeignKey(TipoAbrazadera, on_delete=models.CASCADE, verbose_name='Altura')
    transformador = models.BooleanField(default=False, verbose_name='¿Tiene transformador?')

   
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


