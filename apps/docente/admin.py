from django.contrib import admin
from .models import *

# Register your models here.

from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class docenteResource(resources.ModelResource):
    class Meta:
        model = docente

#class buscarDocenteAdmin(admin.ModelAdmin):
#    search_fields = ['nombre']

class docenteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre','apellidos','estado','imagen','actual',)
    resource_class = docenteResource

admin.site.register(docente,docenteAdmin)
admin.site.register(codigo)
admin.site.register(programas)
admin.site.register(Cursante)
admin.site.register(modulos)
admin.site.register(interno)
