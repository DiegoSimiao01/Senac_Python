import flet as ft
import requests
import os

# --- CONFIGURAÇÕES ---
API_KEY = "8cb2f00bcea8dd56498d37d8b763a9a5"  # <--- SUA CHAVE
BASE_URL = "https://api.themoviedb.org/3"
IMG_URL = "https://image.tmdb.org/t/p/w500"
IMG_HD_URL = "https://image.tmdb.org/t/p/original"

# Cores
COR_PRIMARIA = "#00D1FF"
COR_TEXTO = "#FFFFFF"
COR_NAVBAR = "#E6141414"
COR_YOUTUBE = "#FF0000"

def main(page: ft.Page):
    page.title = "piTexMovies"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    
    # --- ELEMENTOS GLOBAIS ---
    background_image = ft.Image(
        src="", fit=ft.ImageFit.COVER, opacity=0.4, expand=True, animate_opacity=300
    )
    
    background_overlay = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            colors=["#99000000", "#FF141414"], 
            stops=[0.0, 1.0],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        )
    )

    # --- FUNÇÕES DE API ---
    def obter_dados(endpoint, params=None):
        default_params = {"api_key": API_KEY, "language": "pt-BR"}
        if params: default_params.update(params)
        try:
            res = requests.get(f"{BASE_URL}{endpoint}", params=default_params)
            if res.status_code == 200:
                json_data = res.json()
                if 'results' in json_data:
                    return json_data['results']
                return json_data
        except: pass
        return []

    # --- NOVO: PLAYER DE VÍDEO (USANDO WEBVIEW) ---
    def exibir_trailer(key_youtube):
        # URL de Embed do YouTube
        url = f"https://www.youtube.com/embed/{key_youtube}?autoplay=1&controls=1"
        
        # Componente WebView (Vira Iframe na Web)
        webview = ft.WebView(
            url=url,
            expand=True,
        )

        # Cria o Dialog (Janela flutuante)
        dialog_trailer = ft.AlertDialog(
            content=ft.Container(
                content=webview,
                width=800, 
                height=450,
                bgcolor="black"
            ),
            title=ft.Text("Trailer Oficial"),
            bgcolor="#1a1a1a",
        )
        
        # --- CORREÇÃO: NOVA FORMA DE ABRIR DIALOG ---
        page.open(dialog_trailer)
        page.update()

    # --- UI: TELA DE DETALHES ---
    detalhe_titulo = ft.Text(size=40, weight=ft.FontWeight.BOLD, color="white")
    detalhe_subtitulo = ft.Text(size=18, color=COR_PRIMARIA) 
    detalhe_info = ft.Text(size=16, color="#cccccc") 
    detalhe_generos = ft.Row(wrap=True) 
    detalhe_sinopse = ft.Text(size=16, color="#dddddd")
    
    btn_trailer = ft.ElevatedButton(
        "Assistir Trailer",
        icon=ft.Icons.PLAY_CIRCLE_FILL,
        bgcolor=COR_YOUTUBE,
        color="white",
        visible=False,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=20)
    )

    detalhe_poster = ft.Image(src="", width=300, border_radius=10, fit=ft.ImageFit.COVER)
    detalhe_elenco = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=15)

    def fechar_detalhes(e):
        container_detalhes.visible = False
        conteudo_principal.visible = True 
        background_image.opacity = 0.4
        btn_trailer.visible = False 
        
        # --- CORREÇÃO: FECHAR QUALQUER DIALOG ABERTO (SE HOUVER) ---
        # Não tentamos acessar page.dialog, apenas garantimos que overlays fechem
        # Mas aqui estamos fechando a tela de detalhes, o dialog fecha sozinho ao clicar fora
        # ou podemos forçar se necessário, mas a API nova gerencia bem.
        page.update()

    container_detalhes = ft.Container(
        visible=False, 
        padding=ft.padding.only(top=100, left=50, right=50, bottom=50),
        expand=True,
        bgcolor="#CC141414", 
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                         ft.TextButton("< Voltar", icon=ft.Icons.ARROW_BACK, on_click=fechar_detalhes, style=ft.ButtonStyle(color="white")),
                    ]
                ),
                ft.Container(height=20),
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Container(
                            content=detalhe_poster,
                            shadow=ft.BoxShadow(blur_radius=20, color="black"),
                            border_radius=10
                        ),
                        ft.Container(width=30),
                        ft.Column( 
                            expand=True,
                            controls=[
                                detalhe_titulo,
                                detalhe_subtitulo,
                                ft.Container(height=10),
                                detalhe_generos,
                                ft.Container(height=20),
                                ft.Row(controls=[btn_trailer], alignment=ft.MainAxisAlignment.START),
                                ft.Container(height=20),
                                detalhe_info,
                                ft.Divider(color="white24"),
                                ft.Text("Sinopse", weight=ft.FontWeight.BOLD, size=18),
                                detalhe_sinopse,
                                ft.Container(height=20),
                                ft.Text("Elenco Principal", weight=ft.FontWeight.BOLD, size=18),
                                ft.Container(height=10),
                                detalhe_elenco
                            ]
                        )
                    ]
                )
            ]
        )
    )

    # --- LÓGICA: ABRIR DETALHES ---
    def abrir_detalhes_item(id_item, eh_serie=False):
        tipo = "tv" if eh_serie else "movie"
        
        dados = obter_dados(f"/{tipo}/{id_item}")
        if not dados or isinstance(dados, list): return 

        creditos_raw = obter_dados(f"/{tipo}/{id_item}/credits")
        elenco = creditos_raw.get('cast', []) if isinstance(creditos_raw, dict) else []

        videos_raw = obter_dados(f"/{tipo}/{id_item}/videos")
        btn_trailer.visible = False 
        btn_trailer.on_click = None
        
        if isinstance(videos_raw, list): # Verifica se é lista antes de iterar
            for video in videos_raw:
                if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
                    key = video.get('key')
                    btn_trailer.visible = True
                    # Lambda capturando 'k' corretamente
                    btn_trailer.on_click = lambda e, k=key: exibir_trailer(k)
                    break 

        backdrop = dados.get('backdrop_path')
        if backdrop:
            background_image.src = f"{IMG_HD_URL}{backdrop}"
            background_image.opacity = 0.2 
            background_image.update()

        titulo = dados.get('name') if eh_serie else dados.get('title')
        detalhe_titulo.value = titulo.upper() if titulo else "SEM TÍTULO"
        detalhe_subtitulo.value = dados.get('tagline', '')
        
        tempo = f"{dados.get('runtime', '?')} min" if not eh_serie else f"{dados.get('number_of_seasons')} Temporadas"
        ano = dados.get('first_air_date', '') if eh_serie else dados.get('release_date', '')
        nota = dados.get('vote_average', 0)
        status = dados.get('status', 'N/A')
        detalhe_info.value = f"📅 {ano[:4]}  |  ⏱️ {tempo}  |  ⭐ {nota:.1f}/10  |  Status: {status}"
        
        detalhe_sinopse.value = dados.get('overview', 'Sinopse indisponível.')
        
        poster_path = dados.get('poster_path')
        detalhe_poster.src = f"{IMG_URL}{poster_path}" if poster_path else "https://via.placeholder.com/300x450"

        detalhe_generos.controls = [
            ft.Container(padding=10, bgcolor="#333333", border_radius=20, content=ft.Text(g['name'])) 
            for g in dados.get('genres', [])
        ]

        detalhe_elenco.controls.clear()
        if elenco:
            for ator in elenco[:10]: 
                caminho_foto = ator.get('profile_path')
                url_foto = f"{IMG_URL}{caminho_foto}" if caminho_foto else "https://via.placeholder.com/100"
                detalhe_elenco.controls.append(
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=80, height=80, 
                                border_radius=40, 
                                content=ft.Image(src=url_foto, fit=ft.ImageFit.COVER)
                            ),
                            ft.Text(ator['name'], size=12, width=80, text_align=ft.TextAlign.CENTER, no_wrap=False)
                        ]
                    )
                )

        conteudo_principal.visible = False
        container_detalhes.visible = True
        page.update()

    # --- UI: LISTAS (HOME) ---
    conteudo_principal = ft.Column(scroll=ft.ScrollMode.HIDDEN, expand=True)
    
    def criar_poster(item, eh_serie=False):
        img_src = f"{IMG_URL}{item.get('poster_path')}" if item.get('poster_path') else ""
        titulo = item.get('title') or item.get('name')
        return ft.Container(
            content=ft.Image(src=img_src, border_radius=10, fit=ft.ImageFit.COVER),
            width=150, height=225, border_radius=10,
            on_click=lambda e: abrir_detalhes_item(item['id'], eh_serie),
            tooltip=titulo
        )

    def carregar_home(e=None):
        background_image.opacity = 0.4
        container_detalhes.visible = False
        conteudo_principal.visible = True
        conteudo_principal.controls.clear()

        filmes = obter_dados("/movie/popular")
        series = obter_dados("/tv/popular")
        
        if filmes and len(filmes) > 0:
            destaque = filmes[0]
            background_image.src = f"{IMG_HD_URL}{destaque['backdrop_path']}"
            
            conteudo_principal.controls = [
                ft.Container(height=100), 
                ft.Container(padding=40, content=ft.Column([
                    ft.Text(destaque['title'].upper(), size=60, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(destaque['overview'], width=600, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, color="#cccccc"),
                    ft.Container(height=20),
                    ft.ElevatedButton("Mais Informações", on_click=lambda e: abrir_detalhes_item(destaque['id']), bgcolor=COR_PRIMARIA, color="black")
                ])),
                ft.Container(padding=ft.padding.only(left=40), content=ft.Text("Filmes Populares", size=24, weight=ft.FontWeight.BOLD)),
                ft.Container(height=20),
                ft.Container(
                    padding=ft.padding.only(left=40, right=40),
                    content=ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=15, controls=[criar_poster(f) for f in filmes[1:]], height=240)
                ),
                ft.Container(height=40),
                ft.Container(padding=ft.padding.only(left=40), content=ft.Text("Séries em Alta", size=24, weight=ft.FontWeight.BOLD)),
                ft.Container(height=20),
                ft.Container(
                    padding=ft.padding.only(left=40, right=40, bottom=50),
                    content=ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=15, controls=[criar_poster(s, True) for s in series[:10] if s])
                )
            ]
        else:
            conteudo_principal.controls = [ft.Text("Carregando...", color="white")]
            
        page.update()
    
    def buscar_item(e):
        termo = e.control.value
        if not termo: return
        res = obter_dados("/search/movie", {"query": termo})
        resultados_ui = [criar_poster(f) for f in res] if res else []
        if not resultados_ui: resultados_ui = [ft.Text("Nada encontrado.")]

        conteudo_principal.controls = [
            ft.Container(height=100),
            ft.Container(padding=40, content=ft.Text(f"Resultados para: {termo}", size=30)),
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=20, controls=resultados_ui)
        ]
        page.update()

    navbar = ft.Container(
        bgcolor=COR_NAVBAR, padding=ft.padding.symmetric(horizontal=40, vertical=15),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("piTexMovies", size=24, weight=ft.FontWeight.BOLD, color=COR_PRIMARIA),
                ft.Row([
                    ft.IconButton(ft.Icons.HOME, on_click=carregar_home, icon_color="white"),
                    ft.TextField(hint_text="Buscar...", height=40, text_size=14, content_padding=10, border_radius=20, on_submit=buscar_item, bgcolor="#333333", border_width=0)
                ])
            ]
        )
    )

    page.add(ft.Stack(expand=True, controls=[background_image, background_overlay, conteudo_principal, container_detalhes, navbar]))
    carregar_home()

# --- CONFIGURAÇÃO FINAL DE EXECUÇÃO PARA RENDER ---
port = int(os.getenv("PORT", 8000))
ft.app(target=main, port=port, view=ft.AppView.WEB_BROWSER)