from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models.functions import Coalesce 
from core.erp.forms import ProductoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Producto, TipoMovimiento, Movimiento, Sale, DetSale, MovEmp, DetMov, OrdenCompra , DetMov
from django.db.models import Sum , DecimalField, F
from datetime import datetime, timedelta
from django.db import models
import json
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
class StockListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'stock/list.html'
    permission_required = 'view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:producto_create')
        context['list_url'] = reverse_lazy('erp:producto_list')
        context['entity'] = 'Productos'
        return context

"""


"""

class StockListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'stock/list.html'
    permission_required = 'view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for producto in Producto.objects.all():
                    producto_data = producto.toJSON()
                    producto_data['stock'] = self.calculate_stock(producto)
                    data.append(producto_data)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_productos_with_stock(self):
        productos = Producto.objects.all()
        data = []
        for producto in productos:
            producto_data = producto.toJSON()
            producto_data['stock'] = self.calculate_stock(producto)
            data.append(producto_data)
            producto.stock = producto_data['stock']  # Actualiza el stock del producto
            producto.save()  # Guarda el producto con el stock actualizado
        return data


    def calculate_stock(self, producto):
        total_stock = producto.stock
    # Sumar las entradas de movimientos para este producto
        entradas = MovEmp.objects.filter(tipo=1, detmovemp__prod=producto).aggregate(
        r=Coalesce(Sum('detmovemp__cant'), 0)
    )['r']
    # Restar las salidas de movimientos para este producto
        salidas = MovEmp.objects.filter(tipo=2, detmovemp__prod=producto).aggregate(
        r=Coalesce(Sum('detmovemp__cant'), 0)
    )['r']
        ventassuma = Sale.objects.filter(tipo=1, detsale__prod=producto).aggregate(
        r=Coalesce(Sum('detsale__cant'), 0)
    )['r']
        ventasresta = Sale.objects.filter(tipo=2,detsale__prod=producto).aggregate(
        r=Coalesce(Sum('detsale__cant'), 0)
    )['r']
        
          

        if entradas:
            total_stock += entradas 
        if salidas:

            total_stock -= salidas
        if ventassuma:
            total_stock += ventassuma
        
        if ventasresta:
            total_stock -= ventasresta
        return total_stock

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:producto_create')
        context['list_url'] = reverse_lazy('erp:stock_list')
        context['entity'] = 'Stock'
        return context

"""
        








#prueba 1 casi lista
"""
class StockListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'stock/list.html'
    permission_required = 'view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = self.get_productos_with_stock()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_productos_with_stock(self):
        productos = Producto.objects.all()
        data = []
        for producto in productos:
            producto.stock = self.calculate_stock(producto)  # Actualiza el stock del producto
            producto.save()  # Guarda el producto con el stock actualizado
            producto_data = producto.toJSON()
            producto_data['stock'] = producto.stock
            data.append(producto_data)
        return data

    def calculate_stock(self, producto):
        total_stock = producto.stock
        # Obtén la suma de las entradas recientes para este producto
        entradas = MovEmp.objects.filter(tipo=1, detmovemp__prod=producto).aggregate(
            r=Sum('detmovemp__cant', output_field=models.FloatField())
        )['r']
        # Obtén la suma de las salidas recientes para este producto
        salidas = MovEmp.objects.filter(tipo=2, detmovemp__prod=producto).aggregate(
            r=Sum('detmovemp__cant', output_field=models.FloatField())
        )['r']
        # Obtén la suma de las ventas recientes para este producto
        ventas = Sale.objects.filter(detsale__prod=producto).aggregate(
            r=Sum('detsale__cant', output_field=models.FloatField())
        )['r']

        if entradas:
            total_stock = entradas  # Actualiza el stock con las entradas recientes
        if salidas:
            total_stock -= salidas  # Resta las salidas recientes al stock
        if ventas:
            total_stock -= ventas  # Resta las ventas recientes al stock

        return total_stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:producto_create')
        context['list_url'] = reverse_lazy('erp:stock_list')
        context['entity'] = 'Stock'
        return context
"""








# Otras importaciones

class StockListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'stock/list.html'
    permission_required = 'view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for producto in Producto.objects.all():
                    producto_data = producto.toJSON()
                    producto_data['stock'] = self.calculate_stock(producto)
                    data.append(producto_data)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_productos_with_stock(self):
        productos = Producto.objects.all()
        data = []
        for producto in productos:
            producto_data = producto.toJSON()
            producto_data['stock'] = self.calculate_stock(producto)
            data.append(producto_data)
            producto.stock = producto_data['stock']  # Actualiza el stock del producto
            producto.save()  # Guarda el producto con el stock actualizado
        return data


    def calculate_stock(self, producto):
        # Establecer el campo stock en cero antes de los cálculos
        producto.stock = 0
        producto.save()

        total_stock = 0

        # Realizar los cálculos como lo estabas haciendo

        # Sumar las entradas de movimientos para este producto
        entradas = MovEmp.objects.filter(tipo=1, detmovemp__prod=producto).aggregate(
            r=Coalesce(Sum('detmovemp__cant'), 0)
        )['r']
        # Restar las salidas de movimientos para este producto
        salidas = MovEmp.objects.filter(tipo=2, detmovemp__prod=producto).aggregate(
            r=Coalesce(Sum('detmovemp__cant'), 0)
        )['r']
        ventassuma = Sale.objects.filter(tipo=1, detsale__prod=producto).aggregate(
            r=Coalesce(Sum('detsale__cant'), 0)
        )['r']
        ventasresta = Sale.objects.filter(tipo=2, detsale__prod=producto).aggregate(
            r=Coalesce(Sum('detsale__cant'), 0)
        )['r']
        oc = OrdenCompra.objects.filter(detoc__prod=producto).aggregate(
            r=Coalesce(Sum('detoc__cant'), 0)
        )['r']

        if entradas:
            total_stock += entradas
        if salidas:
            total_stock -= salidas
        if ventassuma:
            total_stock += ventassuma
        if ventasresta:
            total_stock -= ventasresta
        if oc:
            total_stock += oc

        # Actualizar el campo stock del producto con el valor calculado
        producto.stock = total_stock
        producto.save()

        return total_stock

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:producto_create')
        context['list_url'] = reverse_lazy('erp:stock_list')
        context['entity'] = 'Stock'
        return context