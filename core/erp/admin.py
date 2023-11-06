from django.contrib import admin
from core.erp.models import *

# Register your models here.
admin.site.register(Category)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        
        'id',
        'estado',
        'pvp',

    )
    search_fields =('id',)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(TipoProducto)
admin.site.register(Cliente)
admin.site.register(TipoMovimiento)
admin.site.register(Movimiento)
admin.site.register(Empleado)
admin.site.register(DetMov)
admin.site.register(DetSale)
admin.site.register(Sale)
admin.site.register(MovEmp)
admin.site.register(DetMovEmp)
admin.site.register(Proveedor)
admin.site.register(OrdenCompra)
admin.site.register(Conformidad)
admin.site.register(DetOc)
