from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.core.exceptions import *
from datetime import date
from django.shortcuts import render
from qr_code.qrcode.utils import ContactDetail, WifiConfig, Coordinates, QRCodeOptions
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.views.generic import ListView, TemplateView
import io
from io import BytesIO
#from PIL import Image
import PIL.Image
from datetime import datetime
import qrcode  # Importamos el modulo necesario para trabajar con codigos
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import *


# Create your views here.


def Principio(request):
    return render(request,'inicio.html')

def CursanteDocente(request):
    return render(request,'cursante_docente.html')

def EncuestaCursante(request):
    return render(request,'cursante_encuesta.html')

def RegistroSatisfactorio(request):
    return render(request,'satisfatorio.html')

def registroDelCursante(request):
    if request.method == 'POST':
        form = CursanteForms(request.POST, request.FILES)
        if form.is_valid():
            Cursante = form.save(commit=False)
            Cursante.id_usuario = (request.user)

            form.save()
        return redirect('RegistroSatisfactorio')
    else:
        form = CursanteForms()
    return render(request,'registro_del_cursante.html', {'form':form})

def registroDelDocente(request):
    if request.method == 'POST':
        form = DocenteForms(request.POST, request.FILES)
        if form.is_valid():
            docente = form.save(commit=False)
            docente.id_usuario = (request.user)

            form.save()
        return redirect('RegistroSatisfactorio')
    else:
        form = DocenteForms()
    return render(request,'registro_del_docente.html', {'form':form})

def registroDocInterno(request):
    if request.method == 'POST':
        form = DocumentosForms(request.POST, request.FILES)
        if form.is_valid():
            interno = form.save(commit=False)
            interno.remitente = request.user
            form.save()
        return redirect('index')
    else:
        form = DocumentosForms()
    return render(request,'documentos_internos.html', {'form':form})

def EncuestaNegativaCursante(request):
    return render(request,'cursante_encuesta_negativa.html')

def EncuestaDocente(request):
    return render(request,'docente_encuesta.html')

@login_required
def registroDoc(request):
    if request.method == 'POST':
        form = DocenteForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = "Image uploaded succesfully!"
            return redirect('principio')
    else:
        form = DocenteForms()

    return render(request,'register.html', {'form':form})

def editarDocumento(request,id):
    form = None
    error = None
    try:
        Docente = docente.objects.get(id = id)
        if request.method == 'GET':
            form = DocenteFormsEditar(instance= Docente)
        else:
            form = DocenteFormsEditar(request.POST, request.FILES, instance=Docente)
            if form.is_valid():

                docentes = form.save(commit=False)


                x = (str(request.user),str(docentes.codigo_titulo),str(datetime.now()))

                imagen = qrcode.make(x)  # Creamos un codigo a partir de una cadena de texto
                img = PIL.Image.open(docentes.titulo)
                img = img.resize((2500, 2500), PIL.Image.ANTIALIAS)
                docentes.actual=datetime.now()
                img.paste(imagen, (0, 0))


                blob = BytesIO()
                img.save(blob, 'JPEG')

                y = (str(request.user),str(docentes.codigo_diplomado),str(datetime.now()))
                imagen1 = qrcode.make(y)
                img1 = PIL.Image.open(docentes.diplomado)
                img1 = img1.resize((2500, 2500), PIL.Image.ANTIALIAS)
                img1.paste(imagen1, (0, 0))
                blob1 = BytesIO()
                img1.save(blob1, 'JPEG')


                z = (str(request.user),str(docentes.codigo_maestria),str(datetime.now()))
                imagen2 = qrcode.make(z)
                img2 = PIL.Image.open(docentes.maestria)
                img2 = img2.resize((2500, 2500), PIL.Image.ANTIALIAS)
                img2.paste(imagen2, (0, 0))
                blob2 = BytesIO()
                img2.save(blob2, 'JPEG')

                docentes.titulo.save('ticket-filename.jpg', File(blob), save=False)
                docentes.diplomado.save('diplomado.jpg', File(blob1), save=False)
                docentes.maestria.save('maestria.jpg', File(blob2), save=False)

                form.save()
            return redirect('listarTodo')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'register.html',{'form':form,'error':error})

from django.core.files import File

