from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ProyectoForm, ProyectoFormEdit
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Proyecto


class ProyectoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyecto/list.html'
    permission_required = 'view_proyecto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proyecto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proyectos'
        context['create_url'] = reverse_lazy('erp:proyecto_create')
        context['list_url'] = reverse_lazy('erp:proyecto_list')
        context['entity'] = 'Proyectos'
        return context


class ProyectoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto/create.html'
    success_url = reverse_lazy('erp:proyecto_list')
    permission_required = 'add_poste'
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
        context['title'] = 'Creación de un proyecto'
        context['entity'] = 'P'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProyectoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoFormEdit
    template_name = 'proyecto/create.html'
    success_url = reverse_lazy('erp:proyecto_list')
    permission_required = 'change_proyecto'
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
        context['title'] = 'Edición de un Proyecto'
        context['entity'] = 'Proyecto'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProyectoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Proyecto
    template_name = 'proyecto/delete.html'
    success_url = reverse_lazy('erp:proyecto_list')
    permission_required = 'delete_proyecto'
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
        context['title'] = 'Eliminación de un Proyecto'
        context['entity'] = 'Proyecto'
        context['list_url'] = self.success_url
        return context
