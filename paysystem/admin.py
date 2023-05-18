from django.contrib import admin
from .models import Task, Usuario, Transaccion

# Register your models here.
admin.site.register(Task)
admin.site.register(Usuario)
admin.site.register(Transaccion)