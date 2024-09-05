from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Plantilla,Renglon, Registro
from  .forms import RenglonForm, RegistroForm
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.db.models import F
from datetime import datetime, date
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from django.conf import settings

@login_required
def ListaPlantilla(request):
    Lista=Renglon.objects.filter().order_by('dia')
    data={
        'lista':Lista,
    }
    return render(request,'ListaPlantilla.html',data)

@login_required
def addRenglonPlantilla(request):
    renglon_form= RenglonForm()

    if request.method == 'POST':
        renglon_form = RenglonForm(data=request.POST)
        if renglon_form.is_valid():
            renglon_form.save()
        return redirect(reverse('ListaPlantilla'))

    data={
        'formulario':renglon_form,
    }
    return render(request, 'addRenglon.html',data)


@login_required
def addRegistro(request,anio, mes):
    #asigno el dia 1 del mes al que se está por agregar el registro
    registro_form= RegistroForm(initial={'fecha': date(anio,mes,1)})
    if request.method == 'POST':
        registro_form = RegistroForm(data=request.POST)
        if registro_form.is_valid():
            registro_form.save()
        return redirect(reverse('Pagos', args=[anio, mes]))

    data={
        'anio':anio,
        'mes':mes,
        'formulario':registro_form,
    }
    return render(request, 'addRegistro.html',data)


@login_required
def editRenglonPlantilla(request, id):

    miRenglon = Renglon.objects.get(id=id)

    if request.method == 'POST':
        if 'btnBorrar' in request.POST:
            miRenglon.delete()
        else:
            renglon_form = RenglonForm(data=request.POST, instance=miRenglon)
            if renglon_form.is_valid():
                renglon_form.save()

        return redirect(reverse('ListaPlantilla'))
    else:
        renglon_form = RenglonForm(instance=miRenglon)

    data={
        'formulario':renglon_form,
        'borrar':True,
    }
    return render(request, 'editRenglon.html',data)


@login_required
def editRegistro(request, id):

    miRegistro = Registro.objects.get(id=id)
    #guardo la fecha para volver a la página de pago desde donde se llamó al registro 
    fecha=miRegistro.fecha
    pagado=miRegistro.pagado
    if request.method == 'POST':
        if 'btnBorrar' in request.POST:
            miRegistro.delete()
        elif 'btnPagar' in request.POST:
            registro_form = RegistroForm(data=request.POST, instance=miRegistro)
            if registro_form.is_valid():
                miRegistro.pagado = not miRegistro.pagado
                registro_form.save()
        else:
            registro_form = RegistroForm(data=request.POST, instance=miRegistro)
            if registro_form.is_valid():
                registro_form.save()

        return redirect(reverse('Pagos', args=[fecha.year, fecha.month]))
    else:
        registro_form = RegistroForm(instance=miRegistro)

    data={
        'formulario':registro_form,
        'pagado':pagado,
        'borrar':True,
    }
    return render(request, 'editRegistro.html',data)



@login_required
def CopiarRegistros(request,anio,mes):
    print("Año:",anio, " Mes:",mes)
    #Obtengo los meses ya generados
    lista = Registro.objects.annotate(
        year=ExtractYear('fecha'),
        month=ExtractMonth('fecha')
    )

    mesesexistentes= lista.values('year', 'month').distinct()
    listameses=[]

    for li in mesesexistentes:
        listameses.append(str(li['year'])+"-"+str(li['month']))

    if request.method == 'POST':
        messelect = request.POST.get("meses").split('-')
        registros= lista.filter(year=messelect[0], month=messelect[1])
        print(registros)
        for r in registros:
            reg=Registro()
            reg.plantilla=r.plantilla
            reg.descripcion=r.descripcion
            reg.monto=r.monto
            reg.fecha=date(anio,mes,r.fecha.day)
            reg.save()
        return redirect(reverse('Pagos', args=[anio,mes])) 

    data={
        'listameses':listameses,
        'mes':mes, 
        'anio':anio,
    }    
    return render(request,'CopiarRegistros.html',data)