def registroPrograma(request):
    if request.method == 'POST':
        form = ProgramaForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('listarPrograma')
    else:
        form = ProgramaForms()
    return render(request,'registrar_programa.html', {'form':form})

def registroCursante(request):
    if request.method == 'POST':
        form = CursanteForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('principio')
    else:
        form = CursanteForms()
    return render(request,'registrar_cursante.html', {'form':form})

def editarCursante(request,id):
    form = None
    error = None
    try:
        cursante = Cursante.objects.get(id = id)
        if request.method == 'GET':
            form = CursanteDocumentosObservados(instance= cursante)
        else:
            form = CursanteDocumentosObservados(request.POST, request.FILES, instance=cursante)
            if form.is_valid():
                cursante = form.save(commit=False)
                cursante.estado='APROBADO PARCIALMENTE'
                cursante.bitacora = str(request.user)
                cursante.fecha_revision = datetime.now()
                form.save()
                mail = cursante.correo
                sendemail(mail,id)
            return redirect('consultarDocumentoCursante', id = cursante.id)
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'editar_cursante.html',{'form':form,'error':error})

def cursanteAprobarParcialmente(request,id):
    cursante=Cursante.objects.get(id=id)
    if request.method=='POST':
        cursante.estado='APROBADO PARCIALMENTE'
        cursante.bitacora = str(request.user)
        cursante.fecha_revision = datetime.now()
        cursante.save()
        return redirect('listarDocInternos')
    return render(request,'aprobado_parcialmente_cursante.html',{'cursante':cursante})

def editarCursanteLog(request,id_usuario):
    form = None
    error = None
    try:
        cursante = Cursante.objects.get(id_usuario = id_usuario)
        if request.method == 'GET':
            form = CursanteForms(instance= cursante)
        else:
            form = CursanteForms(request.POST, request.FILES, instance=cursante)
            if form.is_valid():
                form.save()
            return redirect('workflowCursante1', id = cursante.id)
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'editar_cursante_logueado.html',{'form':form,'error':error})

def editarDocenteLog(request,id_usuario):
    form = None
    error = None
    try:
        cursante = docente.objects.get(id_usuario = id_usuario)
        if request.method == 'GET':
            form = DocenteFormsEditarObservados(instance= cursante)
        else:
            form = DocenteFormsEditarObservados(request.POST, request.FILES, instance=cursante)
            if form.is_valid():
                form.save()
            return redirect('workflowDocente', id = cursante.id)
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'editar_docente_observado.html',{'form':form,'error':error})

def baucherCursante(request,id_usuario):
    form = None
    error = None
    try:
        cursante = Cursante.objects.get(id_usuario = id_usuario)
        if request.method == 'GET':
            form = CursanteBaucher(instance= cursante)
        else:
            form = CursanteBaucher(request.POST, request.FILES, instance=cursante)
            if form.is_valid():
                cursante = form.save(commit=False)
                cursante.fecha_envio_baucher = datetime.now()
                form.save()
            return redirect('workflowCursante1', id = cursante.id)
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'agregarr_baucher.html',{'form':form,'error':error})

def editarDocenteEstados(request,id):
    form = None
    error = None
    try:
        cursante = docente.objects.get(id = id)
        if request.method == 'GET':
            form = DocenteDocumentosObservados(instance= cursante)
        else:
            form = DocenteDocumentosObservados(request.POST, request.FILES, instance=cursante)
            if form.is_valid():
                form.save()
            return redirect('consultarDocumento', id = cursante.id)
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'editar_cursante.html',{'form':form,'error':error})

class buscarModulo(ListView):
    model = modulos
    template_name = 'modulos_busqueda.html'
    context_object_name = 'modulos'

from  django.core import serializers

class busqueda_ajax(TemplateView):
    def get(self,request, *args, **kwargs):
        id_modulo = request.GET['id']
        Modulo = modulos.objects.filter(id_programas_id=id_modulo)
        data = serializers.serialize('json', Modulo, fields=('nombre'))
        return HttpResponse(data, 'application/json')

def registroModulo(request):
    if request.method == 'POST':
        form = ModuloForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('principio')
    else:
        form = ModuloForms()

    return render(request,'registrar_modulo.html', {'form':form})

def servicio(request):
    return render(request,'Servicios.html')

