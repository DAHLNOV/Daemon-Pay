from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Usuario(models.Model):
    user = models.CharField(primary_key=True, max_length=255, verbose_name='usuario')
    contrasena = models.CharField(max_length=20)
    saldo = models.IntegerField(default=50000)

    def __str__(self):
        return self.user

class Transaccion(models.Model):
    nrotransaccion = models.AutoField(primary_key=True, verbose_name='nro de transaccion')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    estado = models.CharField(max_length=32, null=False,blank=False,default='esperando', verbose_name='estado')
    usuario_origen = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarioOrigen')
    usuario_destino = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarioDestinatario')

    def __str__(self):
        return self.nrotransaccion