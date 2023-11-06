from django.urls import path
from core.erp.views.category.views import *

from core.erp.views.dashboard.views import *

from core.erp.views.sale.views import *
from core.erp.views.tests.views import TestView
from core.erp.views.producto.views import *
from core.erp.views.mov.views import *
from core.erp.views.tiposmov.views import *
from core.erp.views.tiposprod.views import *
from core.erp.views.empleado.views import *
from core.erp.views.cliente.views import *
from core.erp.views.movemp.views import *
from core.erp.views.stock.views import *
from core.erp.views.proveedor.views import *
from core.erp.views.oc.views import *
from core.erp.views.conformidad.views import *


app_name = 'erp'

urlpatterns = [
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # client
 
    path('empleado/list/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado/add/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado/update/<str:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleado/delete/<str:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),
    # cliente
    path('cliente/list/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/add/', ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/update/<str:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/delete/<str:pk>/', ClienteDeleteView.as_view(), name='cliente_delete'),
    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # productob
    path('producto/list/', ProductoListView.as_view(), name='producto_list'),
    path('producto/add/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/update/<str:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/delete/<str:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
    #mov
    path('mov/list/', MovListView.as_view(), name='mov_list'),
    path('mov/add/', MovCreateView.as_view(), name='mov_create'),
    path('mov/delete/<int:pk>/', MovDeleteView.as_view(), name='mov_delete'),
    path('mov/update/<int:pk>/', MovUpdateView.as_view(), name='mov_update'),
    path('mov/invoice/pdf/<int:pk>/', MovInvoicePdfView.as_view(), name='mov_invoice_pdf'),
    #movimientos empleados
    path('movemp/list/', MovEmpListView.as_view(), name='movemp_list'),
    path('movemp/add/', MovEmpCreateView.as_view(), name='movemp_create'),
    path('movemp/delete/<int:pk>/', MovEmpDeleteView.as_view(), name='movemp_delete'),
    path('movemp/update/<int:pk>/', MovEmpUpdateView.as_view(), name='movemp_update'),
    path('movemp/invoice/pdf/<int:pk>/', MovEmpInvoicePdfView.as_view(), name='movemp_invoice_pdf'),
    # tipos de movimientos
    path('tipomov/list/', TipoMovListView.as_view(), name='tipomov_list'),
    path('tipomov/add/', TipoMovCreateView.as_view(), name='tipomov_create'),
    path('tipomov/update/<int:pk>/', TipoMovUpdateView.as_view(), name='tipomov_update'),
    path('tipomov/delete/<int:pk>/', TipoMovDeleteView.as_view(), name='tipomov_delete'),
    # tipos de productos
    path('tipoprod/list/', TipoProdListView.as_view(), name='tipoprod_list'),
    path('tipoprod/add/', TipoProdCreateView.as_view(), name='tipoprod_create'),
    path('tipoprod/update/<int:pk>/', TipoProdUpdateView.as_view(), name='tipoprod_update'),
    path('tipoprod/delete/<int:pk>/', TipoProdDeleteView.as_view(), name='tipoprod_delete'),

    # proveedores
    path('proveedor/list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedor/add/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedor/update/<str:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedor/delete/<str:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),

    #oc
    path('oc/list/', OcListView.as_view(), name='oc_list'),
    path('oc/add/', OcCreateView.as_view(), name='oc_create'),
    path('oc/update/<str:pk>/', OcUpdateView.as_view(), name='oc_update'),
    path('oc/delete/<str:pk>/', OcDeleteView.as_view(), name='oc_delete'),
    path('oc/invoice/pdf/<int:pk>/', OcInvoicePdfView.as_view(), name='oc_invoice_pdf'),

    # category
    path('conformidad/list/', ConformidadListView.as_view(), name='conformidad_list'),
    path('conformidad/add/', ConformidadCreateView.as_view(), name='conformidad_create'),
    path('conformidad/update/<int:pk>/', ConformidadUpdateView.as_view(), name='conformidad_update'),
    path('conformidad/delete/<int:pk>/', ConformidadDeleteView.as_view(), name='conformidad_delete'),
    
    
    #inventario

    path('inventario/list/', StockListView.as_view(), name='stock_list'),

]
