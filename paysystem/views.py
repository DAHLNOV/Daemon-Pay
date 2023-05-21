from rest_framework import viewsets
from django.contrib.auth import authenticate, login
from .serializer import TaskSerializer, UsuarioSerializer, TransaccionSerializer
from .models import Task, Usuario, Transaccion
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import requests

# Create your views here.

class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

class TransaccionView(viewsets.ModelViewSet):
    serializer_class = TransaccionSerializer
    queryset = Transaccion.objects.all()


@api_view(['POST'])
def login_view(request):
    serializer = UsuarioSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['user']
    password = serializer.validated_data['contrasena']

    user = Usuario.objects.get(user=username)

    if user.check_password(password):
        login(request, user)
        return Response({'message': 'Inicio de sesión exitoso.'}, status=200)
    else:
        return Response({'error': 'Credenciales de inicio de sesión inválidas.'}, status=400)


def homeApi(request):
    return render(request, 'indexAPI.html')

def saludo(request):
    url = 'http://192.168.137.1:5000/api/v1/test/saludo'
    response = requests.get(url)
    content = response.json()

    print(content['message'])
    return HttpResponse(content)