def listarTodo(request):
    docentes = docente.objects.all()
    return render(request,'listar_todo.html',{'docentes':docentes})

def listarTodoCursante(request):
    docentes = Cursante.objects.all()
    return render(request,'listar_todo_cursante.html',{'docentes':docentes})

def listarDocInternos(request):
    docentes = interno.objects.filter(estado='ACTIVO')
    return render(request,'listar_internos.html',{'docentes':docentes})

def listarDocInternosRevisado(request):
    docentes = interno.objects.filter(estado='ARCHIVADO')
    return render(request,'listar_internos_archivados.html',{'docentes':docentes})

def listarDocInternosDirector(request):
    docentes = interno.objects.filter(area='DIRECTOR',estado='ACTIVO')
    return render(request,'listar_interno_director.html',{'docentes':docentes})

def listarDocInternosCoordinador(request):
    docentes = interno.objects.filter(area='COORDINADOR GENERAL',estado='ACTIVO')
    return render(request,'listar_interno_coordinador.html',{'docentes':docentes})

def listarDocInternosEncargada(request):
    docentes = interno.objects.filter(area='ENCARGADA DE PLATAFORMA',estado='ACTIVO')
    return render(request,'listar_interno_encargada.html',{'docentes':docentes})

def listarDocInternosFacilitador(request):
    docentes = interno.objects.filter(area='FACILITADOR DE PROGRAMAS',estado='ACTIVO')
    return render(request,'listar_interno_facilitador.html',{'docentes':docentes})

def listarDocInternosFinanzas(request):
    docentes = interno.objects.filter(area='ENCARGADA DE FINANZAS',estado='ACTIVO')
    return render(request,'listar_interno_finanzas.html',{'docentes':docentes})

def listarDocInternosSecretaria(request):
    docentes = interno.objects.filter(area='SECRETARIA',estado='ACTIVO')
    return render(request,'listar_interno_secretaria.html',{'docentes':docentes})

def listarRevisado(request):
    docentes = docente.objects.filter(estado='APROBADO')
    return render(request,'listar_revisado.html',{'docentes':docentes})

def listarNoRevisado(request):
    docentes = docente.objects.filter(estado='PARA REVISAR')
    return render(request,'listar_no_revisado.html',{'docentes':docentes})

def listarDocenteAprobadoParcialmente(request):
    docentes = docente.objects.filter(estado_seleccion='DESCARTADO')
    return render(request,'listar_docente_parcialmente.html',{'docentes':docentes})

def listarDocenteAprobado(request):
    docentes = docente.objects.filter(estado_seleccion='SELECCIONADO')
    return render(request,'listar_docente_aprobado.html',{'docentes':docentes})

def listarDocenteObservado(request):
    docentes = docente.objects.filter(estado='OBSERVADO')
    return render(request,'listar_docente_observado.html',{'docentes':docentes})

def listarCursanteRevisado(request):
    cursantes = Cursante.objects.filter(estado='APROBADO FINANZAS')
    return render(request,'cursantes_no_revisados.html',{'cursantes':cursantes})

def listarCursanteObservado(request):
    cursantes = Cursante.objects.filter(estado='APROBADO')
    return render(request,'cursantes_observado.html',{'cursantes':cursantes})

def listarPrograma(request):
    #cursantes = programas.objects.filter(fecha_inicio=timezone.now())
    cursantes = programas.objects.order_by('tipo')

    count = programas.objects.all().count()
    context= {'count': count}
    #cursantes = Cursante.objects.filter(id_programas=2)
    return render(request,'programa.html',{'cursantes':cursantes} )

def listarModulo(request):
    cursantes = modulos.objects.order_by('nombre')
    return render(request,'listar_modulo.html',{'cursantes':cursantes} )

def listarDiplomado(request):
    cursantes = programas.objects.filter(tipo="DIPLOMADO")
    return render(request,'listar_diplomado.html',{'cursantes':cursantes} )

def listarMaestria(request):
    cursantes = programas.objects.filter(tipo="MAESTRIA")
    return render(request,'listar_maestria.html',{'cursantes':cursantes} )

def listarDoctorado(request):
    cursantes = programas.objects.filter(tipo="DOCTORADO")
    return render(request,'listar_doctorado.html',{'cursantes':cursantes} )

