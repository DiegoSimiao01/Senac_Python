from django.shortcuts import render

def pagina_cadastro(request):
    # Por enquanto, esta view apenas renderiza o template.
    # No futuro, ela também receberá os dados do POST.
    
    # O Django irá procurar por 'cadastro.html' em todas as 
    # pastas 'templates' dos seus apps.
    return render(request, 'cadastro.html')