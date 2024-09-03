from django.urls import path
from .views import addRenglonPlantilla,ListaPlantilla,editRenglonPlantilla,generarMes,Pagos, editRegistro,PagosPrincipal,addRegistro,CopiarRegistros,Calendario

urlpatterns = [
    path('', PagosPrincipal, name="inicio"),

    path('ListaPlantilla/',ListaPlantilla, name="ListaPlantilla"),
    path('addRenglon/',addRenglonPlantilla, name="addRenglon"),
    path('editRenglonPlantilla/<int:id>',editRenglonPlantilla, name="editRenglonPlantilla"),
    path('generarMes/',generarMes, name="generarMes"),
    path('pagos/<int:anio>/<int:mes>/',Pagos, name="Pagos"),
    path('pagos/',PagosPrincipal, name="PagosPrincipal"),
    path('editRegistro/<int:id>',editRegistro, name="editRegistro"),
    path('addRegistro/<int:anio>/<int:mes>/',addRegistro, name="addRegistro"),
    path('CopiarRegistros/<int:anio>/<int:mes>/',CopiarRegistros, name="CopiarRegistros"),
    path('calendario/',Calendario, name="calendario"),

]