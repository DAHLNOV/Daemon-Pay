from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Usuario(models.Model):
    correo = models.EmailField(primary_key=True, verbose_name='correo')
    user = models.CharField(max_length=255, verbose_name='usuarios')
    contrasena = models.CharField(max_length=20)
    dinero = models.IntegerField(default=0,max_length=10)

    def __str__(self):
        return self.user

class Transaccion(models.Model):
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE,default='defaultUser', related_name='usuario', verbose_name='usuario')
    id = models.AutoField(primary_key=True, verbose_name='idTransaccion')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(max_length=10)
    estado = models.CharField(max_length=32, null=False,blank=False,default='esperando', verbose_name='estado')
    target = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tarjeta.numero} - ${self.monto} - {self.fecha}'