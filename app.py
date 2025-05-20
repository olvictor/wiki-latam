from collections import defaultdict
from flask import Flask, request
import pandas as pd
import re
import unicodedata
from flask_cors import CORS
from flask import Flask, render_template, jsonify
from openpyxl import load_workbook
import urllib.request
import urllib.parse
import json


app = Flask(__name__)
CORS(app)


CLIENT_ID = 'qdn4nkcag974fxftx5xwfs5goddqx6'
CLIENT_SECRET = 'l0a2yo19o38jl7luid7nu0xerz38m1'

def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    data = urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        return result['access_token']
    
 
def is_stream_live(username):
    token = get_access_token()

    # Aqui, estamos usando o nome de usuário extraído da URL
    url = f'https://api.twitch.tv/helix/streams?user_login={username}'
    req = urllib.request.Request(url)
    req.add_header('Client-ID', CLIENT_ID)
    req.add_header('Authorization', f'Bearer {token}')

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            streams = result.get('data', [])
            return len(streams) > 0  # Retorna True se a live estiver online, caso contrário, False
    except urllib.error.HTTPError as e:
        # Isso captura o erro 400 e imprime o conteúdo da resposta
        print(f"Erro HTTP {e.code}: {e.reason}")
        print(f"Resposta: {e.read()}")
        return False
    

def extrair_nome_usuario(url):
    # Utiliza expressão regular para pegar a parte após "https://www.twitch.tv/"
    match = re.search(r'https://www.twitch.tv/([a-zA-Z0-9_]+)', url)
    if match:
        return match.group(1)
    return None  # Caso o URL não esteja no formato esperado   


