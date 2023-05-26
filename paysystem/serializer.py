from rest_framework import serializers
from .models import Task, Usuario, Transaccion
from django.contrib.auth import authenticate
from rest_framework.response import Response


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'done') 

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('user', 'contrasena', 'dinero')


class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usuario
		fields = ('user', 'contrasena')
	def create(self, clean_data):
		user_obj = Usuario.objects.create_user(user=clean_data['user'], contrasena=clean_data['contrasena'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	userdb = serializers.CharField()
	contrasenadb = serializers.CharField()
	def check_user(self, clean_data):
		usercheck = authenticate(user=clean_data['user'], contrasena=clean_data['contrasena'])
		if not usercheck:
			raise Response('user not found')
		return usercheck

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = ('id', 'fecha', 'total', 'estado')
        