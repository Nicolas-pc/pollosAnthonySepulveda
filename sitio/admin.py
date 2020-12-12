from django.contrib import admin
from .models import Cliente, Menu,Pedido,Detalle_Pedido,Producto,Observacion,Estado,Tablero
class DetallePedidoInline(admin.TabularInline):
    extra = 0
    model = Detalle_Pedido

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        DetallePedidoInline,
    ]
# Register your models here.
admin.site.site_header = 'Administración de pollos de anthony Sepulveda'

admin.site.register(Cliente)
admin.site.register(Pedido,PedidoAdmin)
admin.site.register(Estado)
admin.site.register(Producto)
admin.site.register(Menu)
admin.site.register(Observacion)
@admin.register(Tablero)
class TableroAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self,request):
        return False
    change_list_template = 'admin/Tablero_change_list.html'
    


