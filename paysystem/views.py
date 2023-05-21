from rest_framework import viewsets
from .serializer import TaskSerializer, UsuarioSerializer, TransaccionSerializer
from .models import Task, Usuario, Transaccion
from django.shortcuts import render, HttpResponse

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


def homeApi(request):
    return render(request, 'indexAPI.html')

def cargo(request):
    redirect('end')

