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

from core.erp.forms import OcForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import OrdenCompra, DetOc, Producto


class OcListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = OrdenCompra
    template_name = 'oc/list.html'
    permission_required = 'view_ordencompra'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in OrdenCompra.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetOc.objects.filter(oc_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Ordenes de Compra'
        context['create_url'] = reverse_lazy('erp:oc_create')
        context['list_url'] = reverse_lazy('erp:oc_list')
        context['entity'] = 'Ordenes'
        return context


class OcCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = OrdenCompra
    form_class = OcForm
    template_name = 'oc/create.html'
    success_url = reverse_lazy('erp:oc_list')
    permission_required = 'add_oc'
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
                    oc = OrdenCompra()
                    oc.pro_id = vents['pro']
                    oc.date_joined = vents['date_joined']
                    oc.subtotal = float(vents['subtotal'])
                    oc.iva = float(vents['iva'])
                    oc.total = float(vents['total'])
                    oc.save()
                    for i in vents['products']:
                        det = DetOc()
                        det.oc_id = oc.id
                        det.prod_id = i['id']  
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
    

                    data = {'id': oc.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Orden'
        context['entity'] = 'Ordenes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context


class OcUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = OrdenCompra
    form_class = OcForm
    template_name = 'oc/create.html'
    success_url = reverse_lazy('erp:oc_list')
    permission_required = 'change_oc'
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
                    oc = self.get_object()
                    oc.date_joined = vents['date_joined']
                    oc.pro_id = vents['pro']
                    oc.subtotal = float(vents['subtotal'])
                    oc.iva = float(vents['iva'])
                    oc.total = float(vents['total'])
                    oc.save()
                    oc.detoc_set.all().delete()
                    for i in vents['products']:
                        det = DetOc()
                        det.oc_id = oc.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': oc.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetOc.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Orden'
        context['entity'] = 'Ordenes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        return context


class OcDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = OrdenCompra
    template_name = 'oc/delete.html'
    success_url = reverse_lazy('erp:oc_list')
    permission_required = 'delete_oc'
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
        context['title'] = 'Eliminación de una Orden'
        context['entity'] = 'Ordenes'
        context['list_url'] = self.success_url
        return context


class OcInvoicePdfView(View):

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
            template = get_template('oc/invoice.html')
            context = {
                'oc': OrdenCompra.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Inetwork SpA', 'ruc': '9999999999999', 'address': 'Coquimbo, Chile'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:oc_list'))