def check_live(username):
        try:
            live, data = is_stream_live(username)
            return jsonify({
                'username': username,
                'live': live,
                'stream_data': data
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def carregar_links():
    file_path = 'rola.xlsx'
    df = pd.read_excel(file_path, header=None)

    links = df.iloc[10:14, 1].dropna().tolist()

    icones = {
    'Discord': 'fa-brands fa-discord',
    'Site': 'fa-solid fa-globe',
    'Calculadora': 'fa-solid fa-calculator',
    'Skill Simulator': 'fa-solid fa-wand-magic-sparkles'
    }


    links_formatados = []
    for item in links:
     if ':' in item:
            nome, link = item.split(':', 1)
            nome = nome.strip()
            link = link.strip()
            icone = icones.get(nome, 'fa-solid fa-link') 
            links_formatados.append({
                'nome': nome,
                'link': link,
                'icone': icone
            })

    return links_formatados


@app.context_processor
def inject_request():
    return dict(request=request)

@app.route('/')
def info_page():
    file_path = 'rola.xlsx'
    df_link = pd.read_excel(file_path, header=None)
    info_essenciais = df_link.iloc[2:7, 1].dropna().tolist()

    links = df_link.iloc[10:14, 1].dropna().tolist()


    icones = {
    'Discord': 'fa-brands fa-discord',
    'Site': 'fa-solid fa-globe',
    'Calculadora': 'fa-solid fa-calculator',
    'Skill Simulator': 'fa-solid fa-wand-magic-sparkles'
    }


    links_formatados = []
    for item in links:
     if ':' in item:
            nome, link = item.split(':', 1)
            nome = nome.strip()
            link = link.strip()
            icone = icones.get(nome, 'fa-solid fa-link')  # ícone padrão
            links_formatados.append({
                'nome': nome,
                'link': link,
                'icone': icone
            })

    rank_tiers = df_link.iloc[3:, 8].dropna().tolist()
    rank_classes = df_link.iloc[3:, 9].dropna().tolist()

    links = carregar_links()

    rank_data = list(zip(rank_tiers, rank_classes))


    return render_template(
        'index.html',
        info=info_essenciais,
        links=links_formatados,
        rank_data = rank_data
        )


@app.route('/classes')
def classes_page():
    df = pd.read_excel('rola.xlsx', header=None)
    classes = df.iloc[1:27, 3].dropna().tolist()
    builds = df.iloc[1:29, 4].dropna().tolist()

    wb = load_workbook('rola.xlsx')
    ws = wb["INFORMAÇÕES"]
        
    links_classes = []
    for row in ws.iter_rows(min_row=33, min_col=2, max_col=2):
            cell = row[0]
            if cell.hyperlink:
                links_classes.append(cell.hyperlink.target)
            elif cell.value:
                links_classes.append(cell.value)


    class_builds = [
        {"classe": classes[1], "builds": [builds[1], builds[2]], "link": "","imagem": "assets/classes/feiticeiro.png"}, #Feiticeiro
        {"classe": classes[2], "builds": [builds[3]], "link": links_classes[4],"imagem": "assets/classes/sentinela.png"},# Sentinela
        {"classe": classes[3], "builds": [builds[4]], "link": links_classes[5],"imagem": "assets/classes/sicario.png"},# Sicario
        {"classe": classes[4], "builds": [builds[5]], "link": links_classes[6],"imagem": "assets/classes/arcano.png"},# Arcano
        {"classe": classes[5], "builds": [builds[6], builds[7]], "link": "","imagem": "assets/classes/arcebispo.png"},# Arcebispo
        {"classe": classes[6], "builds": [builds[9], builds[8]], "link": links_classes[3],"imagem": "assets/classes/renegado.png"},# Renegado
        {"classe": classes[7], "builds": [builds[11], builds[10]], "link": "","imagem": "assets/classes/sura.png"},# Shura
        {"classe": classes[8], "builds": [builds[12]], "link": links_classes[1],"imagem": "assets/classes/cavaleiro_runico.png"}, # Cavaleiros Rúnicos
        {"classe": classes[9], "builds": [builds[14], builds[13]], "link": links_classes[2],"imagem": "assets/classes/guardioes_reais.png"},# Guardião Real
        {"classe": classes[10], "builds": [builds[15]], "link": "","imagem": "assets/classes/mecanico.png"},# Mecânico
        {"classe": classes[11], "builds": [builds[16]], "link": "","imagem": "assets/classes/genetico.png"},# Bioquímicos
        {"classe": classes[12], "builds": [builds[17], builds[18]], "link": links_classes[7],"imagem": "assets/classes/trovador.png"},# Trovadores
        {"classe": classes[13], "builds": [builds[19], builds[20]], "link": links_classes[7],"imagem": "assets/classes/musa.png"}, # Musa
    ]
    links = carregar_links()
    return render_template('classes.html', 
                           class_builds=class_builds,
                           links = links
                           )

@app.route('/rank')
def rank_page():
    df = pd.read_excel('rola.xlsx', header=None)
    rank_tiers = df.iloc[3:, 8].dropna().tolist()
    rank_classes = df.iloc[3:, 9].dropna().tolist()

    links = carregar_links()

    rank_data = list(zip(rank_tiers, rank_classes))
    return render_template('rank.html', 
                           rank_data=rank_data,
                           links= links
                           )

@app.route('/rotas')
def rotas_page():
    df_melee = pd.read_excel('rola.xlsx', sheet_name='ROTAS MELEE + DICAS', header=None)
    melee_raw = df_melee.iloc[2:,1].dropna().tolist()
    quest_melee =  df_melee.iloc[1:,3].dropna().tolist() 
    builds_melee = df_melee.iloc[:,4].dropna().tolist() 

    df_ranged = pd.read_excel('rola.xlsx', sheet_name='ROTAS RANGED + DICAS', header=None)
    ranged_raw = df_ranged.iloc[2:,1].dropna().tolist()
    quest_ranged =  df_ranged.iloc[1:,3].dropna().tolist() 
    builds_ranged = df_ranged.iloc[:,4].dropna().tolist() 

    #ROTAS MELEE
    rotas_melee = []
    for linha in melee_raw:
        linha = str(linha).strip()

        match = re.match(r"^(\d+~\d+|\d+\+?)\s*(.*)", linha)

        if match:
            nivel = match.group(1).strip()
            local = match.group(2).strip()
        else:
            nivel = ""
            local = linha

        rotas_melee.append((nivel, local))


    array_quest_melee = [
        (quest_melee[1]),
        (quest_melee[2]),
        (quest_melee[3]),
        (quest_melee[4]),
        (quest_melee[5]),
        (quest_melee[6]),
        (quest_melee[8]),
        (quest_melee[9]),
        (quest_melee[10])
    ]

    array_builds_melee = [
         (quest_melee[13], builds_melee[4]),
         (quest_melee[14], builds_melee[5]),
         (quest_melee[15], builds_melee[6]),
         (quest_melee[16], builds_melee[7]),
         (quest_melee[17], builds_melee[8]),
         (quest_melee[18], builds_melee[9]),
         (quest_melee[19], builds_melee[10]),
    ]

    print(array_builds_melee)
    array_builds_formatado =[]
   
    for quest, build in array_builds_melee:
    # Converte para string e remove espaços
        quest = str(quest).strip()
        build = str(build).strip()

    # Remove parênteses e aspas se houver
        quest = re.sub(r"^[('\"\s]+|[)'\"]+$", "", quest)
        build = re.sub(r"^[('\"\s]+|[)'\"]+$", "", build)

    # Adiciona como tupla limpa
        array_builds_formatado.append((quest, build))
    

    ########### ROTAS RANGED
    rotas_ranged = []
    for linha in ranged_raw:
        linha = str(linha).strip()

        match = re.match(r"^(\d+~\d+|\d+\+?)\s*(.*)", linha)

        if match:
            nivel = match.group(1).strip()
            local = match.group(2).strip()
        else:
            nivel = ""
            local = linha

        rotas_ranged.append((nivel, local))


    array_quest_ranged = [
        ("Equipamentos " + quest_ranged[1]),
        (quest_ranged[2]),
        (quest_ranged[3]),
        (quest_ranged[4]),
        (quest_ranged[5]),
        (quest_ranged[6]),
        (quest_ranged[8]),
        (quest_ranged[9]),
        (quest_ranged[10])
    ]

    array_builds_ranged = [
         (quest_ranged[13], builds_ranged[4]),
         (quest_ranged[14], builds_ranged[5]),
         (quest_ranged[15], builds_ranged[6]),
         (quest_ranged[16], builds_ranged[7]),
         (quest_ranged[17], builds_ranged[8]),
    ]
    array_builds_ranged_formatado =[]
   
    for quest, build in array_builds_ranged:
    # Converte para string e remove espaços
        quest = str(quest).strip()
        build = str(build).strip()

    # Remove parênteses e aspas se houver
        quest = re.sub(r"^[('\"\s]+|[)'\"]+$", "", quest)
        build = re.sub(r"^[('\"\s]+|[)'\"]+$", "", build)

    # Adiciona como tupla limpa
        array_builds_ranged_formatado.append((quest, build))
   
    links = carregar_links()

    return render_template(
        'rotas.html',
        rotas_melee=rotas_melee,
        array_quest_melee=array_quest_melee,
        array_builds_formatado = array_builds_formatado,
        rotas_ranged=rotas_ranged,
        array_quest_ranged=array_quest_ranged,
        array_builds_ranged_formatado = array_builds_ranged_formatado,
        links=links
    )

@app.route('/items')
def items_page():
    file_path = 'rola.xlsx'
    df = pd.read_excel(file_path, sheet_name='TABELA ITENS', header=None)
    df_items = pd.read_excel(file_path, sheet_name='ITENS NÃO VENDER', header=None)

    items = df.iloc[3:,1]
    utilizar = df.iloc[3:,2]


    
    arquivo = ["item_db_usable.yml","item_db_equip.yml","item_db_etc.yml"]
    items_n_vender_raw_3 = df_items.iloc[3:,6].dropna().tolist()
    items_n_vender_raw_3_2 = df_items.iloc[3:,7].dropna().tolist()
    items_n_vender_raw_3_2_3 = df_items.iloc[3:,8].dropna().tolist()

    items_n_vender_raw_4 = df_items.iloc[3:,12].dropna().tolist()
    items_n_vender_raw_4_2 = df_items.iloc[3:,14].dropna().tolist()



    items_n_vender_raw_5 = df_items.iloc[3:,20].dropna().tolist()
    items_n_vender_raw_6 = df_items.iloc[3:,24].dropna().tolist()
    items_n_vender_raw_6_2 = df_items.iloc[3:,26].dropna().tolist()
    items_n_vender_raw_6_3 = df_items.iloc[3:,28].dropna().tolist()
    items_n_vender_raw_6_4 = df_items.iloc[3:,30].dropna().tolist()
    items_n_vender_raw_6_5 = df_items.iloc[3:,32].dropna().tolist()



    items_n_vender_raw_7 = df_items.iloc[3:,36].dropna().tolist()
    items_n_vender_raw_7_2 = df_items.iloc[3:,37].dropna().tolist()
    items_n_vender_raw_7_3 = df_items.iloc[3:,38].dropna().tolist()
    items_n_vender_raw_7_4 = df_items.iloc[3:,39].dropna().tolist()



    items_n_vender_raw_8 = df_items.iloc[3:,43].dropna().tolist()
    items_n_vender_raw_8_2 = df_items.iloc[3:,44].dropna().tolist()
    items_n_vender_raw_8_3 = df_items.iloc[3:,45].dropna().tolist()
    items_n_vender_raw_8_4 = df_items.iloc[3:,46].dropna().tolist()



    items_n_vender_raw_9 = df_items.iloc[12:,45].dropna().tolist()





    def normalizar(texto):
        if texto is None:
            return ""
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').strip().lower()
    
    def buscar_id_por_nome_em_arquivos(nome_procurado, arquivo):
        nome_procurado_norm = normalizar(nome_procurado)

        for caminho_arquivo in arquivo:
            try:
                with open(caminho_arquivo, 'r', encoding='latin-1') as file:
                    bloco = []
                    for linha in file:
                        if linha.strip().startswith('- Id:'):
                            if bloco:
                                for l in bloco:
                                    if l.strip().startswith("Name:"):
                                        nome_linha = l.split(":", 1)[1].strip()
                                        if normalizar(nome_linha) == nome_procurado_norm:
                                            for b in bloco:
                                                if 'Id:' in b:
                                                    return b.split(':', 1)[1].strip()
                            bloco = [linha]
                        else:
                            bloco.append(linha)

                    # Verifica o último bloco
                    for l in bloco:
                        if l.strip().startswith("Name:"):
                            nome_linha = l.split(":", 1)[1].strip()
                            if normalizar(nome_linha) == nome_procurado_norm:
                                for b in bloco:
                                    if 'Id:' in b:
                                        return b.split(':', 1)[1].strip()

            except Exception as e:
                print(f"Erro ao processar {caminho_arquivo}: {e}")

        return None
    imagens = []

    # Loop para percorrer os itens e montar a URL da imagem com base no ID
    for item in items:
        item_id = buscar_id_por_nome_em_arquivos(item, arquivo)
        if item_id:
            imagem_url = f"https://www3.worldrag.com/database/media/item/{item_id}.gif"
            imagens.append(imagem_url)
        else:
            imagens.append("imagem_nao_encontrada")

    

    tabela_items = list(zip(items,utilizar,imagens))

    items_importantes = df.iloc[9:20,4].dropna().tolist()
    items_importantes_local = df.iloc[9:20,5].dropna().tolist()

   


    imagens_items_importantes = []
    
    for item in items_importantes:
        id_str = buscar_id_por_nome_em_arquivos(item, arquivo)
        if id_str:
            imagem_url = f"https://www3.worldrag.com/database/media/item/{id_str}.gif"
            imagens_items_importantes.append(imagem_url)
        else:
            imagens_items_importantes.append("imagem_nao_encontrada")

    tabela_items_importantes = list(zip(items_importantes,items_importantes_local,imagens_items_importantes))



    ################  items para o futuro ###############################

    item_guardar_intancia = df.iloc[23:,4].dropna().tolist()
    item_guardar = df.iloc[23:,5].dropna().tolist()
    item_guardar_moedas = df.iloc[23:,6].dropna().tolist()
    

    array_items_guardar = [
        (item_guardar_intancia[0],item_guardar[0],item_guardar_moedas[0]), # Altar do Selo
        (item_guardar_intancia[1],item_guardar[1],item_guardar_moedas[1],item_guardar[2],
        item_guardar_moedas[2],item_guardar[3],item_guardar_moedas[3],item_guardar[4],item_guardar_moedas[4],
        item_guardar[5],item_guardar_moedas[5],item_guardar[6],item_guardar_moedas[6],), # Invasão ao Aeroplano
        (item_guardar_intancia[2],item_guardar[7],item_guardar_moedas[7],item_guardar[8],item_guardar_moedas[8],
        item_guardar[9],item_guardar_moedas[9],item_guardar[10],item_guardar_moedas[10],item_guardar[11],item_guardar_moedas[11],item_guardar[12],
        item_guardar_moedas[12],item_guardar[13],item_guardar_moedas[13],item_guardar[14],item_guardar_moedas[14]), #Maldição de Glast Heim
        (item_guardar_intancia[3],item_guardar[15],item_guardar_moedas[15],item_guardar[16],item_guardar_moedas[16],item_guardar[17],item_guardar_moedas[17],
        item_guardar[18],item_guardar_moedas[18],item_guardar[19],item_guardar_moedas[19],item_guardar[20],item_guardar_moedas[20]),# Torre do Demônio
        (item_guardar_intancia[4],item_guardar[21],item_guardar_moedas[21],item_guardar[22],item_guardar_moedas[22]), # Sala Final
        (item_guardar_intancia[5],item_guardar[23],item_guardar_moedas[23]), # Ilha Bios
        (item_guardar_intancia[6],item_guardar[24],item_guardar_moedas[24]), # Caverna de Mors
    ]
    array_items_guardar_tabela = []


    array_link_instancias = [
        "https://browiki.org/wiki/Altar_do_Selo",
        "https://browiki.org/wiki/Invas%C3%A3o_ao_Aeroplano",
        "https://browiki.org/wiki/Maldi%C3%A7%C3%A3o_de_Glast_Heim",
        "https://browiki.org/wiki/Torre_do_Dem%C3%B4nio",
        "https://browiki.org/wiki/Sala_Final",
        "https://browiki.org/wiki/Ilha_Bios",
        "https://browiki.org/wiki/Caverna_de_Mors"
    ]
    # Iterar por cada bloco
    for bloco in array_items_guardar:
        instancia = bloco[0]
        dados = bloco[1:]
        
        # pares de item/moeda
        for i in range(0, len(dados), 2):
            item = dados[i]
            moeda = dados[i + 1]
            array_items_guardar_tabela.append((instancia, item, moeda))
   

    tabela_formatada = []
    instancia_anterior = None

    for instancia, item, moeda in array_items_guardar_tabela:
            if instancia != instancia_anterior:
                tabela_formatada.append((instancia, item, moeda))
                instancia_anterior = instancia
            else:
                tabela_formatada.append(("", item, moeda))
 

    dados_com_links = []
    link_index = 0
    for nome, descricao, quantidade in tabela_formatada:
        if nome.strip():  # se nome não está vazio
            link = array_link_instancias[link_index] if link_index < len(array_link_instancias) else None
            link_index += 1
        else:
            link = " "

        dados_com_links.append((nome, descricao, quantidade, link))

    for item in dados_com_links:
        print(item)

        ###################  items n vender ###############
    
    array_items_n_vender = [
    {"classe": items_n_vender_raw_3[0].replace(" Nada", "").strip(), "items": [], "imagem": "assets/classes/espadachin.png"}, #Espadachin
    {"classe": items_n_vender_raw_3[1], "items": [
        [
            items_n_vender_raw_3[2],
            items_n_vender_raw_3[3],
            items_n_vender_raw_3[4],
            items_n_vender_raw_3[5],
            items_n_vender_raw_3[6],
            items_n_vender_raw_3[7]
        ],
        [
            items_n_vender_raw_3_2_3[0],
            items_n_vender_raw_3_2_3[1],
            items_n_vender_raw_3_2_3[2],
            items_n_vender_raw_3_2_3[3],
            items_n_vender_raw_3_2_3[4],
            items_n_vender_raw_3_2_3[5]
        ]
    ],
    "imagem": "assets/classes/cavaleiro.png"
    }, #Cavaleiro
    {"classe": items_n_vender_raw_3[8], "items": [
        [
            items_n_vender_raw_3[9],
            items_n_vender_raw_3[10]
        ],
        [
            items_n_vender_raw_3_2_3[6],
            items_n_vender_raw_3_2_3[7]
        ]
    ],
    "imagem": "assets/classes/templario.png"
    }, #Templario
    {"classe": items_n_vender_raw_3[11].replace(" Nada", "").strip(), "items": [], "imagem": "assets/classes/cavaleiro_runico.png"}, #Cavaleiro Runico
    {"classe": items_n_vender_raw_3[12], "items": [
        [items_n_vender_raw_3[13]]
    ],
    "imagem": "assets/classes/guardioes_reais.png"
    },#Guardiao Real
    {"classe": items_n_vender_raw_4[0].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/mago.png"}, #Mago
    {"classe": items_n_vender_raw_4[1].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_4[2],
            items_n_vender_raw_4[3],
            items_n_vender_raw_4[4]
        ],
        [
            items_n_vender_raw_4_2[0],
            items_n_vender_raw_4_2[1],
            items_n_vender_raw_4_2[2],
            items_n_vender_raw_4_2[3]
        ]
    ],
    "imagem": "assets/classes/bruxo.png"
    }, #Bruxo
    {"classe": items_n_vender_raw_4[5].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_4[6],
            items_n_vender_raw_4[7]
        ],
        [
            items_n_vender_raw_4_2[4],
            items_n_vender_raw_4_2[5],
            items_n_vender_raw_4_2[6]
        ]
    ],
    "imagem": "assets/classes/sabio.png"
    }, #Sabio
    {"classe": items_n_vender_raw_4[20].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/arcano.png"}, #Arcano
    {"classe": items_n_vender_raw_4[21].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_4[22],
            items_n_vender_raw_4[23],
            items_n_vender_raw_4[24],
            items_n_vender_raw_4[25]
        ]
    ],
    "imagem": "assets/classes/feiticeiro.png"
    },#Feiticeiro
    {"classe": items_n_vender_raw_5[0].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/gatuno.png"}, #Gatuno
    {"classe": items_n_vender_raw_5[1].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/mercenario.png"},#Mercenario
    {"classe": items_n_vender_raw_5[2].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_5[3],
            items_n_vender_raw_5[4],
            items_n_vender_raw_5[5],
            items_n_vender_raw_5[6]
        ]
    ],
    "imagem": "assets/classes/arruaceiro.png"
    },#Arruaceiro
    {"classe": items_n_vender_raw_5[7].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/sicario.png"},#Sicario
    {"classe": items_n_vender_raw_5[8].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/renegado.png"},#Renegado
    {"classe": items_n_vender_raw_6[0].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/mercador.png"},#Mercador
    {"classe": items_n_vender_raw_6[1].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_6[2],
            items_n_vender_raw_6[3],
            items_n_vender_raw_6[4],
            items_n_vender_raw_6[5]
        ],
        [
            items_n_vender_raw_6_2[0],
            items_n_vender_raw_6_2[1],
            items_n_vender_raw_6_2[2],
            items_n_vender_raw_6_2[3]
        ],
        [
            items_n_vender_raw_6_3[0],
            items_n_vender_raw_6_3[1],
            items_n_vender_raw_6_3[2],
            items_n_vender_raw_6_3[3]
        ],
        [
            items_n_vender_raw_6_4[0],
            items_n_vender_raw_6_4[1],
            items_n_vender_raw_6_4[2],
            items_n_vender_raw_6_4[3]
        ],
        [
            items_n_vender_raw_6_5[0],
            items_n_vender_raw_6_5[1],
            items_n_vender_raw_6_5[2],
            items_n_vender_raw_6_5[3]
        ]
    ],
    "imagem": "assets/classes/ferreiro.png"},#Ferreiro
    {"classe": items_n_vender_raw_6[6].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_6[7],
            items_n_vender_raw_6[8],
            items_n_vender_raw_6[9],
            items_n_vender_raw_6[10],
            items_n_vender_raw_6[11],
            items_n_vender_raw_6[12],
            items_n_vender_raw_6[13],
            items_n_vender_raw_6[14],
            items_n_vender_raw_6[15],
            items_n_vender_raw_6[16]
        ],
        [
            items_n_vender_raw_6_2[4],
            items_n_vender_raw_6_2[5]
        ],
        [
            items_n_vender_raw_6_2[6]
        ]
    ],
    "imagem": "assets/classes/alquimista.png"
    },#Alquimista
    {"classe": items_n_vender_raw_6[17].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/mecanico.png"},#Mecanico
    {"classe": items_n_vender_raw_6[18].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/genetico.png"},#Genetico
    {"classe": items_n_vender_raw_7[0].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/novico.png"},#Novico
    {"classe": items_n_vender_raw_7[1].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/sacerdote.png"},#Sacerdote
    {"classe": items_n_vender_raw_7[2].replace(" Nada", "").strip(), "items": [
        [
            "Possibilidade 1",
            items_n_vender_raw_7_2[1],
            items_n_vender_raw_7_2[2],
            items_n_vender_raw_7_2[3],
            items_n_vender_raw_7_2[4],
            items_n_vender_raw_7_2[5],
            items_n_vender_raw_7_2[6],
            items_n_vender_raw_7_2[7],

        ], 
        [
            "Possibilidade 2",
            items_n_vender_raw_7_3[1],
            items_n_vender_raw_7_3[2],
            items_n_vender_raw_7_3[3],
            items_n_vender_raw_7_3[4],
            items_n_vender_raw_7_3[5],
            items_n_vender_raw_7_3[6],
        ],
        [
            "Possibilidade 3",
            items_n_vender_raw_7_4[1],
            items_n_vender_raw_7_4[2],
            items_n_vender_raw_7_4[3],
            items_n_vender_raw_7_4[4],
            items_n_vender_raw_7_4[5],
            items_n_vender_raw_7_4[6],
        ]
    ],
    "imagem": "assets/classes/monge.png"
    },#Monge
    {"classe": items_n_vender_raw_7[11].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/arcebispo.png"},#Arcebispo
    {"classe": items_n_vender_raw_7[12].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/sura.png"},#Sura
    {"classe": items_n_vender_raw_8[0].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/arqueiro.png"},#arqueiro
    {"classe": items_n_vender_raw_8[1].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_8[2],
            items_n_vender_raw_8[3],
        ],[    
            items_n_vender_raw_8_2[0],
            items_n_vender_raw_8_2[1],
        ],
        [
            items_n_vender_raw_8_3[0],
            items_n_vender_raw_8_3[1],
        ],[
              items_n_vender_raw_8_4[0],
            items_n_vender_raw_8_4[1],
        ],
        [
            items_n_vender_raw_8[4],
            items_n_vender_raw_8[5],
        ],
        [
            items_n_vender_raw_8_2[2],
            items_n_vender_raw_8_2[3],
        ],
        [
            items_n_vender_raw_8_3[2],
            items_n_vender_raw_8_3[3],
        ],
        # [
        #     items_n_vender_raw_8_2[2],
        #     items_n_vender_raw_8_2[3],
        #     items_n_vender_raw_8_2[4],
        # ]

    ],"imagem": "assets/classes/caçador.png"},#Caçador
    {"classe": items_n_vender_raw_8[6].replace(" Nada", "").strip(), "items": [
        [
            items_n_vender_raw_8[7],
            items_n_vender_raw_8[8],
            items_n_vender_raw_8[9],
            items_n_vender_raw_8[10],
            items_n_vender_raw_8[11],
            items_n_vender_raw_8[12],
            items_n_vender_raw_8[13],
            items_n_vender_raw_8[14],
            items_n_vender_raw_8[15]
        ]],
     "imagem": "assets/classes/bardo.png"},#Bardo
    {"classe": items_n_vender_raw_8[16].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/sentinela.png"},#Sentinela
    {"classe": items_n_vender_raw_8[17].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/trovador.png"},#Trovador
    {"classe": items_n_vender_raw_9[0], "items": [
        [
            items_n_vender_raw_9[1],
            items_n_vender_raw_9[2],
            items_n_vender_raw_9[3],
            items_n_vender_raw_9[4],
            items_n_vender_raw_9[5],
        ],
        [  
            items_n_vender_raw_9[6],
            items_n_vender_raw_9[7],
            items_n_vender_raw_9[8],
        ],
        [
            items_n_vender_raw_9[9],
            items_n_vender_raw_9[10],
            items_n_vender_raw_9[11],
            items_n_vender_raw_9[12],
            items_n_vender_raw_9[13],
            items_n_vender_raw_9[14]
        ]
    ],
    "imagem": "assets/classes/odalisca.png"
    },#Odalistica
    {"classe": items_n_vender_raw_9[15].replace(" Nada", "").strip(), "items": [],"imagem": "assets/classes/musa.png"}#Musa
]
    
    links = carregar_links()
    return render_template('items.html', 
                           tabela_items=tabela_items,
                           tabela_items_importantes=tabela_items_importantes,
                           array_items_guardar=dados_com_links,
                           array_items_n_vender=array_items_n_vender,
                           links=links
                           )

@app.route('/monstros')
def monstros_page():
    file_path = 'rola.xlsx'
    df = pd.read_excel(file_path, sheet_name='Monstros + Drop + XP', header=None)
    df_monstro_novo = pd.read_excel('monstros_e_drops.xlsx',header=None)



    caminho_arquivos = 'itens.xlsx'
 

    def buscar_ids_itens_para_monstro(itens_str, dict_ids):
        nomes_itens = [item.strip() for item in itens_str.split(',') if item.strip()]
        resultado = []

        for nome in nomes_itens:
            id_encontrado = dict_ids.get(nome)
            resultado.append({
                "nome": nome,
                "id": id_encontrado
            })

        return resultado

    def carregar_ids_em_memoria(caminho_arquivo):
        dicionario = {}

        try:
            df = pd.read_excel(caminho_arquivo, header=None)

            for _, row in df.iterrows():
                id_item = str(row[0]).strip()
                nome = str(row[1]).strip()
                if nome and id_item:
                    dicionario[nome] = id_item

        except Exception as e:
            print(f"Erro ao processar {caminho_arquivo}: {e}")

        return dicionario


    df_monstros_novo = pd.DataFrame({
        "id": df_monstro_novo.iloc[1:, 0],
        "nome": df_monstro_novo.iloc[1:, 1],
        "level": df_monstro_novo.iloc[1:, 2],
        "hp": df_monstro_novo.iloc[1:, 3],
        "exp_base": df_monstro_novo.iloc[1:, 4],
        "exp_job": df_monstro_novo.iloc[1:, 5],
        "itens": df_monstro_novo.iloc[1:, 7],
        "mapa": df_monstro_novo.iloc[1:, 9]
    })

    df_agrupado = df_monstros_novo.groupby("nome", as_index=False).agg({
        "id": "first",
        "level": "first",
        "hp": "first",
        "exp_base": "first",
        "exp_job": "first",
        "itens": "first",
        "mapa": lambda x: ', '.join(sorted(set(str(i).strip() for i in x if pd.notna(i))))
    })

    dicionario_ids = carregar_ids_em_memoria(caminho_arquivos)

    df_agrupado["itens_com_id"] = df_agrupado["itens"].apply(
        lambda x: buscar_ids_itens_para_monstro(x, dicionario_ids)
    )
    
    data = df_agrupado.to_dict(orient='records')

    links = carregar_links()

    return render_template('monstros.html', data=data,links=links)

@app.route("/timer")
def timer_page():

    file_path = 'rola.xlsx'

    df_xp_segunda_classe = pd.read_excel(file_path, sheet_name='Tabela de XP Segunda Classe', header=None)
    df_xp_terceira_classe = pd.read_excel(file_path, sheet_name='Tabela de XP Terceira Classe', header=None)
    data =""

    bloco1 = df_xp_segunda_classe.iloc[2:, 1:4]
    bloco2 = df_xp_segunda_classe.iloc[2:, 5:8]
    bloco3 = df_xp_segunda_classe.iloc[2:, 9:12]

    for bloco in [bloco1, bloco2, bloco3]:
        bloco.columns = ['Level', 'Total EXP', 'EXP Proximo Level']

    tabela_unificada = pd.concat([bloco1, bloco2, bloco3], ignore_index=True)

    tabela_unificada = tabela_unificada.dropna(how='all')

    tabela_unificada['Level'] = pd.to_numeric(tabela_unificada['Level'], errors='coerce')
    tabela_unificada = tabela_unificada.dropna(subset=['Level'])
    tabela_unificada['Level'] = tabela_unificada['Level'].astype(int)


    df_xp_tranclasse = pd.read_excel(file_path, sheet_name='Tabela de XP Transclasse', header=None)
    
    bloco1_tranclasse = df_xp_tranclasse.iloc[2:, 1:4]
    bloco2_tranclasse = df_xp_tranclasse.iloc[2:, 5:8]
    bloco3_tranclasse = df_xp_tranclasse.iloc[2:, 9:12]


    for bloco in [bloco1_tranclasse, bloco2_tranclasse, bloco3_tranclasse]:
        bloco.columns = ['Level', 'Total EXP', 'EXP Proximo Level']

    tabela_unificada_tranclasse = pd.concat([bloco1_tranclasse, bloco2_tranclasse, bloco3_tranclasse], ignore_index=True)

    tabela_unificada_tranclasse = tabela_unificada_tranclasse.dropna(how='all')

    tabela_unificada_tranclasse['Level'] = pd.to_numeric( tabela_unificada_tranclasse['Level'], errors='coerce')
    tabela_unificada_tranclasse =  tabela_unificada_tranclasse.dropna(subset=['Level'])
    tabela_unificada_tranclasse['Level'] =  tabela_unificada_tranclasse['Level'].astype(int)




    bloco1_terceira = df_xp_terceira_classe.iloc[2:, 1:4]
    bloco2_terceira = df_xp_terceira_classe.iloc[2:, 5:8]
    bloco3_terceira = df_xp_terceira_classe.iloc[2:, 9:12]

    for bloco in [bloco1_terceira, bloco2_terceira, bloco3_terceira]:
        bloco.columns = ['Level', 'Total EXP', 'EXP Proximo Level']


    tabela_unificada_terceira = pd.concat([bloco1_terceira, bloco2_terceira, bloco3_terceira], ignore_index=True)

    tabela_unificada_terceira = tabela_unificada_terceira.dropna(how='all')

    tabela_unificada_terceira['Level'] = pd.to_numeric( tabela_unificada_terceira['Level'], errors='coerce')
    tabela_unificada_terceira =  tabela_unificada_terceira.dropna(subset=['Level'])
    tabela_unificada_terceira['Level'] =  tabela_unificada_terceira['Level'].astype(int)

    links= carregar_links()

    return render_template('timer.html', data=data,
                            tabela_unificada_segunda_classe = tabela_unificada.to_dict(orient='records'),
                            tabela_unificada_transclasse = tabela_unificada_tranclasse.to_dict(orient='records'),
                            tabela_unificada_terceira = tabela_unificada_terceira.to_dict(orient='records'),
                            links=links
                            )
@app.route('/streamers')
def streamers_page():
    file_path = 'rola.xlsx'

    df = pd.read_excel(file_path, sheet_name='INFORMAÇÕES', header=None)

    dados = df.iloc[19:,1].dropna().tolist()
    
    wb = load_workbook(file_path)
    ws = wb["INFORMAÇÕES"]
    
    links = []
    for row in ws.iter_rows(min_row=20,max_row=31, min_col=2, max_col=2):
        cell = row[0]
        if cell.hyperlink:
            links.append(cell.hyperlink.target)
        elif cell.value:
            links.append(cell.value)

    dados_links_imagens = [
         {"dados": dados[0].split(':')[0].strip(), "links": links[0],"imagem": "assets/classes/feiticeiro.png","imagem_gif": "assets/classes/gifs/feiticeiro.gif","status": "off"},
         {"dados": dados[1].split(':')[0].strip(), "links": links[1],"imagem": "assets/classes/sura.png","imagem_gif": "assets/classes/gifs/sura.gif","status": "off"},
        #  {"dados": dados[2].split(':')[0].strip(), "links": links[2],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},
        #  {"dados": dados[3].split(':')[0].strip(), "links": links[3],"imagem": "assets/classes/sicario.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[4].split(':')[0].strip(), "links": links[4],"imagem": "assets/classes/arcebispo.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[5].split(':')[0].strip(), "links": links[5],"imagem": "assets/classes/trovador.png","imagem_gif": "assets/classes/gifs/trovador.gif","status": "off"},    # lyelz
         {"dados": dados[6].split(':')[0].strip(), "links": links[6],"imagem": "assets/classes/guardioes_reais.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"}, 
         {"dados": dados[7].split(':')[0].strip(), "links": links[7],"imagem": "assets/classes/cavaleiro_runico.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},  #Asbrun 
         {"dados": dados[8].split(':')[0].strip(), "links": links[8],"imagem": "assets/classes/renegado.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[9].split(':')[0].strip(), "links": links[9],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},
         {"dados": dados[10].split(':')[0].strip(), "links": links[10],"imagem": "assets/classes/sentinela.png","imagem_gif": "assets/classes/gifs/trovador.gif","status": "off"},   
    ]
    print(dados_links_imagens)
    links = carregar_links()
    for item in dados_links_imagens:
            username = extrair_nome_usuario(item['links'])  # Extrai o nome de usuário da URL
            if username:
                is_live = is_stream_live(username)  # Verifica se está ao vivo
                
                # Atualiza o status com base no estado da live
                item['status'] = 'on' if is_live else 'off'
            else:
                print(f"Nome de usuário não encontrado na URL: {item['links']}")
    print(dados_links_imagens)
    
    return render_template('streamers.html', data=dados_links_imagens,
                            links=links
                            )



@app.route('/utilitarios')
def utilitarios_page():

   return render_template('utilitarios.html',links=carregar_links(),
)

@app.route('/contato&apoio')
def contato_page():

   return render_template('contato&apoio.html',links=carregar_links(),
)



@app.route('/spots')
def melhores_spots_page():
    file_path = 'melhor_spot_por_level.xlsx'
    df = pd.read_excel(file_path, header=None)

    monstros = df.iloc[1:,1].dropna().tolist()
    base_exp = df.iloc[1:,3].dropna().tolist()
    job_exp = df.iloc[1:,4].dropna().tolist()
    quantidade = df.iloc[1:,5].dropna().tolist()
    mapa = df.iloc[1:,6].dropna().tolist()
    xp_ajustada = df.iloc[1:,7].dropna().tolist()
    nivel_jogador = df.iloc[1:,8].dropna().tolist()
    nivel_monstro = df.iloc[1:,2].dropna().tolist()

    dicionario_ids= 'monstros_e_drops.xlsx'

    def normalizar(texto):
        if not isinstance(texto, str):
            return ""
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').strip().lower()

    def carregar_ids_monstros(caminho_arquivo):
        df = pd.read_excel(caminho_arquivo)
        dicionario = {}

        for _, row in df.iterrows():
            nome = normalizar(str(row['nome_monstro']))
            id_monstro = row['id']
            dicionario[nome] = id_monstro

        return dicionario
    

    def buscar_ids_para_monstros(lista_nomes, dict_ids):
        resultado = []

        for nome in lista_nomes:
            nome_limpo = normalizar(nome)
            id_encontrado = dict_ids.get(nome_limpo)
            resultado.append({
                "nome": nome,
                "id": id_encontrado
            })

        return resultado
    dicionario_ids = carregar_ids_monstros(dicionario_ids)
    
    dados_com_ids = buscar_ids_para_monstros(monstros, dicionario_ids)

    data = list(zip(dados_com_ids,base_exp,job_exp,quantidade,mapa,xp_ajustada,nivel_jogador,nivel_monstro))


    print(data)

    return render_template(
        'spots.html',
        dados = data,
        links=carregar_links(),
)


if __name__ == '__main__':

 app.run(debug=True)


@app.route('/links')
def links_page():
  
    return render_template(
    'links.html',
    links=carregar_links(),
)