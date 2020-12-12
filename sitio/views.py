from django.contrib.auth import logout as do_logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django import http
from .models import *
from django.forms.models import model_to_dict
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
import datetime
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def updateRequest(request):
    recibidos = Pedido.objects.filter(id_estado=1)
    enproceso = Pedido.objects.filter(id_estado=2)
    finalizados = Pedido.objects.filter(id_estado=3)
    pagados = Pedido.objects.filter(id_estado=4)
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
            'Observacion':row2.Observacion,'Producto':row2.id_producto.Nombre})
        lista_recibidos.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha})
    for row in enproceso:
        detalles= Detalle_Pedido.objects.filter(id_pedido=row.id_pedido)
        detalle=[]
        for row2 in detalles:
            detalle.append({'Cantidad':row2.Cantidad,'Precio':row2.Precio,
            'Observacion':row2.Observacion,'Producto':row2.id_producto.Nombre})
        lista_enproceso.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha})
    for row in finalizados:
        detalles= Detalle_Pedido.objects.filter(id_pedido=row.id_pedido)
        detalle=[]
        for row2 in detalles:
            detalle.append({'Cantidad':row2.Cantidad,'Precio':row2.Precio,
            'Observacion':row2.Observacion,'Producto':row2.id_producto.Nombre})
        lista_finalizados.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha})
    for row in pagados:
        detalles= Detalle_Pedido.objects.filter(id_pedido=row.id_pedido)
        detalle=[]
        for row2 in detalles:
            detalle.append({'Cantidad':row2.Cantidad,'Precio':row2.Precio,
            'Observacion':row2.Observacion,'Producto':row2.id_producto.Nombre})
        lista_pagados.append({'id_pedido':row.id_pedido, 'Detalle_pedido':detalle,'Fecha':row.Fecha})
    pedidos= {'recibidos':lista_recibidos,'enproceso':lista_enproceso, 'finalizados':lista_finalizados,'pagados':lista_pagados}
    list_json = json.dumps(pedidos,default=myconverter) #dump list as JSON
    return JsonResponse(pedidos,safe=False)


def index(request):
    return render(request, 'sitio/index.html')

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