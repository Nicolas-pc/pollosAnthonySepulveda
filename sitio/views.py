from django.contrib.auth import logout as do_logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django import http
from .models import *
from django.forms.models import model_to_dict
from django.forms import formset_factory
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import datetime
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
def changeState(request):
    print(Pedido.objects.filter(pk=request.GET.get('req')))
    actualestado=Pedido.objects.get(pk=request.GET.get('req')).id_estado.pk
    if(actualestado<4):
        Pedido.objects.filter(pk=request.GET.get('req')).update(id_estado=actualestado+1)
    return HttpResponse('listo')

def updateRequest(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    recibidos = Pedido.objects.filter(id_estado=1
    ,Fecha__range=(today_min, today_max)
    )
    enproceso = Pedido.objects.filter(id_estado=2
    ,Fecha__range=(today_min, today_max)
    )
    finalizados = Pedido.objects.filter(id_estado=3,Fecha__range=(today_min, today_max)
    )
    pagados = Pedido.objects.filter(id_estado=4,Fecha__range=(today_min, today_max)
    )
    pedidos = []
    lista_recibidos = []
    lista_enproceso = []
    lista_finalizados = []
    lista_pagados = []
    for row in recibidos:
        detalles= Detalle_Pedido.objects.filter(id_pedido=row.id_pedido)
        detalle=[]
        for row2 in detalles:
            detalle.append({'Cantidad':row2.Cantidad,'Precio':row2.Precio,
            'Producto':row2.id_producto.Nombre})
        lista_recibidos.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha,
        'Cliente':row.id_cliente.Nombres+' '+row.id_cliente.Primer_Apellido,'Telefono':row.id_cliente.Telefono,
        'Direccion':row.id_cliente.Direccion})
    for row in enproceso:
        detalles= Detalle_Pedido.objects.filter(id_pedido=row.id_pedido)
        detalle=[]
        for row2 in detalles:
            detalle.append({'Cantidad':row2.Cantidad,'Precio':row2.Precio,'Producto':row2.id_producto.Nombre})
        lista_enproceso.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha,
        'Cliente':row.id_cliente.Nombres+' '+row.id_cliente.Primer_Apellido,'Telefono':row.id_cliente.Telefono,
        'Direccion':row.id_cliente.Direccion})
    for row in finalizados:
        detalles= Detalle_Pedido.objects.filter(id_pedido=row.id_pedido)
        detalle=[]
        for row2 in detalles:
            detalle.append({'Cantidad':row2.Cantidad,'Precio':row2.Precio,
            'Producto':row2.id_producto.Nombre})
        lista_finalizados.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha,
        'Cliente':row.id_cliente.Nombres+' '+row.id_cliente.Primer_Apellido,'Telefono':row.id_cliente.Telefono,
        'Direccion':row.id_cliente.Direccion})
    for row in pagados:
        detalles= Detalle_Pedido.objects.filter(id_pedido=row.id_pedido)
        detalle=[]
        for row2 in detalles:
            detalle.append({'Cantidad':row2.Cantidad,'Precio':row2.Precio,
            'Producto':row2.id_producto.Nombre})
        lista_pagados.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha,
        'Cliente':row.id_cliente.Nombres+' '+row.id_cliente.Primer_Apellido,'Telefono':row.id_cliente.Telefono,
        'Direccion':row.id_cliente.Direccion})
    pedidos= {'recibidos':lista_recibidos,'enproceso':lista_enproceso, 'finalizados':lista_finalizados,'pagados':lista_pagados}
    list_json = json.dumps(pedidos,default=myconverter) #dump list as JSON
    return JsonResponse(pedidos,safe=False)

def success(request):
    return render(request, 'sitio/success.html')
def index(request):
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = DetallePedidoFormset(queryset=Detalle_Pedido.objects.none())
        formDatos = ClienteForm()
    elif request.method == 'POST':
        formDatos = ClienteForm(request.POST)
        formset = DetallePedidoFormset(request.POST)
        if formset.is_valid() and formDatos.is_valid():
            aux = formDatos.save()
            recibido = Estado.objects.get(pk=1)
            miPedido = Pedido(id_cliente=aux,id_estado=recibido,Fecha=datetime.datetime.today())
            miPedido.save()
            print(miPedido)
            for form in formset:
                # only save if name is present
                if form.cleaned_data.get('id_producto'):
                    aux2 = form.save(commit=False)
                    aux2.id_pedido= miPedido
                    aux2.save()
            return redirect('/success')
    context = {
        'images':Images.objects.all(),
        'formset':formset,
        'formDatos':formDatos
    }
    return render(request, 'sitio/index.html',context)

def welcome(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PedidoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            form = PedidoForm()
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PedidoForm()
 
    context = { 
        'Pedidos_recibidos':Pedido.objects.filter(id_estado=1),
        'Pedidos_en_proceso':Pedido.objects.filter(id_estado=2),
        'Pedidos_finalizados':Pedido.objects.filter(id_estado=3),
        'Pedidos_pagados':Pedido.objects.filter(id_estado=4),
        'form':form
    }
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "administracion/index.html",context)
    # En otro caso redireccionamos al login
    return redirect('/admin/login')
def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/admin')

    # Si llegamos al final renderizamos el formulario
    return render(request, "administracion/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/admin')