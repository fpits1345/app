from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ConformidadForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Conformidad


class ConformidadListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Conformidad
    template_name = 'conformidad/list.html'
    permission_required = 'view_conformidad'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Conformidad.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Conformidades'
        context['create_url'] = reverse_lazy('erp:conformidad_create')
        context['list_url'] = reverse_lazy('erp:conformidad_list')
        context['entity'] = 'Conformidades'
        return context


class ConformidadCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Conformidad
    form_class = ConformidadForm
    template_name = 'conformidad/create.html'
    success_url = reverse_lazy('erp:conformidad_list')
    permission_required = 'add_conformidad'
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
        context['title'] = 'Creación una conformidad'
        context['entity'] = 'Conformidades'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ConformidadUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Conformidad
    form_class = ConformidadForm
    template_name = 'conformidad/create.html'
    success_url = reverse_lazy('erp:conformidad_list')
    permission_required = 'change_conformidad'
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
        context['title'] = 'Edición una conformidad'
        context['entity'] = 'Conformidades'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ConformidadDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Conformidad
    template_name = 'conformidad/delete.html'
    success_url = reverse_lazy('erp:conformidad_list')
    permission_required = 'delete_conformidad'
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
        context['title'] = 'Eliminación de un conformidad'
        context['entity'] = 'Conformidades'
        context['list_url'] = self.success_url
        return context
