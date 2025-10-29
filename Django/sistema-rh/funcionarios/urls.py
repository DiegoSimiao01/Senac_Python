from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('api/funcionarios/', views.api_funcionarios, name='api_funcionarios'),
]