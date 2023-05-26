from rest_framework import viewsets, status, permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializer import TaskSerializer, UsuarioSerializer, TransaccionSerializer, UserLoginSerializer, UserRegisterSerializer
from .models import Task, Usuario, Transaccion
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, HttpResponseRedirect
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




#########################
@api_view(['POST'])
def UserRegister (request):
     usr_entrante = request.data['user']
     pass_entrante = request.data['contrasena']
     try:
        newuser = Usuario(user=usr_entrante, contrasena=pass_entrante)
        newuser.save()
        return redirect('/perfil/')
        #return Response({'message':'Usuario creado'}, status=status.HTTP_200_OK)
     except:
        return Response({'message':'No se pudo crear el usuario, revise bien los campos'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def UserLogin(request):
    usr_entrante = request.data['user']
    passw_entrante = request.data['contrasena']
    print(request.data)
    try:
        usr_encontrado = Usuario.objects.get(user = usr_entrante)
        print(usr_encontrado)
        passw_encontrada = usr_encontrado.contrasena
        if(passw_encontrada == passw_entrante):
            request.session['usuario'] = usr_encontrado.user
            return HttpResponseRedirect('/perfil/', {'user': usr_encontrado.user})
        else: 
            return Response({'message':'Información errónea, intente nuevamente'},status=status.HTTP_400_BAD_REQUEST)
    except:#cambiar el usuario buscado no existe a info erronea por seguridad
        return Response({'messaje':'El usuario buscado no existe en nuestros registros'},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def UserLogout(request):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	logout(request)
	return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserView(request):
    usuario = request.user
    serializer = UsuarioSerializer(usuario)
    return Response({'user': serializer.data}, status=status.HTTP_200_OK)

########################

def homeApi(request):
    return render(request, 'indexAPI.html')

def registerview(request):
      return render(request, 'Register.html')

def loginview(request):
	return render(request, 'Login.html')

def perfilview(request):
    usuario = request.session['usuario']
    usr_encontrado = Usuario.objects.get(user = usuario)
    dinero_usuario = usr_encontrado.dinero
    print(usr_encontrado)
    return render(request, 'Perfil.html', {'user': usr_encontrado.user, 'dinero': dinero_usuario})

def saludo(request):
    url = 'http://192.168.137.1:5000/api/v1/test/saludo'
    response = requests.get(url)
    content = response.json()

    print(content['message'])
    return HttpResponse(content)