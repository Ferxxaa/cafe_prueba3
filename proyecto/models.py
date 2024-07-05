from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django


class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=32)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen = models.ImageField(upload_to='productos/', default='img/default.jpg')
    

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.usuario.username} - Producto: {self.producto.nombre}"
    
class Cliente(models.Model):
    nombre_usuario = models.CharField(max_length=100, default='usuario_temporal')
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(default='temporal@example.com')
    contraseña = models.CharField(max_length=100, default='valor_por_defecto')  # Considera usar un campo más seguro para contraseñas en producción

    def __str__(self):
        return self.nombre_usuario