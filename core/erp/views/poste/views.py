from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import PosteForm, PosteFormEdit
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Poste


class PosteListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Poste
    template_name = 'poste/list.html'
    permission_required = 'view_poste'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Poste.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Poste'
        context['create_url'] = reverse_lazy('erp:poste_create')
        context['list_url'] = reverse_lazy('erp:poste_list')
        context['entity'] = 'Postes'
        return context


class PosteCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Poste
    form_class = PosteForm
    template_name = 'poste/create.html'
    success_url = reverse_lazy('erp:poste_list')
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
        context['title'] = 'Creación de un poste'
        context['entity'] = 'Postes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PosteUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Poste
    form_class = PosteFormEdit
    template_name = 'poste/create.html'
    success_url = reverse_lazy('erp:poste_list')
    permission_required = 'change_poste'
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
        context['title'] = 'Edición de un Poste'
        context['entity'] = 'Poste'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PosteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Poste
    template_name = 'poste/delete.html'
    success_url = reverse_lazy('erp:poste_list')
    permission_required = 'delete_poste'
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
        context['title'] = 'Eliminación de un Poste'
        context['entity'] = 'Poste'
        context['list_url'] = self.success_url
        return context
