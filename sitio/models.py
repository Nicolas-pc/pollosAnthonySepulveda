from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
import os
import cloudinary.uploader
from django.forms import modelformset_factory
from django import forms
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Archivo no soportado, solo se admiten archivos .pdf')

# Create your models here.

class Cliente(models.Model): 
    id_cliente = models.AutoField(primary_key=True)
    Nombres = models.CharField(max_length = 50)
    Primer_Apellido = models.CharField(max_length= 30)
    Segundo_Apellido = models.CharField(max_length= 30,blank=True)
    Direccion = models.CharField(max_length= 100,verbose_name='Dirección')
    Telefono = models.CharField(max_length= 12,verbose_name='Teléfono')
    CorreoElectronico = models.CharField(max_length= 100,verbose_name='Correo Electrónico')
    def __str__(self):
        return str(self.Nombres+' '+self.Primer_Apellido+' '+self.Segundo_Apellido)
 
    def save(self,*args, **kwargs):
        super(Cliente, self).save(*args, **kwargs)
        


class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length = 20,verbose_name='nombre de Estado')
    def __str__(self):
        return self.Nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length = 50)
    Precio = models.PositiveIntegerField()
    def __str__(self):
        return self.Nombre+' $'+str(self.Precio)
    def __unicode__(self):
        return u'id_producto: %s, Nombre - %s, Precio - %s' % (str(self.id_producto), self.Nombre, self.Precio)
    def get_Precio(self):
        return Precio

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,verbose_name='Cliente')
    Fecha = models.DateTimeField()
    id_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    def __str__(self):
        return 'Numero de Pedido: '+str(self.id_pedido)

class Detalle_Pedido(models.Model): 
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE,verbose_name='Numero de pedido')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE,verbose_name='Producto')
    Cantidad = models.PositiveIntegerField(default=1)
    Precio = models.PositiveIntegerField(editable=False)
    def __str__(self):
        return 'Pedido N°'+str(self.id_pedido.id_pedido)+': Detalle N°'+str(self.id_detalle_pedido)
    def save(self,*args, **kwargs ):
        self.Precio=self.id_producto.Precio
        super(Detalle_Pedido, self).save(*args, **kwargs)

class Menu(models.Model):
    id = models.AutoField(primary_key=True, default=1)
    pdf = models.FileField(validators=[validate_file_extension],upload_to='uploads',verbose_name='Archivo con Menu')
    def save(self, *args, **kwargs):
        if Menu.objects.count() == 1:
            Menu.objects.first().delete()
        super(Menu, self).save(*args, **kwargs)
    def __str__(self):
            return self.pdf.name

class Images(models.Model):
    id = models.AutoField(primary_key=True)
    
    Image = CloudinaryField('Image')
    def __str__(self):
            return str(self.id)
    class Meta:
        verbose_name_plural ='imagenes'

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombres', 'Primer_Apellido', 'Segundo_Apellido','Direccion','Telefono','CorreoElectronico']
        widgets={'Nombres': forms.TextInput(attrs={
            'class': 'form-control',
        }),
        'Primer_Apellido': forms.TextInput(attrs={
            'class': 'form-control',
        }),
        'Segundo_Apellido': forms.TextInput(attrs={
            'class': 'form-control',
        }),
        'Direccion': forms.TextInput(attrs={
            'class': 'form-control',
        }),
        'Telefono': forms.TextInput(attrs={
            'class': 'form-control',
        }),
        'CorreoElectronico': forms.TextInput(attrs={
            'class': 'form-control',
        }),

    }
    

class Detalle_PedidoForm(ModelForm):
    class Meta:
        model = Detalle_Pedido
        fields = ['id_pedido','id_producto','Cantidad']


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['id_cliente','Fecha','id_estado']

DetallePedidoFormset = modelformset_factory(
    Detalle_Pedido,
    fields=('id_producto','Cantidad'),
    extra=1,
    
    widgets={'Cantidad': forms.Select(attrs={
            'class': 'form-control row-pedido',
        },choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'))),
        'id_producto': forms.Select(attrs={
            'class': 'form-control row-pedido',
        })
    }
)

class Tablero(Pedido):
    class Meta:
        proxy = True
        verbose_name = 'Tablero'
        verbose_name_plural = 'Tablero de pedidos'

@receiver(models.signals.post_delete, sender=Images)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print(instance.Image.public_id)
    if instance.Image:
        cloudinary.uploader.destroy(instance.Image.public_id,invalidate=True)
