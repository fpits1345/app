from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel

#listo
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

#listo
class TipoProducto(models.Model):

    name = models.CharField(max_length=20, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
class TipoMovimiento(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimientos'
        ordering = ['id']

class Producto(models.Model):
    
    id = models.CharField(verbose_name='identificador único', max_length=50, unique=True, blank=False, null=False, primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE, verbose_name='Tipo de producto')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0, verbose_name='stock')

    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio unitario')
    estado = models.BooleanField(verbose_name='Incorporado', default=True)


    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['tipo'] = self.tipo.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
    
        return item
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
#listo

class Persona(models.Model):
    id=models.CharField(verbose_name='Rut',max_length=20 , unique=True, blank=False, null=False, primary_key=True)
    nombre=models.CharField(verbose_name='Nombre', max_length=50,  blank=False, null=False)
    apellido=models.CharField(verbose_name='Apellido',max_length= 50 , blank=False, null=False)
    direccion=models.CharField(verbose_name='Direccion',max_length= 120, blank=True, null=True)
    correo=models.EmailField(verbose_name='Correo', blank=False, null=False)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural='Personas'
        db_table= 'Persona'
        ordering=['id']

class Cliente(Persona):
    username=models.CharField(verbose_name='Username Ipanel', max_length=25, unique=True, blank=False, null=False)
    folio_contrato=models.PositiveIntegerField(verbose_name='Folio', blank=True, null=True)

    def __str__(self):
        return self.username
    
    def toJSON(self):
        item = model_to_dict(self)
    
        return item
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural='Clientes'
        db_table= 'Cliente'
        ordering=['id'] 

class Empleado(Persona): 

    cargo=models.CharField(verbose_name='Cargo',max_length=25)
  
    def __str__(self):
        return self.id
    
    
    def toJSON(self):
        item = model_to_dict(self)
        # Agrega aquí cualquier otro campo que desees incluir en la representación JSON del empleado.
        return item

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural='Empleados'
        db_table= 'Empleado'
        ordering=['id']

#Movimimiento principal
class Movimiento(models.Model):
    #cli = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    #emp = models.ForeignKey(Empleado, on_delete=models.CASCADE, blank=True, null=True)
    date_joined = models.DateField(default=datetime.now)
    #direccion= models.CharField(verbose_name='Dirección', max_length=100)
    tipo = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)
    #subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['emp'] = self.emp.toJSON()
        item['tipo'] = self.tipo.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detmov_set.all()]
        return item

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['id']


class MovCliente(Movimiento):
    cli = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    emp = models.ForeignKey(Empleado, on_delete=models.CASCADE, blank=True, null=True)
    direccion= models.CharField(verbose_name='Dirección', max_length=100)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['emp'] = self.emp.toJSON()
        item['tipo'] = self.tipo.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detmov_set.all()]
        return item

    class Meta:
        verbose_name = 'Movimiento Cliente'
        verbose_name_plural = 'Movimientos Clientes'
        ordering = ['id']



class DetMov(models.Model):
    movimiento = models.ForeignKey(MovCliente, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['movimiento'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Movimiento'
        verbose_name_plural = 'Detalle de Movimientos'
        ordering = ['id']

class MovEmp(Movimiento):
    emp = models.ForeignKey(Empleado, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['emp'] = self.emp.toJSON()
        item['tipo'] = self.tipo.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detmovemp_set.all()]
        return item

    class Meta:
        verbose_name = 'Movimiento Empleado'
        verbose_name_plural = 'Movimientos Empleados'
        ordering = ['id']



class DetMovEmp(models.Model):
    movimiento = models.ForeignKey(MovEmp, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['movimiento'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Movimiento Empleado'
        verbose_name_plural = 'Detalle de Movimientos Empleados'
        ordering = ['id']

#################################################################################################################################3



class Sale(Movimiento):
    cli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.username

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['tipo'] = self.tipo.toJSON()
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']



####################################################################
#nuevo

class Proveedor(models.Model):
    id = models.CharField(primary_key=True, verbose_name='Rut',max_length=50, unique=True, blank=False, null=False)
    razon_social=models.CharField(verbose_name='Razón Social', max_length=120, blank=False, null=False)
    pagina_web= models.CharField(verbose_name='Página web', blank=True, null=True)
    correo_prov= models.EmailField(verbose_name='Correo', blank=False, null=False)
    
    def __str__(self):
        return self.id

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'proveedores'
        ordering = ['id']
    

##############################################################################################################

class OrdenCompra(models.Model):
    pro = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.pro.razon_social

    def toJSON(self):
        item = model_to_dict(self)
        item['pro'] = self.pro.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detoc_set.all()]
        return item

    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Ordenes'
        ordering = ['id']


class DetOc(models.Model):
    oc = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self)
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de oc'
        verbose_name_plural = 'Detalles oc'
        ordering = ['id']

##############################################################################################################

class Conformidad(models.Model):#listo

    choice_conformidad = [
        ('Conforme','Conforme'),
        ('No conforme','No conforme'),
    ]
    tipo_conformidad=models.CharField(verbose_name='Tipo de Conformidad', blank=False, null=False, choices=choice_conformidad)

    id_proveedor=models.ForeignKey(Proveedor,verbose_name='Proveedor',on_delete=models.CASCADE)
    obs_prov=models.TextField(verbose_name='Causa', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Conformidad'
        verbose_name_plural = 'Conformidades'
        ordering = ['id']
