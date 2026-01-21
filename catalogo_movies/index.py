import requests
import sys

# --- CONFIGURAÇÕES GERAIS ---
# Substitua 'SUA_CHAVE_AQUI' pela sua API Key real do TMDB
API_KEY = "8cb2f00bcea8dd56498d37d8b763a9a5" 
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500" # Link base para imagens (tamanho w500)
IDIOMA = "pt-BR" # Para receber respostas em português

def formatar_dinheiro(valor):
    """Função auxiliar para formatar orçamento e receita"""
    if valor == 0:
        return "Não informado"
    return f"U$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def buscar_filme(nome_filme):
    """Busca o filme pelo nome e retorna o ID do primeiro resultado"""
    endpoint = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": nome_filme,
        "language": IDIOMA
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status() # Lança erro se houver problema na conexão (404, 500, etc)
        
        dados = response.json()
        
        if dados['total_results'] > 0:
            # Retorna o primeiro filme da lista (o mais relevante)
            filme_encontrado = dados['results'][0]
            return filme_encontrado['id'], filme_encontrado['title']
        else:
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        sys.exit()

def obter_detalhes_filme(movie_id):
    """Busca os detalhes completos usando o ID do filme"""
    endpoint = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": IDIOMA
    }
    
    response = requests.get(endpoint, params=params)
    return response.json()

def exibir_relatorio(dados):
    """Formata e imprime os dados de forma bonita no terminal"""
    print("\n" + "="*50)
    print(f"🎬  TÍTULO: {dados['title'].upper()}")
    print("="*50)
    
    # Tratamento da data (pega apenas o ano)
    ano = dados.get('release_date', '')[:4]
    
    # Gêneros (vem como uma lista de dicionários, precisamos extrair os nomes)
    generos = [g['name'] for g in dados.get('genres', [])]
    generos_str = ", ".join(generos)

    print(f"📅  Ano: {ano}")
    print(f"⭐  Nota: {dados['vote_average']:.1f}/10 (baseado em {dados['vote_count']} votos)")
    print(f"🎭  Gêneros: {generos_str}")
    print(f"⏱️  Duração: {dados['runtime']} minutos")
    print(f"💰  Orçamento: {formatar_dinheiro(dados.get('budget', 0))}")
    print(f"💵  Bilheteria: {formatar_dinheiro(dados.get('revenue', 0))}")
    print("-" * 50)
    print(f"📝  SINOPSE:\n{dados.get('overview', 'Sinopse não disponível.')}")
    print("-" * 50)
    
    # Construção da URL da imagem
    if dados.get('poster_path'):
        url_imagem = f"{IMAGE_BASE_URL}{dados['poster_path']}"
        print(f"🖼️  LINK DO PÔSTER: {url_imagem}")
    else:
        print("🖼️  LINK DO PÔSTER: Imagem não disponível")
    print("="*50 + "\n")

# --- FLUXO PRINCIPAL (MAIN) ---
if __name__ == "__main__":
    print("--- SISTEMA DE BUSCA DE FILMES (TMDB API) ---")
    
    if API_KEY == "SUA_CHAVE_AQUI":
        print("⚠️  ERRO: Você precisa configurar a API_KEY no código antes de rodar!")
    else:
        while True:
            busca = input("Digite o nome do filme (ou 'sair' para fechar): ").strip()
            
            if busca.lower() == 'sair':
                break
            
            if not busca:
                continue

            print(f"🔍  Buscando por '{busca}'...")
            
            # 1. Buscar ID
            id_filme, titulo_oficial = buscar_filme(busca)
            
            if id_filme:
                print(f"✅  Encontrado: {titulo_oficial}. Carregando detalhes...")
                
                # 2. Buscar Detalhes Completos
                detalhes = obter_detalhes_filme(id_filme)
                
                # 3. Exibir
                exibir_relatorio(detalhes)
            else:
                print("❌  Filme não encontrado. Tente outro nome.")