@login_required
def generarMes(request):

    mesgenerado=False
    noexsite=False

    hoy=datetime.now()
    # Calcular el próximo mes
    prox_mes = hoy.replace(month=hoy.month + 1)

    # Manejar el caso de año nuevo
    if prox_mes.month == 1:
        prox_mes = prox_mes.replace(year=prox_mes.year + 1)

    #Obtengo los meses ya generados
    lista = Registro.objects.annotate(
        year=ExtractYear('fecha'),
        month=ExtractMonth('fecha')
    )

    #Verifico si proximo mes ya está generado
    existe= lista.filter(year=prox_mes.year, month=prox_mes.month)
    if existe.exists():
        noexsite=True

    renglones={}
    if request.method == 'POST':
        if 'btnPlantilla' in request.POST:
            renglones=Renglon.objects.filter().order_by('dia')
        elif'btnMes' in request.POST:
            renglones=Registro.objects.annotate(
                plantilla=F('plantilla'),
                descripcion=F('descripcion'),
                dia=ExtractDay('fecha'),
                monto=F('monto')                
            ).filter(fecha__month=hoy.month, fecha__year=hoy.year).order_by('dia')
        
        for r in renglones:
            reg=Registro()
            reg.plantilla=r.plantilla
            reg.descripcion=r.descripcion
            reg.monto=r.monto
            reg.fecha=prox_mes.replace(day=r.dia)
            reg.save()
            mesgenerado=True


    # Obtener los valores únicos de año y mes
    registros_unicos = lista.values('year', 'month').distinct()
    data={
        'lista':registros_unicos,
        'proximo':prox_mes.strftime("%B %Y"), # FEcha en formato 'Enero 2024'
        'generado':mesgenerado,
        'noexiste':noexsite
    }    
    return render(request,'generarMes.html',data)


def Mes(mes):
    if mes==1: return "Enero"
    if mes==2: return "Febrero"
    if mes==3: return "Marzo"
    if mes==4: return "Abril"
    if mes==5: return "Mayo"
    if mes==6: return "Junio"
    if mes==7: return "Julio"
    if mes==8: return "Agosto"
    if mes==9: return "Setiembre"
    if mes==10: return "Octubre"
    if mes==11: return "Noviembre"
    if mes==11: return "Diciembre"


@login_required
def Calendario(request):
    Hoy= now().date()
    year = Hoy.year
    month = Hoy.month
    return render(request,'calendario.html') 

@login_required
def PagosPrincipal(request):
    Hoy= now().date()
    year = Hoy.year
    month = Hoy.month
    return redirect(reverse('Pagos', args=[year, month]))


@login_required
def Pagos(request,anio,mes): 
    estaticos= str(settings.STATIC_ROOT)
    print("RECIBE: ",anio,"-", mes)
    plantillas = Plantilla.objects.all()
    registros = Registro.objects.filter(fecha__month=mes, fecha__year=anio).order_by('pagado','fecha')

    # Añadir el campo "Estado" dinámicamente
    for registro in registros:
        if registro.pagado:
            registro.estado = "2" #PAGADO
        else:
            dias = (registro.fecha - now().date()).days
            if dias >= 3:
                registro.estado = "0" #PENDIENTE
            elif dias > 0 and dias < 3:
                registro.estado = "1" #POR VENCER
            else:     
                registro.estado = "3" #VENCIDO

    Total=0
    Pagado=0
    Falta=0
    for reg in registros:
        Total = Total+reg.monto
        if reg.pagado:
            Pagado=Pagado+reg.monto
    Falta=Total-Pagado 
    pagosde=Mes(mes)+" "+str(anio) 
    data={
        'plantillas':plantillas,
        'registros':registros,
        'total':Total,
        'pagado':Pagado,
        'falta': Falta,
        'pagosde':pagosde,
        'anio':anio,
        'mes':mes,
        'estaticos':estaticos,
    }
    return render(request,'pagos.html',data) 