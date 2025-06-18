# Wiki-latam

Wiki-latam é um sistema web desenvolvido com Flask que combina engenharia de dados e programação web para organizar e apresentar informações do jogo Ragnarok Online de forma acessível, estruturada e responsiva.

Este projeto segue o padrão ETL (Extract, Transform, Load):

- 🔍 Extração: Leitura de dados brutos em planilhas .xlsx com informações de monstros, instâncias, itens e atributos do jogo.

- 🛠️ Transformação: Normalização dos nomes, associação de IDs, enriquecimento com links externos e estruturação de dados para consumo web.

- 🚀 Carregamento: Renderização dos dados em páginas HTML dinâmicas com Jinja2, permitindo consultas organizadas e visuais amigáveis.

🎯 Objetivo do Projeto
O Wiki-latam surgiu com o propósito de automatizar e simplificar a consulta e análise de dados complexos do universo de Ragnarok Online, utilizando uma abordagem de engenharia de dados aplicada a jogos.

Trata-se de uma ferramenta que pode ser usada por:
- Jogadores que desejam otimizar rotas e farm de instâncias
- Desenvolvedores e entusiastas interessados em visualização de dados em jogos
- Estudantes ou profissionais de dados que queiram explorar projetos ETL com propósito prático

## 1 - 📌 Funcionalidades

- ✅ Listagem dos ultimos videos relacionados ao tema ragnarok online.
- 📊 Visualização de tabelas organizadas que permitem ao usuário ter acesso a diversas informações.
- 🌈 Animações e efeitos visuais para uma melhor experiência do usuário.
- 📁 Leitura e integração com arquivos .xlsx para alimentar os dados.


## 2 - 🛠 Tecnologias Utilizadas

| Camada     | Tecnologias                                                                 |
|------------|------------------------------------------------------------------------------|
| Backend    | Python 3, Flask                                                              |
| Frontend   | HTML5, CSS3, Jinja2                                                          |
| Dados      | Pandas, OpenPyXL                                                             |
| ETL        | Normalização com Unicodedata, mapeamento de IDs, enriquecimento com links   |

## 3 - 📂 Estrutura do Projeto

```bash
wiki-latam/
│
├── app.py                  # Arquivo principal com as rotas e lógica do Flask
├── templates/              # Templates HTML com Jinja
│   ├── base.html
│   ├── index.html
│   └── ...
├── static/                 # CSS, imagens e scripts
├── data/                   # Arquivos .xlsx com os dados utilizados
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
````

## 4 - 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter os seguintes itens instalados no seu computador:
- [Python 3.10+](https://www.python.org/downloads/) (versão 3.10 ou superior).

### Passo a Passo

#### 1. Clone o repositório

```bash
git clone https://github.com/olvictor/wiki-latam.git
cd wiki-latam
````
#### 2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate
````
#### 3. Instale as dependências:

```bash
pip install -r requirements.txt
````

#### 4. Execute o app Flask:

```bash
flask run
````

Após isso, o Flask irá iniciar o servidor e você pode acessar a aplicação no navegador, normalmente em http://127.0.0.1:5000/.
