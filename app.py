from collections import defaultdict
from flask import Flask
import pandas as pd
import re
import unicodedata
from flask_cors import CORS
from flask import Flask, render_template
from openpyxl import load_workbook

app = Flask(__name__)
CORS(app)


@app.route('/')
def info_page():
    file_path = 'rola.xlsx'
    df = pd.read_excel(file_path, header=None)

    info_essenciais = df.iloc[2:7, 1].dropna().tolist()
    links = df.iloc[10:14, 1].dropna().tolist()


    return render_template(
    'index.html',
    info=info_essenciais,
    links=links,
    )


@app.route('/classes')
def classes_page():
    df = pd.read_excel('rola.xlsx', header=None)
    classes = df.iloc[1:27, 3].dropna().tolist()
    builds = df.iloc[1:29, 4].dropna().tolist()

    wb = load_workbook('rola.xlsx')
    ws = wb["INFORMAÇÕES"]
        
    links = []
    for row in ws.iter_rows(min_row=33, min_col=2, max_col=2):
            cell = row[0]
            if cell.hyperlink:
                links.append(cell.hyperlink.target)
            elif cell.value:
                links.append(cell.value)


    class_builds = [
        {"classe": classes[1], "builds": [builds[1], builds[2]], "link": "","imagem": "assets/classes/feiticeiro.png"}, #Feiticeiro
        {"classe": classes[2], "builds": [builds[3]], "link": links[4],"imagem": "assets/classes/sentinela.png"},# Sentinela
        {"classe": classes[3], "builds": [builds[4]], "link": links[5],"imagem": "assets/classes/sicario.png"},# Sicario
        {"classe": classes[4], "builds": [builds[5]], "link": links[6],"imagem": "assets/classes/arcano.png"},# Arcano
        {"classe": classes[5], "builds": [builds[6], builds[7]], "link": "","imagem": "assets/classes/arcebispo.png"},# Arcebispo
        {"classe": classes[6], "builds": [builds[9], builds[8]], "link": links[3],"imagem": "assets/classes/renegado.png"},# Renegado
        {"classe": classes[7], "builds": [builds[11], builds[10]], "link": "","imagem": "assets/classes/sura.png"},# Shura
        {"classe": classes[8], "builds": [builds[12]], "link": links[1],"imagem": "assets/classes/cavaleiro_runico.png"}, # Cavaleiros Rúnicos
        {"classe": classes[9], "builds": [builds[14], builds[13]], "link": links[2],"imagem": "assets/classes/guardioes_reais.png"},# Guardião Real
        {"classe": classes[10], "builds": [builds[15]], "link": "","imagem": "assets/classes/mecanico.png"},# Mecânico
        {"classe": classes[11], "builds": [builds[16]], "link": "","imagem": "assets/classes/genetico.png"},# Bioquímicos
        {"classe": classes[12], "builds": [builds[17], builds[18]], "link": links[7],"imagem": "assets/classes/trovador.png"},# Trovadores
        {"classe": classes[13], "builds": [builds[19], builds[20]], "link": links[7],"imagem": "assets/classes/musa.png"}, # Musa
    ]
    return render_template('classes.html', 
                           class_builds=class_builds
                           )

