from rest_framework import viewsets, status
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
    usr_entrante = request.data['user']
    passw_entrante = request.data['contrasena']
    try:
        usr_encontrado = Usuario.objects.get(user = usr_entrante)
        passw_encontrada = usr_encontrado.contrasena
        if(passw_encontrada == passw_entrante):
            return Response({'message':'ok'}, status=status.HTTP_200_OK)
        else: 
            return Response({'message':'Información errónea, intente nuevamente'},status=status.HTTP_400_BAD_REQUEST)
    except:#cambiar el usuario buscado no existe a info erronea por seguridad
        return Response({'messaje':'El usuario buscado no existe en nuestros registros'},status=status.HTTP_404_NOT_FOUND)


def homeApi(request):
    return render(request, 'indexAPI.html')

def saludo(request):
    url = 'http://192.168.137.1:5000/api/v1/test/saludo'
    response = requests.get(url)
    content = response.json()

    print(content['message'])
    return HttpResponse(content)