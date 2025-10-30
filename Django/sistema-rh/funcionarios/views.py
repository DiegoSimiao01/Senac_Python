from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
funcionarios = []

def api_funcionarios(request):
    """
    Endpoint que retorna lista de funcionários em JSON
    Acesse: http://127.0.0.1:8000/api/funcionarios/
    """
    data = {
    'funcionarios': funcionarios,
    'total': len(funcionarios)
    }

    return JsonResponse(data)

def pagina_principal(request):
    """
    Página principal do Sistema RH
    Acesse: http://127.0.0.1:8000/
    """
    if request.method == 'POST':
    # Processar formulário
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')
        salario = request.POST.get('salario')
        departamento = request.POST.get('departamento')
        
        if nome and cargo:  # Campos obrigatórios
            novo_funcionario = {
                'id': len(funcionarios) + 1,
                'nome': nome,
                'cargo': cargo,
                'salario': salario,
                'departamento': departamento
            }
            funcionarios.append(novo_funcionario)
            return redirect('pagina_principal')
    context = {
        'funcionarios': funcionarios,
        'total': len(funcionarios)
}
    return render(request, 'index.html', context)
def api_funcionarios(request):
    """
    Endpoint JSON da API
    """
    data = {
    'funcionarios': funcionarios,
    'total': len(funcionarios)
}
    return JsonResponse(data)