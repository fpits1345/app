from django.views.generic import TemplateView
from django.db.models import Sum , DecimalField, F
from django.db.models.functions import Coalesce 
from django.shortcuts import render
from django.db.models import Count
from core.erp.models import Sale, Producto, DetSale, Movimiento, TipoMovimiento , MovCliente, Conformidad, Proveedor, MovEmp, TipoProducto
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import json

class DashboardView(TemplateView, LoginRequiredMixin ):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                data = self.get_graph_sales_year_month()
            elif action == 'get_graph_mov_products':
                data = self.get_graph_mov_products()
            elif action == 'get_movements_by_month':
                data = self.get_movements_by_month()
 

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)



    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year= year, date_joined__month=m ).aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                data.append(float(total))
        except:
            pass

        return data
    
    def get_graph_mov_products(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            tipo_productos = TipoProducto.objects.all()
            for tipo_producto in tipo_productos:
                total_sales = DetSale.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month, prod__tipo=tipo_producto).count()
                if total_sales > 0:
                    data.append({
                        'name': tipo_producto.name,
                        'y': total_sales
                    })
        except:
            pass

        return data
    

    def get_top_products(self):
        top_products = Producto.objects.annotate(
        total_sales=Sum(F('detsale__cant'), output_field=DecimalField(max_digits=9, decimal_places=2))
    ).order_by('-total_sales')[:5]
        return top_products
    
    
    def get_critical_products(self):
        # Filtra los productos con stock crítico (stock <= 10, ajusta el umbral según tus necesidades)
        critical_products = Producto.objects.filter(stock__lte=5)
        return critical_products
    
    def get_medium_products(self):
    # Filtra los productos con stock entre 6 y 15 (ajusta el rango según tus necesidades)
        medium_products = Producto.objects.filter(stock__gte=6, stock__lte=15)
        return medium_products
    
    def get_normal_products(self):
    # Filtra los productos con stock superior a 15 (ajusta el umbral según tus necesidades)
        normal_products = Producto.objects.filter(stock__gt=15)
        return normal_products



    def get_top_providers_with_conformities(self):
        top_providers = Proveedor.objects.annotate(conformity_count=Count('conformidad')).order_by('-conformity_count')[:5]
        return top_providers

    def get_movement_percentage_by_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for m in range(1, month + 1):
                total_movements_in_month = MovEmp.objects.filter(date_joined__year=year, date_joined__month=m).count()
                month_name = datetime(year, m, 1).strftime('%B')  # Obtener el nombre del mes
                if total_movements_in_month > 0:
                    result = MovEmp.objects.filter(date_joined__year=year, date_joined__month=m) \
                        .values('tipo__name') \
                        .annotate(count=Count('tipo')) \
                        .order_by('tipo__name')
                    for item in result:
                        item['percentage'] = (item['count'] / total_movements_in_month) * 100
                    data.append({
                        'month_name': month_name,
                        'data': result,
                    })
                else:
                    data.append({
                        'month_name': month_name,
                        'data': [],
                    })
        except Exception as e:
            print(str(e))  # Maneja adecuadamente las excepciones en tu aplicación
        return data

    
    def get_stock_summary(self):
        total_products = Producto.objects.count()
        zero_stock_products = Producto.objects.filter(stock=0).count()
        stock_greater_than_zero_products = Producto.objects.filter(stock__gt=0).count()
    
        if total_products == 0:
            zero_stock_percentage = 0
            stock_greater_than_zero_percentage = 0
        else:
            zero_stock_percentage = round((zero_stock_products / total_products) * 100, 2)
            stock_greater_than_zero_percentage = round((stock_greater_than_zero_products / total_products) * 100, 2)

        return total_products, zero_stock_products, zero_stock_percentage, stock_greater_than_zero_products, stock_greater_than_zero_percentage

    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        context['top_products'] = self.get_top_products()
        context['critical_products'] = self.get_critical_products()
        context['medium_products'] = self.get_medium_products()
        context['normal_products'] = self.get_normal_products()
        context['top_providers_with_conformities'] = self.get_top_providers_with_conformities()
        context['movement_percentage_by_month'] = self.get_movement_percentage_by_month()
        total_products, zero_stock_products, zero_stock_percentage, stock_greater_than_zero_products, stock_greater_than_zero_percentage = self.get_stock_summary()
    
        context['total_products'] = total_products
        context['zero_stock_products'] = zero_stock_products
        context['zero_stock_percentage'] = zero_stock_percentage
        context['stock_greater_than_zero_products'] = stock_greater_than_zero_products
        context['stock_greater_than_zero_percentage'] = stock_greater_than_zero_percentage


   
        
 
        return context