@app.route('/rank')
def rank_page():
    df = pd.read_excel('rola.xlsx', header=None)
    rank_tiers = df.iloc[3:, 8].dropna().tolist()
    rank_classes = df.iloc[3:, 9].dropna().tolist()

    print(rank_tiers)

    rank_data = list(zip(rank_tiers, rank_classes))
    return render_template('rank.html', rank_data=rank_data)

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
   


    return render_template(
        'rotas.html',
        rotas_melee=rotas_melee,
        array_quest_melee=array_quest_melee,
        array_builds_formatado = array_builds_formatado,
        rotas_ranged=rotas_ranged,
        array_quest_ranged=array_quest_ranged,
        array_builds_ranged_formatado = array_builds_ranged_formatado
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
    return render_template('items.html', 
                           tabela_items=tabela_items,
                           tabela_items_importantes=tabela_items_importantes,
                           array_items_guardar=tabela_formatada,
                           array_items_n_vender=array_items_n_vender
                           )

@app.route('/monstros')
def monstros_page():
    file_path = 'rola.xlsx'
    df = pd.read_excel(file_path, sheet_name='Monstros + Drop + XP', header=None)

    arquivos = ["item_db_usable.yml", "item_db_equip.yml", "item_db_etc.yml"]

# Função para normalizar nomes
    def normalizar(texto):
        if texto is None:
            return ""
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').strip().lower()

    # Carrega todos os nomes e IDs dos arquivos em um dicionário
    def carregar_ids_em_memoria(arquivos):
        dicionario = {}

        for caminho_arquivo in arquivos:
            try:
                with open(caminho_arquivo, 'r', encoding='latin-1') as file:
                    bloco = []
                    for linha in file:
                        if linha.strip().startswith('- Id:'):
                            if bloco:
                                nome, id_item = extrair_nome_id(bloco)
                                if nome and id_item:
                                    dicionario[nome] = id_item
                            bloco = [linha]
                        else:
                            bloco.append(linha)

                    # Processa o último bloco
                    nome, id_item = extrair_nome_id(bloco)
                    if nome and id_item:
                        dicionario[nome] = id_item

            except Exception as e:
                print(f"Erro ao processar {caminho_arquivo}: {e}")

        return dicionario

    # Extrai nome e ID de um bloco de YAML
    def extrair_nome_id(bloco):
        nome = None
        id_item = None
        for linha in bloco:
            if "AegisName:" in linha:
                nome = normalizar(linha.split(":", 1)[1].strip())
            if "Id:" in linha:
                id_item = linha.split(":", 1)[1].strip()
        return nome, id_item
    def limpar_item(item):
        item = item.strip()
        item = re.sub(r'\[\d+\]', '', item)  # Remove sufixos como [1], [2]
        return item.strip()

    def buscar_ids_itens_para_monstro(itens_str, dict_ids):
        nomes_itens = [limpar_item(item) for item in itens_str.split(',') if item.strip()]
        resultado = []

        for nome in nomes_itens:
            nome_norm = normalizar(nome).replace(' ', '_')
            id_encontrado = None

            for chave, id_item in dict_ids.items():
                if nome_norm in chave:
                    id_encontrado = id_item
                    break

            resultado.append({
                "nome": nome,
                "id": id_encontrado
            })

        return resultado

    # ------------ Leitura e processamento do DataFrame original ------------

    # Supondo que 'df' já esteja carregado com os dados da planilha
    df_monstros = pd.DataFrame({
        "id": df.iloc[1:, 0],
        "nome": df.iloc[1:, 1],
        "level": df.iloc[1:, 2],
        "hp": df.iloc[1:, 3],
        "exp_base": df.iloc[1:, 4],
        "exp_job": df.iloc[1:, 5],
        "itens": df.iloc[1:, 7],
        "mapa": df.iloc[1:, 9]
    })

    # Agrupa monstros com o mesmo nome e junta os mapas
    df_agrupado = df_monstros.groupby("nome", as_index=False).agg({
        "id": "first",
        "level": "first",
        "hp": "first",
        "exp_base": "first",
        "exp_job": "first",
        "itens": "first",
        "mapa": lambda x: ', '.join(sorted(set(str(i).strip() for i in x if pd.notna(i))))
    })

    # Carrega os IDs de itens em memória
    dicionario_ids = carregar_ids_em_memoria(arquivos)

    # Adiciona a coluna com os nomes de itens e seus respectivos IDs
    df_agrupado["itens_com_id"] = df_agrupado["itens"].apply(
        lambda x: buscar_ids_itens_para_monstro(x, dicionario_ids)
    )

    # Transforma em lista de tuplas para enviar ao Jinja
    data = df_agrupado.to_dict(orient='records')


    return render_template('monstros.html', data=data)

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

    print(tabela_unificada_terceira)


    return render_template('timer.html', data=data,
                            tabela_unificada_segunda_classe = tabela_unificada.to_dict(orient='records'),
                            tabela_unificada_transclasse = tabela_unificada_tranclasse.to_dict(orient='records'),
                            tabela_unificada_terceira = tabela_unificada_terceira.to_dict(orient='records')
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
         {"dados": dados[0], "links": links[0],"imagem": "assets/classes/cavaleiro_runico.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "on"},
         {"dados": dados[1], "links": links[1],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},
         {"dados": dados[2], "links": links[2],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},
         {"dados": dados[3], "links": links[3],"imagem": "assets/classes/sicario.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[4], "links": links[4],"imagem": "assets/classes/arcebispo.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[5], "links": links[5],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[6], "links": links[6],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"}, 
         {"dados": dados[7], "links": links[7],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[8], "links": links[8],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "off"},   
         {"dados": dados[9], "links": links[9],"imagem": "assets/classes/arcano.png","imagem_gif": "assets/classes/gifs/cavaleiro_runico.gif","status": "on"},
         {"dados": dados[10], "links": links[10],"imagem": "assets/classes/hunter.gif","imagem_gif": "assets/classes/gifs/trovador.gif","status": "on"},   
    ]

    return render_template('streamers.html', data=dados_links_imagens,
                        
                            )
if __name__ == '__main__':
    app.run(debug=True)