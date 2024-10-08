from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import JsonResponse
from core.reports.forms import ReportForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.erp.models import Poste
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import ValidatePermissionRequiredMixin

class ReportPosteView(LoginRequiredMixin, TemplateView, ValidatePermissionRequiredMixin):
    template_name = 'postes/report.html'
    permission_required = 'view_report'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = {
                    'proyecto': {},
                    'postes': []
                }
                proyecto_id = request.POST.get('proyecto_id', '')
                search = Poste.objects.all()

                if proyecto_id:
                    search = search.filter(proyecto_id=proyecto_id)
                    # Obtenemos la información del proyecto
                    proyecto = search.first().proyecto if search.exists() else None

                    if proyecto:
                        data['proyecto'] = {
                            'name': proyecto.name,
                            'contacto': proyecto.contacto,
                            'mail': proyecto.mail,
                            'direccion': proyecto.direccion,
                            'desc': proyecto.desc
                        }

                for p in search:
                    data['postes'].append([
                        p.id,
                        p.name,
                        p.proyecto.name if p.proyecto else 'Sin proyecto',
                        p.tipo_poste.name,
                        p.tipo_cruceta.name,
                        p.tipo_abrazadera.name,
                        p.latitud,
                        p.longitud,
                    ])

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Postes'
        context['entity'] = 'Postes'
        context['list_url'] = reverse_lazy('postes_report')
        context['form'] = ReportForm()
        return context
