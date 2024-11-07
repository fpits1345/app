from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from core.reports.forms import ReportForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.erp.models import Poste, Proyecto
from xhtml2pdf import pisa
from django.template.loader import render_to_string
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
                    'diseno': {},
                    'postes': [],
                    'total_postes': 0
                }
                proyecto_id = request.POST.get('proyecto_id', '')
                search = Poste.objects.all()

                if proyecto_id:
                    search = search.filter(proyecto_id=proyecto_id)
                    proyecto = search.first().proyecto if search.exists() else None

                    if proyecto:
                        data['proyecto'] = {
                            'name': proyecto.name,
                            'contacto': proyecto.contacto,
                            'mail': proyecto.mail,
                            'direccion': proyecto.direccion,
                            'desc': proyecto.adm
                        }

                        # Agregar información de diseño si existe
                        diseno = proyecto.diseno_set.first()
                        if diseno:
                            data['diseno'] = {
                                'olt': diseno.olt,
                                'odf': diseno.odf,
                                'hilo': diseno.hilo,
                                'slot': diseno.slot,
                                'pon': diseno.pon,
                                'nap8': diseno.nap8,
                                'nap16': diseno.nap16,
                                'm1': diseno.m1,
                                'm2': diseno.m2,
                                'sp8': diseno.sp8,
                                'sp16': diseno.sp16,
                                'odf1': diseno.odf1,
                                'odf2': diseno.odf2,
                                'odf3': diseno.odf3,
                                'cable4': diseno.cable4,
                                'cable8': diseno.cable8,
                                'cable12': diseno.cable12,
                                'cable24': diseno.cable24,
                                'cable48': diseno.cable48,
                                'cable96': diseno.cable96,
                                'hp': diseno.hp,
                                'obs': diseno.obs
                            }

                for p in search:
                    data['postes'].append([
                        p.id,
                        p.name,
                        p.proyecto.name if p.proyecto else 'Sin proyecto',
                        p.tipo_poste.name,
                        p.tipo_abrazadera.name,
                        p.transformador,
                        p.remate,
                        p.latitud,
                        p.longitud,
                    ])

                # Contar la cantidad total de postes
                data['total_postes'] = search.count()  # Añadir total de postes
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get(self, request, *args, **kwargs):
        if 'pdf' in request.path:
            return self.generate_pdf(request)
        return super().get(request, *args, **kwargs)

    def generate_pdf(self, request):
        proyecto_id = request.GET.get('proyecto_id')

        # Verificar si el proyecto_id es válido
        if not proyecto_id or proyecto_id == 'None':
            return HttpResponse("Error: No se ha seleccionado un proyecto válido.", status=400)

        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except Proyecto.DoesNotExist:
            return HttpResponse("Error: Proyecto no encontrado.", status=404)

        # Obtener información del diseño
        diseno = proyecto.diseno_set.first()

        # Obtener información de postes
        postes = Poste.objects.filter(proyecto_id=proyecto_id)

        # Obtener proveedores
        proveedores = proyecto.proveedor.all()  # Obtener todos los proveedores del proyecto

        # Renderizar la plantilla a un string
        context = {
            'proyecto': proyecto,
            'diseno': diseno,
            'postes': postes,
            'proveedores': proveedores,  # Pasar proveedores al contexto
            'total_postes': postes.count()  # Pasar el total de postes al contexto
        }
        html = render_to_string('postes/report_pdf.html', context)

        # Crear el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{proyecto.name}.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Postes'
        context['entity'] = 'Postes'
        context['list_url'] = reverse_lazy('postes_report')
        context['form'] = ReportForm()  
        return context