def listarPosdoctorado(request):
    cursantes = programas.objects.filter(tipo="POSDOCTORADO")
    return render(request,'listar_posdoctorado.html',{'cursantes':cursantes} )

def listarContinua(request):
    cursantes = programas.objects.filter(tipo="CURSO DE EDUCACION CONTINUA")
    return render(request,'listar_continua.html',{'cursantes':cursantes} )

def listarAprobadosParcialmente(request):
    cursantes = Cursante.objects.filter(estado='APROBADO PARCIALMENTE')
    return render(request,'listar_aprobado_parcialmente.html',{'cursantes':cursantes} )

def listarCursantesAprobados(request):
    cursantes = Cursante.objects.filter(estado='APROBADO')
    return render(request,'listar_cursante_aprobado.html',{'cursantes':cursantes} )

def listarCursantesPendiente(request):
    cursantes = Cursante.objects.filter(estado='PARA REVISAR')
    return render(request,'listar_cursante_pendiente.html',{'cursantes':cursantes} )

def listarFemeninoCursante(request,id_programas):
    cursantes = Cursante.objects.filter(id_programas = id_programas,sexo='FEMENINO')
    return render(request,'listar_femenino_cursante.html',{'cursantes':cursantes} )

def listarMasculinoCursante(request,id_programas):
    cursantes = Cursante.objects.filter(id_programas = id_programas,sexo='MASCULINO')
    return render(request,'listar_masculino_cursante.html',{'cursantes':cursantes} )

def editarDocInterno(request,id):
    docente_form = None
    error = None
    try:
        Docente = interno.objects.get(id = id)
        if request.method == 'GET':
            docente_form = DocumentosForms(instance= Docente)
        else:
            docente_form = DocumentosForms(request.POST, request.FILES, instance=Docente)

            if docente_form.is_valid():
                internos = docente_form.save(commit=False)
                usr = str(internos.receptor)
                x = [usr]
                x.append(str(request.user))
                internos.fecha_recepcion=datetime.now()
                internos.receptor=str(x)
                docente_form.save()
            return redirect('principio')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'editar_interno.html',{'docente_form':docente_form,'error':error})

def eliminarInterno(request,id):
    Interno=interno.objects.get(id=id)
    if request.method=='POST':
        Interno.delete()
        return redirect('listarDocInternos')
    return render(request,'eliminar_interno.html',{'Interno':Interno})

def eliminarProg(request,id):
    Interno=programas.objects.get(id=id)
    if request.method=='POST':
        Interno.delete()
        return redirect('listarPrograma')
    return render(request,'eliminar_prog.html',{'Interno':Interno})

def eliminarCursante(request,id):
    Interno=Cursante.objects.get(id=id)
    if request.method=='POST':
        Interno.delete()
        return redirect('listarTodoCursante')
    return render(request,'eliminar_cursantes.html',{'Interno':Interno})

def ArchivarInterno(request,id):
    Interno=interno.objects.get(id=id)
    if request.method=='POST':
        Interno.estado='ARCHIVADO'
        Interno.save()
        return redirect('listarDocInternos')
    return render(request,'archivar_interno.html',{'Interno':Interno})

def editarPrograma(request,id):
    docente_form = None
    error = None
    try:
        Docente = programas.objects.get(id = id)
        if request.method == 'GET':
            docente_form = ProgramaForms(instance= Docente)
        else:
            docente_form = ProgramaForms(request.POST, instance=Docente)
            if docente_form.is_valid():
                docente_form.save()
            return redirect('listarPrograma')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'editar_programa.html',{'docente_form':docente_form,'error':error})

def consultarPrograma(request,id_programas):
    cursantes = Cursante.objects.filter(id_programas = id_programas).order_by('apellidos')
    return render(request,'programas_cursante.html',{'cursantes':cursantes})

def consultarDocenteModulo(request,id_modulos):
    cursantes = docente.objects.filter(id_modulos = id_modulos).order_by('apellidos')
    return render(request,'postulantes_modulo.html',{'cursantes':cursantes})

def listarNoRevisadoDocentes(request):
    docentes = docente.objects.filter(estado=False)
    return render(request,'docentes_no_revisados.html',{'docentes':docentes})

