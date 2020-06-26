from django.urls import path, include
from .views import *
from .api import *


urlpatterns = [
    path('inicio',Home, name= 'index'),
    path('rest', FileUploadView.as_view()),
    path('generales',generales,name = 'generales'),
    path('registro',registro,name = 'registro'),
    path('revisar',revisar,name = 'revisar'),
    path('consultas',consultas,name = 'consultas'),
    path('crear_docente/',crearDocente, name = 'crear_docente'),
    path('prueba_docente/',prueba, name = 'prueba_docente'),
    path('listar_docente/',listarDocente,name = 'listar_docente'),
    path('editar_docente/<int:id>',editarDocente,name = 'editar_docente'),
    ##Miercoles
    path('revision_docente/<int:id>',revisarDocente,name = 'revision_docente'),
    path('ReporteNoRevisados',ReporteNoRevisados,name = 'ReporteNoRevisados'),
    ###
    path('eliminar_docente/<int:id>',eliminarDocente,name= 'eliminar_docente'),
    path('consultar_docente/<int:id>',consultarDocente,name= 'consultar_docente'),

    path('upload_image/', upload_image, name='upload_image'),
    path('image_gallery/', image_gallery, name='image_gallery'),


    ##rest
    path('File', FileUploadView.as_view()),

    path('docente/<str:codigoS>',filee_detail),
    path('cursante/<str:codigoS>',Cursante_detail),


    ###ultimo
    path('principio',login_required(Principio), name= 'principio'),
    path('register',login_required(registroDoc), name= 'register'),
    path('servicio',login_required(servicio), name= 'servicio'),
    path('listarTodo',login_required(listarTodo), name= 'listarTodo'),
    path('listarRevisado',login_required(listarRevisado), name= 'listarRevisado'),
    path('listarNoRevisado',login_required(listarNoRevisado), name= 'listarNoRevisado'),
    path('consultarDocumento/<int:id>',login_required(consultarDocumento), name= 'consultarDocumento'),
    path('editarDocumento/<int:id>',login_required(editarDocumento), name= 'editarDocumento'),
    path('registroCursante',login_required(registroCursante), name= 'registroCursante'),

    path('listarNoRevisadoDocentes',login_required(listarNoRevisadoDocentes), name= 'listarNoRevisadoDocentes'),
    path('listarNoRevisadoCursantes',login_required(listarNoRevisadoCursantes), name= 'listarNoRevisadoCursantes'),
    path('registroPrograma',login_required(registroPrograma), name= 'registroPrograma'),

    path('editarCursante/<int:id>',login_required(editarCursante), name= 'editarCursante'),
    path('listarCursanteRevisado',login_required(listarCursanteRevisado), name= 'listarCursanteRevisado'),
    path('consultarDocumentoCursante/<int:id>',login_required(consultarDocumentoCursante), name= 'consultarDocumentoCursante'),
    path('registroModulo',login_required(registroModulo), name= 'registroModulo'),

    ##cursante docente
    path('CursanteDocente',login_required(CursanteDocente), name= 'CursanteDocente'),
    path('EncuestaCursante',login_required(EncuestaCursante), name= 'EncuestaCursante'),
    path('EncuestaNegativaCursante',login_required(EncuestaNegativaCursante), name= 'EncuestaNegativaCursante'),
    path('EncuestaDocente',login_required(EncuestaDocente), name= 'EncuestaDocente'),
    path('registroDelCursante',login_required(registroDelCursante), name= 'registroDelCursante'),
    path('RegistroSatisfactorio',login_required(RegistroSatisfactorio), name= 'RegistroSatisfactorio'),
    path('registroDelDocente',login_required(registroDelDocente), name= 'registroDelDocente'),
    path('registroDocInterno',login_required(registroDocInterno), name= 'registroDocInterno'),

    path('listarPrograma',login_required(listarPrograma), name= 'listarPrograma'),
    path('consultarPrograma/<int:id_programas>',login_required(consultarPrograma), name= 'consultarPrograma'),

    path('listarDocInternos',login_required(listarDocInternos), name= 'listarDocInternos'),
    path('editarDocInterno/<int:id>',login_required(editarDocInterno), name= 'editarDocInterno'),
    path('listarDiplomado',login_required(listarDiplomado), name= 'listarDiplomado'),
    path('listarMaestria',login_required(listarMaestria), name= 'listarMaestria'),
    path('listarDoctorado',login_required(listarDoctorado), name= 'listarDoctorado'),
    path('listarPosdoctorado',login_required(listarPosdoctorado), name= 'listarPosdoctorado'),
    path('listarContinua',login_required(listarContinua), name= 'listarContinua'),
    path('editarPrograma/<int:id>',login_required(editarPrograma), name= 'editarPrograma'),
    path('listarDocInternosDirector',login_required(listarDocInternosDirector), name= 'listarDocInternosDirector'),
    path('listarDocInternosCoordinador',login_required(listarDocInternosCoordinador), name= 'listarDocInternosCoordinador'),
    path('listarDocInternosEncargada',login_required(listarDocInternosEncargada), name= 'listarDocInternosEncargada'),
    path('listarDocInternosFacilitador',login_required(listarDocInternosFacilitador), name= 'listarDocInternosFacilitador'),
    path('listarDocInternosFinanzas',login_required(listarDocInternosFinanzas), name= 'listarDocInternosFinanzas'),
    path('listarDocInternosSecretaria',login_required(listarDocInternosSecretaria), name= 'listarDocInternosSecretaria'),
    path('listarDocInternosRevisado',login_required(listarDocInternosRevisado), name= 'listarDocInternosRevisado'),
    path('consultarDocumentoInterno/<int:id>',login_required(consultarDocumentoInterno), name= 'consultarDocumentoInterno'),
    path('eliminarInterno/<int:id>',login_required(eliminarInterno), name= 'eliminarInterno'),
    path('ArchivarInterno/<int:id>',login_required(ArchivarInterno), name= 'ArchivarInterno'),
    path('cursanteAprobarParcialmente/<int:id>',login_required(cursanteAprobarParcialmente), name= 'cursanteAprobarParcialmente'),
    path('listarAprobadosParcialmente',login_required(listarAprobadosParcialmente), name= 'listarAprobadosParcialmente'),
    path('listarCursantesAprobados',login_required(listarCursantesAprobados), name= 'listarCursantesAprobados'),
    path('listarCursantesPendiente',login_required(listarCursantesPendiente), name= 'listarCursantesPendiente'),
    path('cursanteIncompleto/<int:id>',login_required(cursanteIncompleto), name= 'cursanteIncompleto'),
    path('listarModulo',login_required(listarModulo), name= 'listarModulo'),
    path('consultarDocenteModulo/<int:id_modulos>',login_required(consultarDocenteModulo), name= 'consultarDocenteModulo'),
    path('workflowCursante/<int:id>',login_required(workflowCursante), name= 'workflowCursante'),

    path('usuarios/',include(('apps.usuarios.urls','usuarios'))),
    path('listarTodoCursante',login_required(listarTodoCursante), name= 'listarTodoCursante'),
    path('listarDocenteAprobadoParcialmente',login_required(listarDocenteAprobadoParcialmente), name= 'listarDocenteAprobadoParcialmente'),
    path('listarDocenteAprobado',login_required(listarDocenteAprobado), name= 'listarDocenteAprobado'),
    path('listarDocenteObservado',login_required(listarDocenteObservado), name= 'listarDocenteObservado'),
    path('listarCursanteObservado',login_required(listarCursanteObservado), name= 'listarCursanteObservado'),
    path('docenteDescartar/<int:id>',login_required(docenteDescartar), name= 'docenteDescartar'),
    path('buscarModulo',buscarModulo.as_view(),name= 'buscarModulo'),
    path('busqueda_ajax/',busqueda_ajax.as_view(),name= 'busqueda_ajax'),

    path('correo/<int:id>',login_required(correo), name= 'correo'),
    path('correodocente/<int:id>',login_required(correodocente), name= 'correodocente'),
    path('consultar_Doc_interno/<int:id>',login_required(consultar_Doc_interno), name= 'consultar_Doc_interno'),

    path('listarFemeninoCursante/<int:id_programas>',login_required(listarFemeninoCursante), name= 'listarFemeninoCursante'),
    path('listarMasculinoCursante/<int:id_programas>',login_required(listarMasculinoCursante), name= 'listarMasculinoCursante'),
    path('workflowCursante1/<int:id>',login_required(workflowCursante1), name= 'workflowCursante1'),
    path('workflowDocente/<int:id>',login_required(workflowDocente), name= 'workflowDocente'),
    path('editarDocenteEstados/<int:id>',login_required(editarDocenteEstados), name= 'editarDocenteEstados'),
    path('eliminarProg/<int:id>',login_required(eliminarProg), name= 'eliminarProg'),
    path('eliminarCursante/<int:id>',login_required(eliminarCursante), name= 'eliminarCursante'),
    path('editarCursanteLog/<int:id_usuario>',login_required(editarCursanteLog), name= 'editarCursanteLog'),

    path('reporte_todos_cursantes',login_required(reporte_todos_cursantes), name= 'reporte_todos_cursantes'),

    path('baucherCursante/<int:id_usuario>',login_required(baucherCursante), name= 'baucherCursante'),
    path('editarDocenteLog/<int:id_usuario>',login_required(editarDocenteLog), name= 'editarDocenteLog'),
    path('workflowDocenteLog/<int:id_usuario>',login_required(workflowDocenteLog), name= 'workflowDocenteLog'),
    path('workflowCursante1Log/<int:id_usuario>',login_required(workflowCursante1Log), name= 'workflowCursante1Log'),
    path('consultarDocumentoBaucher/<int:id>',login_required(consultarDocumentoBaucher), name= 'consultarDocumentoBaucher'),
]
