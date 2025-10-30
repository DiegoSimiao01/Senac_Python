from django.urls import path
from . import views

urlpatterns = [
    # ex: /cadastro/
    path('', views.pagina_cadastro, name='pagina_cadastro'),
    
    # NOVA URL: ex: /cadastro/editar/5/
    path('editar/<int:id>/', views.pagina_editar, name='pagina_editar'),
    
    # NOVA URL: ex: /cadastro/deletar/5/
    path('deletar/<int:id>/', views.deletar_funcionario, name='deletar_funcionario'),
]