def listarNoRevisadoCursantes(request):
    cursantes = Cursante.objects.filter(estado=False)
    return render(request,'cursantes_no_revisados.html',{'cursantes':cursantes})

def consultarDocumento(request,id):
    Docente = docente.objects.get(id = id)
    if request.method == 'POST':
        x = (str(request.user),str(Docente.codigo_titulo),str(datetime.now()))

        imagen = qrcode.make(x)  # Creamos un codigo a partir de una cadena de texto
        img = PIL.Image.open(Docente.titulo)
        img = img.resize((2500, 2500), PIL.Image.ANTIALIAS)
        Docente.actual=datetime.now()
        img.paste(imagen, (0, 0))

        blob = BytesIO()
        img.save(blob, 'JPEG')

        y = (str(request.user),str(Docente.codigo_diplomado),str(datetime.now()))
        imagen1 = qrcode.make(y)
        img1 = PIL.Image.open(Docente.diplomado)
        img1 = img1.resize((2500, 2500), PIL.Image.ANTIALIAS)
        img1.paste(imagen1, (0, 0))
        blob1 = BytesIO()
        img1.save(blob1, 'JPEG')

        z = (str(request.user),str(Docente.codigo_maestria),str(datetime.now()))
        imagen2 = qrcode.make(z)
        img2 = PIL.Image.open(Docente.maestria)
        img2 = img2.resize((2500, 2500), PIL.Image.ANTIALIAS)
        img2.paste(imagen2, (0, 0))
        blob2 = BytesIO()
        img2.save(blob2, 'JPEG')

        Docente.titulo.save('ticket-filename.jpg', File(blob), save=False)
        Docente.diplomado.save('diplomado.jpg', File(blob1), save=False)
        Docente.maestria.save('maestria.jpg', File(blob2), save=False)
        Docente.estado_seleccion = 'SELECCIONADO'
        Docente.estado_curriculum = 'APROBADO'
        Docente.estado_titulo = 'APROBADO'
        Docente.estado_maestria = 'APROBADO'
        Docente.estado = 'APROBADO'
        Docente.save()
        return redirect('listarTodo')
    return render(request,'consulta_doc_docente.html',{'docente':Docente})

def consultar_Doc_interno(request,id):
    Docente = interno.objects.get(id = id)
    if request.method == 'POST':
        Docente.estado = 'ARCHIVADO'
        Docente.save()
        return redirect('index')
    return render(request,'consulta_documento_interno.html',{'docente':Docente})

def docenteDescartar(request,id):
    Docente=docente.objects.get(id=id)
    if request.method=='POST':
        Docente.estado_seleccion = 'DESCARTADO'
        Docente.estado = 'OBSERVADO'
        Docente.save()
        return redirect('listarDocenteAprobadoParcialmente')
    return render(request,'descartado_docente.html',{'Docente':Docente})

def consultarDocumentoInterno(request,id):
    Docente = interno.objects.get(id = id)
    if request.method == 'POST':
        Docente.estado = False
        Docente.save()
        return redirect('principio')
    return render(request,'consulta_doc_interno.html',{'docente':Docente})

def workflowCursante(request,id):
    Docente = Cursante.objects.get(id = id)
    if request.method == 'POST':
        Docente.save()
        return redirect('consultarPrograma')
    return render(request,'workflow_cursante.html',{'docente':Docente})

def workflowCursante1(request,id):
    Docente = Cursante.objects.get(id = id)
    if request.method == 'POST':
        Docente.save()
        return redirect('consultarPrograma')
    return render(request,'workflow_cursante1.html',{'docente':Docente})

def workflowCursante1Log(request,id_usuario):
    Docente = Cursante.objects.get(id_usuario = id_usuario)
    if request.method == 'POST':
        Docente.save()
        return redirect('consultarPrograma')
    return render(request,'workflow_cursante1.html',{'docente':Docente})

def workflowDocente(request,id):
    Docente = docente.objects.get(id = id)
    if request.method == 'POST':
        Docente.save()
        return redirect('consultarPrograma')
    return render(request,'workflow_docente.html',{'docente':Docente})

def workflowDocenteLog(request,id_usuario):
    Docente = docente.objects.get(id_usuario = id_usuario)
    if request.method == 'POST':
        Docente.save()
        return redirect('consultarPrograma')
    return render(request,'workflow_docente.html',{'docente':Docente})

