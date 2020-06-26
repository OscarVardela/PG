from django.contrib import admin

# Register your models here.
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class docenteResource(resources.ModelResource):
    class Meta:
        model = docentes

class docenteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre','apellidos','estado','imagen','actual',)
    resource_class = docenteResource

admin.site.register(docentes,docenteAdmin)
admin.site.register(File)
admin.site.register(Serie)
