from django.urls import path
from . import views # Importa as views do app atual

urlpatterns = [
    # Quando a URL for '' (vazio) DENTRO deste app, 
    # chame a view 'pagina_cadastro'
    path('', views.pagina_cadastro, name='pagina_cadastro'),
]