from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from paysystem import views
from .views import *

router = routers.DefaultRouter()
router.register(r'paysystem', views.TaskView, 'paysystem')
router.register(r'usuarios', views.UsuarioView, 'usuario')
router.register(r'transacciones', views.TransaccionView, 'usuario')

urlpatterns = [
    path('',homeApi), 
    path("api/v1/", include(router.urls)),
    path("api/v1/transferencia/", transferencia_api),
    path('docs/', include_docs_urls(title="Tasks API")),
    path('api/v2/login/', UserLogin, name='login'),
    path('api/v2/register/', UserRegister, name='register'),
    path('api/v2/logout/', UserLogout, name='logout'),
    path('api/v2/user/', UserView, name='user'),
    path('api/saludo/', saludo, name='saludo'),
    path('register/', registerview),
    path('login/', loginview),
    path('perfil/', perfilview),
    path('transaccionpage/', transaccion_view, name='transaccionpage'),
    path('transaccion/', transferencia_view, name='transaccion'),
    path('transferirbeatpay/', beatpay, name='transferirbeatpay'),
    path('beatpayform/', beatpayform, name='beatpayform')
]
