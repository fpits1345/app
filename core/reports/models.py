from django.db import models


from django.contrib.auth.models import Permission

class ReportPermission(models.Model):
    class Meta:
        permissions = [
            ("view_report", "Can view report"),
            # Agrega otros permisos personalizados según tus necesidades
        ]