def consultarDocumentoCursante(request,id):
    Docente = Cursante.objects.get(id = id)
    if request.method == 'POST':

        y = (str(request.user),str(Docente.codigoS),str(datetime.now()))
        imagen1 = qrcode.make(y)
        img1 = PIL.Image.open(Docente.titulo)
        img1 = img1.resize((2500, 2500), PIL.Image.ANTIALIAS)
        img1.paste(imagen1, (0, 0))
        blob1 = BytesIO()
        img1.save(blob1, 'JPEG')
        Docente.titulo.save('titulo.jpg', File(blob1), save=False)

        Docente.estado = "APROBADO FINANZAS"
        Docente.estado_titulo = "APROBADO"
        Docente.estado_certificado = "APROBADO"
        Docente.estado_formulario = "APROBADO"
        Docente.estado_cedula = "APROBADO"
        Docente.estado_contrato = "APROBADO"
        Docente.curriculum = "APROBADO"
        Docente.solicitud = "APROBADO"
        Docente.bitacora = str(request.user)
        Docente.fecha_revision = datetime.now()
        Docente.save()
        mail = Docente.correo
        sendemailAprobadoCursante(mail,id)
        return redirect('listarCursantesPendiente')
    return render(request,'consulta_doc.html',{'docente':Docente})

def consultarDocumentoBaucher(request,id):
    Docente = Cursante.objects.get(id = id)
    if request.method == 'POST':
        x = (str(request.user),str(Docente.codigoS),str(datetime.now()))
        imagen = qrcode.make(x)  # Creamos un codigo a partir de una cadena de texto
        img = PIL.Image.open(Docente.comprobante)
        img = img.resize((2500, 2500), PIL.Image.ANTIALIAS)
        Docente.actual=datetime.now()
        img.paste(imagen, (0, 0))
        blob = BytesIO()
        img.save(blob, 'JPEG')
        Docente.comprobante.save('codigo-filename.jpg', File(blob), save=False)

        Docente.estado_comprobante = "APROBADO"
        Docente.estado = "APROBADO"
        Docente.fecha_revision_finanzas = datetime.now()
        Docente.fecha_envio_baucher = datetime.now()
        Docente.bitacora_finanzas = str(request.user)
        Docente.save()
        mail = Docente.correo
        sendemailAprobadoBaucherCursante(mail,id)
        return redirect('listarCursanteRevisado')
    return render(request,'consulta_doc_baucher.html',{'docente':Docente})

def cursanteIncompleto(request,id):
    Docente = Cursante.objects.get(id = id)
    if request.method == 'POST':
        Docente.estado = 'OBSERVADO'
        Docente.save()
        return redirect('listarCursanteObservado')
    return render(request,'cursante_incompleto.html',{'docente':Docente})

def Home(request):
    return render(request,'index.html')

def crearDocente(request):
    if request.method == 'POST':
        docente_form = DocenteForms(request.POST,request.FILES)
        if docente_form.is_valid():
            docente_form.save()
            return redirect('docente:listar_docente')
    else:
        docente_form = DocenteForms()
    return render(request,'docente/crear_docente.html',{'docente_form':docente_form})

def revisarDocente(request,id):
    docente_form = None
    error = None
    try:
        Docente = docente.objects.get(id = id)
        if request.method == 'GET':
            docente_form = DocenteForms(instance= Docente)
        else:
            docente_form = DocenteForms(request.POST, instance=Docente)
            if docente_form.is_valid():
                docente_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'revision.html',{'docente_form':docente_form,'error':error})
####

def prueba(request):
    if request.method == 'POST':
        consulta_form = consultaForms(request.POST)
        if consulta_form.is_valid():
            consulta_form.save()
            return redirect('docente:prueba_docente')
    else:
        consulta_form = consultaForms()
    return render(request,'docente/consulta.html',{'consulta_form':consulta_form})

def listarDocente(request):
    docentes = docente.objects.filter(estado=True)
    return render(request,'docente/listar_docente.html',{'docentes':docentes})

