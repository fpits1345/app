from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from crum import get_current_request


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


"""
class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('index')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())"""

from django.contrib.auth.models import Group

class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []  # Inicializar perms como una lista vacía
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('erp:dashboard')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        group_id = request.session.get('group_id')
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                perms = self.get_perms()
                for p in perms:
                    has_permission = group.permissions.filter(codename=p).exists()
                    if not has_permission:
                        messages.error(request, 'No tiene permiso para ingresar a este módulo')
                        return HttpResponseRedirect(self.get_url_redirect())

                return super().dispatch(request, *args, **kwargs)
            except Group.DoesNotExist:
                messages.error(request, 'Grupo no encontrado en la base de datos.')
        else:
            messages.error(request, 'No se encontró un grupo en la sesión.')

        return HttpResponseRedirect(self.get_url_redirect())