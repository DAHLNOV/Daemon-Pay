from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from paysystem import views
from .views import homeApi

router = routers.DefaultRouter()
router.register(r'paysystem', views.TaskView, 'paysystem')
router.register(r'usuarios', views.UsuarioView, 'usuario')
router.register(r'transacciones', views.TransaccionView, 'transacciones')

urlpatterns = [
    path('',homeApi), 
    path("api/v1/", include(router.urls)) ,
    path('docs/', include_docs_urls(title="Tasks API")),
]
