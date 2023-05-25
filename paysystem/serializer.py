from rest_framework import serializers
from .models import Task, Usuario, Transaccion


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'done') 

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('user', 'contrasena', 'dinero')

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = ('id', 'fecha', 'total', 'estado')
        