from rest_framework import viewsets, status, permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializer import TaskSerializer, UsuarioSerializer, TransaccionSerializer, UserLoginSerializer, UserRegisterSerializer
from .models import Task, Usuario, Transaccion
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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




#########################
@api_view(['POST'])
def UserRegister (request):
     usr_entrante = request.data['user']
     pass_entrante = request.data['contrasena']
     url = 'https://musicpro.bemtorres.win/api/v1/test/saldo'
     response = requests.get(url)
     content = response.json()
     saldo_externo = content['saldo']
     try:
        newuser = Usuario(user=usr_entrante, contrasena=pass_entrante, saldo=saldo_externo)
        newuser.save()
        return redirect('/login/')
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

@api_view(['POST'])
def transferencia_api(request):
        usuario_origen_nombre = request.data.get('usuario-origen')
        usuario_destino_nombre = request.data.get('usuario-destino')
        total = int(request.data.get('total'))

        # Verificar si los usuarios existen
        try:
            usuario_destino = Usuario.objects.get(user=usuario_destino_nombre)
        except Usuario.DoesNotExist:
            return Response({'message':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)
        # Verificar si el usuario origen tiene suficientes fondos
        
        # Realizar la transferencia
        usuario_destino.saldo += total
        usuario_destino.save()

        # Crear registro de transacción
        Transaccion.objects.create(usuario_origen=usuario_origen_nombre, usuario_destino=usuario_destino, total=total, estado="Realizada")
        return Response({'message':'Transferencia exitosa'}, status=status.HTTP_200_OK)

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

    return render(request, 'transaccion.html', {'user': usuario_origen_nombre})

def transaccion_view(request):
    return render(request, 'transaccion.html')

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
    dinero_usuario = usr_encontrado.saldo
    url = 'https://musicpro.bemtorres.win/api/v1/test/saludo'
    response = requests.get(url, timeout=10)    
    content = response.json()
    saludoentrante = content['message']
    print(usr_encontrado)
    return render(request, 'Perfil.html', {'user': usr_encontrado.user, 'saldo': dinero_usuario, 'saludo': saludoentrante})

def saludo(request):
    url = 'http://192.168.137.1:5000/api/v1/test/saludo'
    response = requests.get(url)
    content = response.json()

    print(content['message'])
    return HttpResponse(content)

def beatpayform(request):
    return render(request, 'transferir_beatpay.html')


@csrf_exempt
def beatpay(request):
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud
        tarjeta_origen = request.POST.get('tarjeta_origen')
        tarjeta_destino = request.POST.get('tarjeta_destino')
        comentario = request.POST.get('comentario')
        monto = request.POST.get('monto')
        codigo = 'DAEMON'
        token = 'DAEMON123'

        # Construir el cuerpo de la solicitud
        data = {
            'tarjeta_origen': tarjeta_origen,
            'tarjeta_destino': tarjeta_destino,
            'comentario': comentario,
            'monto': monto,
            'codigo': codigo,
            'token': token
        }

        # Realizar la solicitud POST al endpoint
        response = requests.post('https://musicpro.bemtorres.win/api/v1/tarjeta/transferir', json=data)

        # Devolver la respuesta del endpoint
        return JsonResponse(response.json())

    # La solicitud no es de tipo POST
    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)
