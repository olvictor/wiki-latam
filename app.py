from collections import defaultdict
from flask import Flask
import pandas as pd
import re
import yaml
import unicodedata
from flask_cors import CORS
from flask import Flask, render_template
app = Flask(__name__)
CORS(app)


@app.route('/')
def info_page():
     # Lê o arquivo Excel
    file_path = 'rola.xlsx'
    df = pd.read_excel(file_path, header=None)
    xls = pd.ExcelFile(file_path)

    # Extrair as seções manualmente
    info_essenciais = df.iloc[2:7, 1].dropna().tolist()
    links = df.iloc[10:14, 1].dropna().tolist()
    login_rewards = df.iloc[18:, 1].dropna().tolist()

    classes = df.iloc[1:, 2].dropna().tolist()
    builds = df.iloc[1:, 3].dropna().tolist()
    amigos = df.iloc[1:18, 4].dropna().tolist()

    rank_tiers = df.iloc[3:, 6].dropna().tolist()
    rank_classes = df.iloc[3:, 7].dropna().tolist()
    # rotas_melee = df.iloc[2:20, 4].dropna().tolist()    
    # print(rotas_melee)
    class_builds = [
        (classes[1], [builds[1],builds[2]]), # Feiticeiro
        (classes[2], [builds[3]]), # Sentinela
        (classes[3], [builds[4]]), # Sicario
        (classes[4], [builds[5]]), # Arcano
        (classes[5], [builds[6],builds[7]]), # Arcebispo
        (classes[6], [builds[9],builds[8]]), # Renegado
        (classes[7], [builds[11], builds[10]]), # Shura
        (classes[8], [builds[12]]), # Cavaleiros Rúnicos
        (classes[9], [builds[14],builds[13]]), # Guardião Real
        (classes[10], [builds[15]]), # Mecânico
        (classes[11], [builds[16]]),# Bioquímicos	
        (classes[12], [builds[17],builds[18]]), # Trovadores
        (classes[13], [builds[19],builds[20]]), # Musa
    ]

    # Combinar os dados do rank com zip e enviar como lista
    rank_data = list(zip(rank_tiers, rank_classes))
    # class_builds = list(zip(classes, builds))
  
    # Extrair dados da planilha 'ROTAS MELEE + DICAS'

    df_melee = pd.read_excel(file_path, sheet_name='ROTAS MELEE + DICAS', header=None)
    melee_raw = df_melee.iloc[2:,1].dropna().tolist()

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
    xls = pd.ExcelFile(file_path)

    links = df.iloc[10:14, 1].dropna().tolist()
    
    links_com_indices = list(enumerate(xls.sheet_names))

    return render_template(
    'index.html',
    info=info_essenciais,
    links=links,
    login=login_rewards,
    class_builds=class_builds,
    amigos=amigos,
    rank_data=rank_data,
    rotas_melee=rotas_melee,
    menus=links_com_indices
    )


@app.route('/classes')
def classes_page():
    df = pd.read_excel('rola.xlsx', header=None)
    classes = df.iloc[1:, 2].dropna().tolist()
    builds = df.iloc[1:, 3].dropna().tolist()
  

    class_builds = [
        (classes[1], [builds[1],builds[2]]), # Feiticeiro
        (classes[2], [builds[3]]), # Sentinela
        (classes[3], [builds[4]]), # Sicario
        (classes[4], [builds[5]]), # Arcano
        (classes[5], [builds[6],builds[7]]), # Arcebispo
        (classes[6], [builds[9],builds[8]]), # Renegado
        (classes[7], [builds[11], builds[10]]), # Shura
        (classes[8], [builds[12]]), # Cavaleiros Rúnicos
        (classes[9], [builds[14],builds[13]]), # Guardião Real
        (classes[10], [builds[15]]), # Mecânico
        (classes[11], [builds[16]]),# Bioquímicos	
        (classes[12], [builds[17],builds[18]]), # Trovadores
        (classes[13], [builds[19],builds[20]]), # Musa
    ]
    return render_template('classes.html', class_builds=class_builds)

@app.route('/rank')
def rank_page():
    df = pd.read_excel('rola.xlsx', header=None)
    rank_tiers = df.iloc[3:, 6].dropna().tolist()
    rank_classes = df.iloc[3:, 7].dropna().tolist()

    rank_data = list(zip(rank_tiers, rank_classes))
    return render_template('rank.html', rank_data=rank_data)

@app.route('/rotas')
def rotas_page():
    df_melee = pd.read_excel('rola.xlsx', sheet_name='ROTAS MELEE + DICAS', header=None)
    melee_raw = df_melee.iloc[2:,1].dropna().tolist()
    quest_melee =  df_melee.iloc[:,2].dropna().tolist() 
    builds_melee = df_melee.iloc[:,3].dropna().tolist() 

    df_ranged = pd.read_excel('rola.xlsx', sheet_name='ROTAS RANGED + DICAS', header=None)
    ranged_raw = df_ranged.iloc[2:,1].dropna().tolist()
    quest_ranged =  df_ranged.iloc[1:,2].dropna().tolist() 
    builds_ranged = df_ranged.iloc[:,3].dropna().tolist() 

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
        ("Equipamentos  " + quest_melee[1]),
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
    

    #ROTAS RANGED
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
    items = df.iloc[3:,1]
    utilizar = df.iloc[3:,2]
    arquivo = ["item_db_usable.yml","item_db_equip.yml","item_db_etc.yml"]
    
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

    print(imagens_items_importantes)
    tabela_items_importantes = list(zip(items_importantes,items_importantes_local,imagens_items_importantes))
    ###### items para o futuro #######

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


    # # Exemplo de uso:
    # nome = "Poção de Guyak"

    # item_encontrado = buscar_ids_por_nome_em_arquivos(nome, arquivo)

    # if item_encontrado:
    #     print(item_encontrado)
    # else:
    #     print("Item não encontrado.")

    return render_template('items.html', 
                           tabela_items=tabela_items,
                           tabela_items_importantes=tabela_items_importantes,
                           array_items_guardar=tabela_formatada
                           )


if __name__ == '__main__':
    app.run(debug=True)