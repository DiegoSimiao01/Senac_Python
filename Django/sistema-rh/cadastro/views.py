from django.shortcuts import render, redirect, get_object_or_404
# Lembre-se: Se o seu modelo não se chama 'Funcionario', 
# troque o nome na linha abaixo.
from funcionarios.models import Funcionario 

# --- SUA VIEW EXISTENTE (MODIFICADA) ---
def pagina_cadastro(request):
    if request.method == 'POST':
        # Lógica para CRIAR um novo funcionário
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')
        salario = request.POST.get('salario')
        departamento = request.POST.get('departamento')
        
        Funcionario.objects.create(
            nome=nome,
            cargo=cargo,
            salario_base=salario,
            depto=departamento
        )
        # Redireciona de volta para a mesma página (para limpar o formulário)
        return redirect('pagina_cadastro') 
    
    # Lógica GET (mostrar a lista)
    funcionarios_list = Funcionario.objects.all().order_by('-id') # Ordena por mais novo
    total = funcionarios_list.count()
    context = {
        'funcionarios': funcionarios_list,
        'total': total
    }
    return render(request, 'cadastro.html', context)


# --- NOVA VIEW PARA EDITAR ---
def pagina_editar(request, id):
    # Busca o funcionário específico pelo ID ou retorna um erro 404
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        # Lógica para ATUALIZAR o funcionário existente
        funcionario.nome = request.POST.get('nome')
        funcionario.cargo = request.POST.get('cargo')
        funcionario.salario_base = request.POST.get('salario')
        funcionario.depto = request.POST.get('departamento')
        funcionario.save()
        
        # Redireciona para a página de lista/cadastro
        return redirect('pagina_cadastro')
    
    # Se for um GET, apenas mostra a página de edição com os dados
    context = {
        'funcionario': funcionario
    }
    return render(request, 'editar.html', context)


# --- NOVA VIEW PARA DELETAR ---
def deletar_funcionario(request, id):
    # Busca o funcionário
    funcionario = get_object_or_404(Funcionario, id=id)
    
    # Apenas deleta se for um método POST (por segurança)
    if request.method == 'POST':
        funcionario.delete()
        # Redireciona de volta para a lista
        return redirect('pagina_cadastro')
    
    # Se alguém tentar acessar via GET, apenas redireciona
    return redirect('pagina_cadastro')