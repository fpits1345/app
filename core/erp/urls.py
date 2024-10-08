from django.urls import path

from core.erp.views.dashboard.views import *
from core.erp.views.proyecto.views import *
from core.erp.views.poste.views import *
from core.erp.views.proveedor.views import *

app_name = 'erp'

urlpatterns = [   
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    #poste
    path('poste/list/', PosteListView.as_view(), name='poste_list'),
    path('poste/add/', PosteCreateView.as_view(), name='poste_create'),
    path('poste/update/<str:pk>/', PosteUpdateView.as_view(), name='poste_update'),
    path('poste/delete/<str:pk>/', PosteDeleteView.as_view(), name='poste_delete'),
    
    #proyectos
    path('proyecto/list/', ProyectoListView.as_view(), name='proyecto_list'),
    path('proyecto/add/', ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyecto/update/<str:pk>/', ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyecto/delete/<str:pk>/', ProyectoDeleteView.as_view(), name='proyecto_delete'),

    #proveedor
    path('prov/list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('prov/add/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('prov/update/<str:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('prov/delete/<str:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),

    

]
