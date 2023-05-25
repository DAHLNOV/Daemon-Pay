from rest_framework import viewsets, status
from django.contrib.auth import authenticate, login
from .serializer import TaskSerializer, UsuarioSerializer, TransaccionSerializer
from .models import Task, Usuario, Transaccion
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import requests
from django.views.decorators.csrf import csrf_exempt

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

# def transaccion_dinero(request, usuario_id):
#     usuario_origen = get_object_or_404(Usuario, pk=request.user.id)
#     usuario_destino = get_object_or_404(Usuario, pk=usuario_id)

#     if request.method == 'POST':
#         total_transferencia = int(request.POST.get('total'))

#         if usuario_origen.dinero >= total_transferencia:
#             usuario_origen.dinero -= total_transferencia
#             usuario_destino.dinero += total_transferencia

#             usuario_origen.save()
#             usuario_destino.save()

#             return HttpResponseRedirect('/ruta-de-destino/')
#         else:
#             error_message = 'No tienes suficiente dinero para realizar la transferencia.'

#     return render(request, 'transferencia.html', {'usuario_destino': usuario_destino, 'error_message': error_message})

@csrf_exempt
def transferencia_view(request):
    if request.method == 'POST':
        usuario_origen_nombre = request.POST.get('usuario-origen')
        usuario_destino_nombre = request.POST.get('usuario-destino')
        total = int(request.POST.get('total'))

        # Verificar si los usuarios existen
        try:
            usuario_origen = Usuario.objects.get(user=usuario_origen_nombre)
            usuario_destino = Usuario.objects.get(user=usuario_destino_nombre)
        except Usuario.DoesNotExist:
            return HttpResponse('Los usuarios especificados no existen')
        # Verificar si el usuario origen tiene suficientes fondos
        if usuario_origen.saldo < total:
            return HttpResponse('El usuario origen no tiene suficientes fondos')
        
        # Realizar la transferencia
        usuario_origen.saldo -= total
        usuario_destino.saldo += total
        usuario_origen.save()
        usuario_destino.save()

        # Crear registro de transacción
        Transaccion.objects.create(usuario_origen=usuario_origen, usuario_destino=usuario_destino, total=total, estado="Realizada")
        return HttpResponse('Transferencia realizada con éxito')

    return render(request, 'transaccion.html')


def transaccion_view(request):
    return render(request, 'transaccion.html')

def homeApi(request):
    return render(request, 'indexAPI.html')

def saludo(request):
    url = 'http://192.168.137.1:5000/api/v1/test/saludo'
    response = requests.get(url)
    content = response.json()

    print(content['message'])
    return HttpResponse(content)