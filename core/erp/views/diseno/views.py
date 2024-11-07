from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import DisenoForm, DisenoFormEdit
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Diseno


class DisenoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Diseno
    template_name = 'diseno/list.html'
    permission_required = 'view_diseno'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Diseno.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Diseno'
        context['create_url'] = reverse_lazy('erp:diseno_create')
        context['list_url'] = reverse_lazy('erp:diseno_list')
        context['entity'] = 'Diseño'
        return context


class DisenoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Diseno
    form_class = DisenoForm
    template_name = 'Diseno/create.html'
    success_url = reverse_lazy('erp:diseno_list')
    permission_required = 'add_diseno'
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
        context['title'] = 'Creación de un diseño'
        context['entity'] = 'Diseño'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class DisenoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Diseno
    form_class = DisenoFormEdit
    template_name = 'diseno/create.html'
    success_url = reverse_lazy('erp:diseno_list')
    permission_required = 'change_diseno'
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
        context['title'] = 'Edición de un Diseño'
        context['entity'] = 'Diseño'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class DisenoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Diseno
    template_name = 'diseno/delete.html'
    success_url = reverse_lazy('erp:diseno_list')
    permission_required = 'delete_diseno'
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de un Diseño'
        context['entity'] = 'Diseño'
        context['list_url'] = self.success_url
        return context
