from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TipoProdForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import TipoProducto


class TipoProdListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TipoProducto
    template_name = 'tiposprod/list.html'
    permission_required = 'view_tipoproducto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TipoProducto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de Productos'
        context['create_url'] = reverse_lazy('erp:tipoprod_create')
        context['list_url'] = reverse_lazy('erp:tipoprod_list')
        context['entity'] = 'Tipos de Productos'
        return context


class TipoProdCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TipoProducto
    form_class = TipoProdForm
    template_name = 'tiposprod/create.html'
    success_url = reverse_lazy('erp:tipoprod_list')
    permission_required = 'add_tipoproducto'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de Productos'
        context['entity'] = 'Tipos de Productos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TipoProdUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TipoProducto
    form_class = TipoProdForm
    template_name = 'tiposprod/create.html'
    success_url = reverse_lazy('erp:tipoprod_list')
    permission_required = 'change_tipoproducto'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Productos'
        context['entity'] = 'Tipos de Productos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TipoProdDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TipoProducto
    template_name = 'tiposprod/delete.html'
    success_url = reverse_lazy('erp:tipoprod_list')
    permission_required = 'delete_tipoproducto'
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
        context['title'] = 'Eliminación de un Tipo de Producto'
        context['entity'] = 'Tipos de Productos'
        context['list_url'] = self.success_url
        return context
