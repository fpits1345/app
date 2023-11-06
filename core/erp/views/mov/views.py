import json
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from xhtml2pdf import pisa

from core.erp.forms import MovForm
from core.erp.mixins import ValidatePermissionRequiredMixin
#from core.erp.models import Sale, Product, DetSale
from core.erp.models import MovCliente, Producto, DetMov


class MovListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = MovCliente
    template_name = 'mov/list.html'
    permission_required = 'view_movimiento'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data_list = []  # Usar una variable diferente para almacenar la lista
                for i in MovCliente.objects.all():
                        data_list.append(i.toJSON())
                data = data_list  # Asignar la lista a data después de que esté completa
            elif action == 'search_details_prod':
                data_list = []  # Usar una variable diferente para almacenar la lista
                for i in DetMov.objects.filter(movimiento_id=request.POST['id']):
                    data_list.append(i.toJSON())
                data = data_list  # Asignar la lista a data después de que esté completa
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Movimientos'
        context['create_url'] = reverse_lazy('erp:mov_create')
        context['list_url'] = reverse_lazy('erp:mov_list')
        context['entity'] = 'Movimientos'
        return context


class MovCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = MovCliente
    form_class = MovForm
    template_name = 'mov/create.html'
    success_url = reverse_lazy('erp:mov_list')
    permission_required = 'add_movimiento'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # item['value'] = i.name
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    movimiento = MovCliente()
                    movimiento.date_joined = vents['date_joined']
                    movimiento.tipo_id = vents['tipo']
                    movimiento.cli_id = vents['cli']
                    movimiento.emp_id = vents['emp']
                    movimiento.direccion = vents['direccion']
                    movimiento.subtotal = float(vents['subtotal'])
                 
                    movimiento.save()
                    for i in vents['products']:
                        det = DetMov()
                        det.movimiento_id = movimiento.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': movimiento.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context


class MovUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = MovCliente
    form_class = MovForm
    template_name = 'mov/create.html'
    success_url = reverse_lazy('erp:mov_list')
    permission_required = 'change_movimiento'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    movimiento = self.get_object()
                    movimiento.date_joined = vents['date_joined']
                    movimiento.tipo_id = vents['tipo']
                    movimiento.cli_id = vents['cli']
                    movimiento.emp_id = vents['emp']
                    movimiento.direccion = vents['direccion']
                    movimiento.subtotal = float(vents['subtotal'])
                    movimiento.save()
                    movimiento.detmov_set.all().delete()
                    for i in vents['products']:
                        det = DetMov()
                        det.movimiento_id = movimiento.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': movimiento.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetMov.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Movimiento'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        return context


class MovDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = MovCliente
    template_name = 'mov/delete.html'
    success_url = reverse_lazy('erp:mov_list')
    permission_required = 'delete_movimiento'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Movimiento'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        return context


class MovInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('mov/invoice.html')
            context = {
                'sale': MovCliente.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Inetworks SpA', 'ruc': '9999999999999', 'address': 'Coquimbo, Chile'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:mov_list'))
