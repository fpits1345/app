from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TipoMovForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import TipoMovimiento


class TipoMovListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TipoMovimiento
    template_name = 'tiposmov/list.html'
    permission_required = 'view_tipomovimiento'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TipoMovimiento.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de movimiento'
        context['create_url'] = reverse_lazy('erp:tipomov_create')
        context['list_url'] = reverse_lazy('erp:tipomov_list')
        context['entity'] = 'Tipos de movimientos'
        return context


class TipoMovCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TipoMovimiento
    form_class = TipoMovForm
    template_name = 'tiposmov/create.html'
    success_url = reverse_lazy('erp:tipomov_list')
    permission_required = 'add_tipomovimiento'
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
        context['title'] = 'Tipos de movimientos'
        context['entity'] = 'Tipos de movimiento'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TipoMovUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TipoMovimiento
    form_class = TipoMovForm
    template_name = 'tiposmov/create.html'
    success_url = reverse_lazy('erp:tipomov_list')
    permission_required = 'change_tipomovimiento'
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
        context['title'] = 'Edición un movimiento'
        context['entity'] = 'Tipos de movimiento'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TipoMovDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TipoMovimiento
    template_name = 'tiposmov/delete.html'
    success_url = reverse_lazy('erp:tipomov_list')
    permission_required = 'delete_tipomovimiento'
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
        context['title'] = 'Eliminación de un movimiento'
        context['entity'] = 'Tipos de movimientos'
        context['list_url'] = self.success_url
        return context