def editarDocente(request,id):
    docente_form = None
    error = None
    try:
        Docente = docente.objects.get(id = id)
        if request.method == 'GET':
            docente_form = DocenteForms(instance= Docente)
        else:
            docente_form = DocenteForms(request.POST, instance=Docente)
            if docente_form.is_valid():
                docente_form.save()
            return redirect('principio')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'docente/crear_docente.html',{'docente_form':docente_form,'error':error})

def eliminarDocente(request,id):
    Docente = docente.objects.get(id = id)
    if request.method == 'POST':
        Docente.estado = False
        Docente.save()
        return redirect('principio')
    return render(request,'docente/eliminar_docente.html',{'docente':Docente})

def consultarDocente(request,id):
    Docente = docente.objects.get(id = id)
    if request.method == 'POST':
        Docente.estado = False
        Docente.save()
        return redirect('docente:listar_docente')
    return render(request,'docente/consulta.html',{'docente':Docente})

def generales(request):
    return render(request,'generales.html')

def revisar(request):
    docentes = docente.objects.filter(estado = False)
    print(docentes)
    return render(request,'revisar.html',{'docentes':docentes})

def ReporteNoRevisados(request):
    docentes = docente.objects.filter(estado = False)
    print(docentes)
    return render(request,'consultasNoRevisados.html',{'docentes':docentes})

def consultas(request):
    docentes = docente.objects.filter(estado = True)
    return render(request,'consultas.html',{'docentes':docentes})


def registro(request): #para los QRS
    if request.method == 'POST':
        docente_form = DocenteForms(request.POST)
        if docente_form.is_valid():
            docente_form.save()
            return redirect('docente:listar_docente')
    else:
        docente_form = DocenteForms()
    return render(request,'docente/crear_docente.html',{'docente_form':docente_form})

def upload_image(request):
    if request.method == 'GET':
        return render(request, 'upload_image.html')
    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = Image(  image = form.cleaned_data["image"],
                                name = form.cleaned_data["name"]
                                )
            new_image.save()
            return HttpResponseRedirect('/gallery/image_gallery/')

def image_gallery(request):
    images = Image.objects.all()
    #print(images)
    return render(request, 'image_gallery.html', {'images': images})

###############Serializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def filee_detail(request, codigoS):
    """
    Retrieve, update or delete a serie.
    """
    try:
        file = docente.objects.get(codigoS=codigoS)
    except docente.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = docenteSerializer(file)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = docenteSerializer(file, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        file.delete()
        return HttpResponse(status=204)


def Cursante_detail(request, codigoS):
    """
    Retrieve, update or delete a serie.
    """
    try:
        file = Cursante.objects.get(codigoS=codigoS)
    except docente.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = cursanteSerializer(file)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = cursanteSerializer(file, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        file.delete()
        return HttpResponse(status=204)


#<!--{% providers_media_js %}-->

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def sendemail(mail,id):
    Docente = Cursante.objects.get(id = id)
    context = {'Docente':Docente}
    template = get_template('correo_maquetado.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'Pana Industries',
        settings.EMAIL_HOST_USER,
        [mail]
    )

def sendemailAprobadoCursante(mail,id):
    Docente = Cursante.objects.get(id = id)
    context = {'Docente':Docente}
    template = get_template('correo_maquetado_aprobado_cursante.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'Pana Industries',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()

def sendemailAprobadoBaucherCursante(mail,id):
    Docente = Cursante.objects.get(id = id)
    context = {'Docente':Docente}
    template = get_template('correo_maquetado_aprobado_cursante_baucher.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'Pana Industries',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()

def correo(request,id):
    Docente = Cursante.objects.get(id = id)
    if request.method == 'POST':
        mail = request.POST.get('mail')
        sendemail(mail,id)

    return render(request, 'correo.html', {})


def sendemaildocente(mail,id):
    Docente = docente.objects.get(id = id)
    context = {'Docente':Docente}
    template = get_template('correo_maquetado_docente.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Correo para docente',
        'Pana Industries',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()

def correodocente(request,id):
    Docente = docente.objects.get(id = id)
    if request.method == 'POST':
        #mail = str(Docente.correo)
        mail = request.POST.get('mail')
        sendemaildocente(mail,id)

    return render(request, 'correo_docente.html', {})

from .reportes import ReportePersona

def reporte_todos_cursantes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="personas.pdf"'
    r = ReportePersona()
    response.write(r.run())
    return response
