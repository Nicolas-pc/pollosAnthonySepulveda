from django.contrib import admin
from .models import Cliente, Menu,Pedido,Detalle_Pedido,Producto,Observacion,Estado

# Register your models here.
admin.site.site_header = 'Administración de pollos de anthony Sepulveda'
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Detalle_Pedido)
admin.site.register(Estado)
admin.site.register(Producto)
admin.site.register(Menu)
admin.site.register(Observacion)
