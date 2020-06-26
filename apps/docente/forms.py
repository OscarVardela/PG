from .models import  *
from django import forms

class ProgramaForms(forms.ModelForm):
    class Meta:
        model = programas
        fields = ['nombre','horas','creditos','imagen','costo','fecha_inicio','fecha_final','tipo']

class ModuloForms(forms.ModelForm):
    class Meta:
        model = modulos
        fields = ['nombre','id_programas','horas']

class DocenteForms(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['nombre', 'apellidos','ci','telefono','correo','sexo','fuerza', 'nacionalidad', 'imagen',
                  'curriculum','titulo', 'diplomado','maestria','doctorado','posdoctorado','id_modulos','otro']

class DocenteFormsEditar(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['nombre', 'apellidos','ci','telefono','correo','sexo','fuerza', 'nacionalidad', 'imagen',
                  'curriculum','estado_curriculum','titulo','estado_titulo', 'diplomado',
                  'maestria','estado_maestria','doctorado','posdoctorado','comentarios','id_modulos','estado']

class DocenteFormsEditarObservados(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['nombre', 'apellidos','ci','telefono','correo','sexo','fuerza', 'nacionalidad', 'imagen',
                  'curriculum','titulo', 'diplomado',
                  'maestria','doctorado','posdoctorado']

class CursanteForms(forms.ModelForm):
    class Meta:
        model = Cursante
        fields = ['nombre', 'apellidos', 'telefono', 'ci', 'sexo','fuerza', 'correo', 'nacionalidad', 'imagen',
                  'titulo', 'solicitud', 'curriculum', 'certificado', 'formulario', 'cedula', 'contrato',
                'certificado_no_adeudo', 'luzagua', 'croquis','id_programas']

class CursanteFormsEditar(forms.ModelForm):
    class Meta:
        model = Cursante
        fields = ['nombre', 'apellidos', 'telefono', 'ci', 'sexo','fuerza', 'correo', 'nacionalidad', 'imagen',
                  'titulo', 'solicitud', 'curriculum', 'certificado', 'formulario', 'cedula', 'contrato',
                  'comprobante', 'certificado_no_adeudo', 'luzagua', 'croquis',
                  'id_programas']

class CursanteBaucher(forms.ModelForm):
    class Meta:
        model = Cursante
        fields = ['comprobante']

class CursanteDocumentosObservados(forms.ModelForm):
    class Meta:
        model = Cursante
        fields = ['documento_observado','estado_titulo','estado_certificado','estado_formulario','estado_cedula','estado_contrato','estado_comprobante','estado_no_adeudo']

class DocenteDocumentosObservados(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['documento_observado','estado_titulo','estado_curriculum','estado_maestria']

class consultaForms(forms.ModelForm):
    class Meta:
        model = docente
        fields = ['comentarios']

class ImageForm(forms.ModelForm):
   class Meta:
      model = Image
      fields = ['image','name']

class DocumentosForms(forms.ModelForm):
    class Meta:
        model = interno
        fields = ['nombre','detalle','documento','area']
