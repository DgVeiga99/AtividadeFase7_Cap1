#============================================================================================================
#                    ATIVIDADE FASE 7 - Capítulo 1 - A consolidação de um sistema
#============================================================================================================
#                                   SISTEMA DE CONSULTA FASES
#------------------------------------------------------------------------------------------------------------
"""
# Autor.....: Diego Nunes Veiga
# RM........: 560658
# Turma.....: Graduação - 1TIAOR
# Data......: 17/05/2025
# Assunto...: SISTEMA DE COLSULTA FASES
# Função....: Realizar a conexão com o banco de dados possibilitando cadastrar, consultar, atualizar e excluir
              lotes das sementes colocadas para estoque e gerar um relatório aprovando ou não o lote.
"""

#============================================================================================================
#                            OBJETIVO DO DESENVOLVIMENTO DO SOFTWARE
#============================================================================================================

#   Aprimorar a dashboard da Fase 4 (realizada preferencialmente em Python), integrando os serviços de cada Fase (1, 2, 3 e 6)
# usando botões ou comandos de terminal, mas de modo que todos os programas estejam em uma única pasta de projeto no seu
# VS Code ou outra IDE de desenvolvimento que o grupo tem preferência. Caso alguma entrega entre as Fases 1 e 6 não tenha
# sido feita, é a sua chance de tentar fazê-la e pontuar por isso.

#   Gerar um serviço de alerta aproveitando a infraestrutura AWS criada na Fase 5 para monitorar ou os sensores das Fases 1 ou 3
# ou, ainda, os resultados das análises visuais da visão computacional da Fase 6, isto é, implemente um serviço de mensageria
# na AWS que integre a dashboard geral da fazenda, sugerindo aos funcionários ações corretivas a partir dos dados das Fases 1, 3 ou 6.
# Os funcionários da fazenda precisam receber um e-mail ou um SMS com os devidos alertas e indicando as ações. As ações devem
# ser definidas pelo grupo.

#============================================================================================================
#                                   BIBLIOTECAS, LISTAS E DICIONÁRIOS
#============================================================================================================

# Importação das bibliotecas
import os
import io
import oracledb
import pandas as pd
import numpy as np
import streamlit as st
from streamlit import progress
import time
import torch
import tempfile
import pathlib

#Usuário para acessar o banco de dados
user = "RM560658"
password = "010199"
server = 'oracle.fiap.com.br:1521/ORCL'


# Lista de dados da laranja
padraolaranja = [["Adubo Nitrogenado","Fósforo","Potássio","Boro","Zinco","Fungicida"],
             [150, 50, 100, 1.5, 4, 250],
             ["kg","kg","kg","kg","kg","mL"]]

# Variáveis do processo
padrãorelatorio = (98.0, 90.0, 85.0, 10.0, 0.5, 500)

# Submenu de apresentação do titulo e descrição de função da página
submenu = [["📊 Visão Geral do Projeto","🌱 Estimativa do Consumo de Insumos","🗃️ Banco de Sementes",
            "💧 IoT e Irrigação Inteligente","🛰️ Visão Computacional"],
           ["""
        Bem-vindo ao **Sistema Integrado de Gestão para o Agronegócio - Fase 7**.
    
        Esta aplicação consolida todas as entregas das Fases 1 a 6 em um ambiente único e interativo, permitindo o gerenciamento eficiente da produção agrícola com apoio de tecnologias modernas como **IoT**, **Machine Learning**, **Visão Computacional** e **Cloud Computing**.
    
        ###  Funcionalidades integradas:
        - **Fase 1 – Insumos e Área de Plantio**  
          Cálculo de área plantada e estimativa de insumos com base na cultura selecionada.
        - **Fase 2 – Banco de Dados**  
          Conexão e manipulação de dados em um banco relacional com estrutura organizada.
        - **Fase 3 – IoT e Automação Inteligente**  
          Simulação e controle de sensores (umidade, pH, nutrientes) com lógica de irrigação automática.
        - **Fase 4 – Dashboard Interativa com Data Science**  
          Visualização de dados, gráficos e predições baseadas em aprendizado de máquina com interface Streamlit.
        - **Fase 5 – Integração com AWS**  
          Segurança dos dados e sistema de alerta por e-mail ou SMS utilizando AWS SNS.
        - **Fase 6 – Visão Computacional**  
          Análise de imagens via redes neurais (YOLO ou CNN) para detecção de anomalias nas plantações.
    
        ---
        ###  Objetivo Final
        Oferecer uma plataforma unificada e escalável que possa ser adaptada para qualquer setor produtivo, com foco em **automação, análise de dados e tomada de decisão inteligente** no agronegócio.
        """,
            "Realize o cálculo automatizado dos insumos agrícolas necessários para o cultivo de laranjas com base na área plantada. A ferramenta utiliza fórmulas "
            "pré-definidas para estimar a quantidade ideal de adubos e defensivos, oferecendo precisão no planejamento agrícola.",
            "Gerencie de forma integrada os lotes de sementes armazenadas, com funcionalidades para cadastrar, consultar, atualizar, excluir e gerar relatórios completos. A base de dados é "
            "conectada a um banco Oracle e permite avaliação da qualidade com base em critérios técnicos.",
            "Monitore os principais parâmetros do solo (umidade, pH, nutrientes) e controle o acionamento da bomba de irrigação de forma automatizada via ESP32. O sistema registra os dados coletados "
            "em tempo real, proporcionando uma visão atualizada do estado da plantação.",
            "Realize inspeções visuais automatizadas na lavoura com apoio de redes neurais YOLOv5. O sistema permite o upload de imagens e detecta automaticamente pragas, doenças ou condições indesejadas"
            " nas laranjas, exibindo alertas em caso de não conformidades."]
           ]


#============================================================================================================
#                                       PROCEDIMENTOS E FUNÇÕES
#============================================================================================================


# Gerenciamento da seleção do menu
def MenuLateral():

    with st.sidebar:
        st.title("MENU LATERAL")
        menu =["Visão Geral","Insumos","Banco de Sementes","Automação IoT","Visão Computacional"]

        if "fase_selecionada" not in st.session_state:
            st.session_state.fase_selecionada = menu[0]

        for i in menu:
            if st.button(i):
                st.session_state.fase_selecionada = i

        return st.session_state.fase_selecionada


# Define estilo dos botões
def EstiloBotao() -> None:
    st.markdown("""
        <style>
        div.stButton > button {
            width: 100%;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)


# Realiza conexão com o servidor do banco de dados
def ConexaoServidor(user, password, server) -> bool:
    global conn,bd_comando

    try:
        conn = oracledb.connect(user=user, password=password, dsn=server)
        bd_comando = conn.cursor()

    except Exception:
        conexao = False
    else:
        conexao = True

    return conexao


# Apresentação do Submenu
def SubMenu(titulo: dict, descricao: dict) -> None:

    st.title(titulo)
    st.markdown(descricao)
    st.divider()


# Visualização da Barra de progresso
def BarraProgresso() -> None:

    progresso = progress(0)
    for i in range(100):
        time.sleep(0.01)
        progresso.progress(i+1)


# Cálculo da área de plantio e insumos consumidos
def ConsumoInsumo(raio:int) -> None:

     # Cálculo da área total
    area = np.pi * (raio ** 2)
    hectares = area / 10000
    fileiras = round(area / 7)

    # Apresentação dos resultados
    st.markdown(f"Para o cultivo de **{area:.2f} m²**, ou **{hectares:.2f} hectares**, dedicadas para esta cultura precisamos de:")
    st.markdown(f"- **{fileiras} fileiras** para o cultivo ideal")

    for i in range(len(padraolaranja[0])):
        st.markdown(f"- **{padraolaranja[1][i] * hectares:.2f} {padraolaranja[2][i]}** de {padraolaranja[0][i]}")


# Gerenciamento da seleção do menu do banco de dados
def MenuSementes():
    menu = ["Inserir lote", "Atualizar lote", "Excluir lote", "Exibir registros", "Excluir registros","Relatório"]
    cols = st.columns(len(menu))

    if "cmd_selecionado" not in st.session_state:
        st.session_state.cmd_selecionado = menu[0]

    for i in range(len(menu)):
        with cols[i]:
            if st.button(menu[i]):
                st.session_state.cmd_selecionado = menu[i]

    return st.session_state.cmd_selecionado


# Cadastro do novo lote no banco de dados
def NovoLoteSemente():
    try:
        st.write("Preencha os dados para registro no sistema")
        L = st.number_input("Lote: ",min_value=0)
        DC = st.date_input("Data de colheita: ")

        # Separação em duas colunas de dados
        c1, c2 = st.columns(2)
        with c1:
            Pu = st.slider("Pureza(%): ",min_value=0,max_value=100)
            G= st.slider("Taxa de Germinação(%): ",min_value=0,max_value=100)
            V = st.slider("Viabilidade(%): ",min_value=0,max_value=100)

        with c2:
            U = st.slider("Teor de Umidade(%): ",min_value=0,max_value=100)
            S = st.slider("Sanidade(%): ",min_value=0,max_value=100)
            Ps = st.number_input("Peso Mil sementes(g): ",min_value=0)

        # Confirma o processo escolhido
        if st.button("ARMAZENAR"):

            bd_comando.execute(f""" INSERT INTO sementes (lote,datacolheita,pureza,germinacao,viabilidade,umidade,sanidade,peso)
                                VALUES ('{L}','{DC}','{Pu}','{G}','{V}','{U}','{S}','{Ps}') """)
            conn.commit()
            BarraProgresso()
            st.success("Os dados foram armazenados...")

    except Exception as e:
        st.error("Erro de transferência para o banco de dados")
        st.exception(e)


# Procura lote para realizar a atualização
def ProcuraLoteSemente() -> None:
    try:
        cmd = st.number_input("Qual lote deseja buscar?:", min_value=0)

        if st.button("CONFIRMAR"):
            bd_comando.execute("SELECT * FROM sementes WHERE lote = {}".format(cmd))
            data = bd_comando.fetchall()

            BarraProgresso()

            if not data:
                st.warning(" Nenhum registro encontrado!")
                st.session_state.lote_encontrado = None
            else:
                st.session_state.lote_encontrado = str(cmd)

    except Exception as e:
        st.error("Erro na consulta.")
        st.exception(e)
        st.session_state.lote_encontrado = None



# Atualiza lote existente
def AtualizaLoteSemente(lote: str) -> None:
    try:

        st.markdown("Preencha os dados para atualizar o **Lote {}** no sistema".format(lote))
        DC = st.date_input("Data de colheita: ")

        # Separação em duas colunas de dados
        c1, c2 = st.columns(2)
        with c1:
            Pu = st.slider("Pureza(%): ", min_value=0, max_value=100)
            G = st.slider("Taxa de Germinação(%): ", min_value=0, max_value=100)
            V = st.slider("Viabilidade(%): ", min_value=0, max_value=100)

        with c2:
            U = st.slider("Teor de Umidade(%): ", min_value=0, max_value=100)
            S = st.slider("Sanidade(%): ", min_value=0, max_value=100)
            Ps = st.number_input("Peso Mil sementes(g): ", min_value=0)


        # Confirma o processo escolhido
        if st.button("ATUALIZAR"):

            bd_comando.execute(f"UPDATE sementes SET datacolheita='{DC}', pureza='{Pu}', germinacao='{G}', viabilidade='{V}', umidade='{U}', sanidade='{S}', peso='{Ps}' WHERE lote = '{lote}'")
            conn.commit()
            BarraProgresso()
            st.success("Os dados foram atualizados...")

    except Exception as e:
        st.error("Ocorreu um erro ao atualizar o lote.")
        st.exception(e)


# Comando para excluir lote
def ExcluiDadoSemente(lote: str) -> None:
    try:
        # Confirma o processo escolhido
        if st.button("EXCLUIR LOTE"):

            bd_comando.execute(f"DELETE FROM sementes WHERE id ='{lote}'")
            conn.commit()
            BarraProgresso()
            st.success("O registro foi apagado")

    except Exception as e:
        st.error("Erro de transferência de dados")
        st.exception(e)


# Apresenta lista de todos os lotes registrados
def ListaCompletaSemente() -> None:
    lista = []
    bd_comando.execute('SELECT * FROM sementes')
    tabela = bd_comando.fetchall()

    for dt in tabela:
        lista.append(dt)

    # ordena a lista
    lista = sorted(lista)

    # Formatação para apresentar todas a tabela sem exceção
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', None)

    # Gera um DataFrame com os dados da lista utilizando o Pandas
    DadosFormatados = pd.DataFrame.from_records(lista, columns=["ID","Lote","Data de colheita","Pureza(%)","Germinação(%)","Viabilidade(%)","Umidade(%)","Sanidade(%)","Pesos(g)"], index='ID')

    if DadosFormatados.empty:
        st.warning("Nenhum registro encontrado!\n")
    else:
        st.dataframe(DadosFormatados)


# Exclui todos os registros existentes no banco de dados
def ExcluiCompletoSemente() -> None:
    st.write("!!!!! O COMANDO IRA EXCLUIR SEU BANCO DE DADOS POR COMPLETO !!!!!")
    st.write("Confirma a exclusão?")

    # Comando de exclusão de todos os registros existentes
    if st.button("SIM"):
        bd_comando.execute("DELETE FROM sementes")
        conn.commit()
        bd_comando.execute(" ALTER TABLE sementes MODIFY(ID GENERATED AS IDENTITY (START WITH 1)) ")
        conn.commit()

        BarraProgresso()
        st.success("\nTodos os registros foram excluídos!\n")


# Cálculo de aprovação e reprovação do lote
def CalculoAprovaSemente(lista: list,ref: tuple) -> None:
    resultado = []

    # Realiza comparação dos valores no banco com os padrões
    for i in range(3, len(lista)):
        index = i - 3
        aprova = False

        match i:
            case 3|4|5:
                aprova = lista[i] >= ref[index]

            case 6|7:
                aprova = lista[i] <= ref[index]

            case 8:
                zonamax = ref[index] * 1.05
                zonamin = ref[index] * 0.95
                aprova = zonamin <= lista[i] <= zonamax

        resultado.append("Aprovado" if aprova else "Reprovado")

    return resultado


# Cria o relatório em TXT
def RelatorioTXTSemente(lote: str, dados: list, result: list, ref: tuple) -> None:

    #Construção do relatorio do lote
    conteudo = (
        f"{'=' * 20} RELATÓRIO DE QUALIDADE {'=' * 20}\n"
        "Relatório de qualidade das sementes obtemos os valores que estão aprovado e reprovados conforme padrão\n"
        "VALORES PADRÕES:\n"
        f"\t1. Pureza: acima de {ref[0]} %\n"
        f"\t2. Taxa de Germinação: acima de {ref[1]} %\n"
        f"\t3. Viabilidade: acima de {ref[2]} %\n"
        f"\t4. Teor de Umidade: menor ou igual a {ref[3]} %\n"
        f"\t5. Sanidade: menor ou igual a {ref[4]} %\n"
        f"\t6. Peso Mil sementes: padrão {ref[5]} (g) com tolerância de +/-5%\n"
        f"{'-' * 60}\n\n"
        f"ID...............: {dados[0]} (Número banco de dados)\n"
        f"LOTE.............: {dados[1]}\n"
        f"DATA COLHEITA....: {dados[2]}\n"
        f"\t1. Pureza: {dados[3]} %                  -> {result[0]} conforme padrão\n"
        f"\t2. Taxa de Germinação: {dados[4]} %      -> {result[1]} conforme padrão\n"
        f"\t3. Viabilidade: {dados[5]} %             -> {result[2]} conforme padrão\n"
        f"\t4. Teor de Umidade: {dados[6]} %         -> {result[3]} conforme padrão\n"
        f"\t5. Sanidade: {dados[7]} %                -> {result[4]} conforme padrão\n"
        f"\t6. Peso Mil sementes: {dados[8]} g       -> {result[5]} conforme padrão\n"
    )

    st.success("Relatório gerado com sucesso e pronto para download")

    # Comando para realizar o download do código
    buffer = io.BytesIO(conteudo.encode("utf-8"))
    st.download_button(
        label="📥 Baixar relatório",
        data=buffer,
        file_name=f"RelatorioLote{lote}.txt",
        mime="text/plain"
    )


# Rotina para geração do relatório de lote
def GeraRelatorioSemente(lote: str,ref: tuple) -> None:
    lista = []
    bd_comando.execute(f"SELECT * FROM sementes WHERE lote = '{lote}'")
    tabela = bd_comando.fetchall()

    for dt in tabela:
        lista.append(dt)

    # Converte os dados obtidos de lista + tupla para lista
    lista = sorted(lista)
    dados = list(lista[0])

    # Chamada do cálculo para comparar os itens aprovados
    result = CalculoAprovaSemente(dados,ref)

    #Chamada para realizar o relatorio txt
    RelatorioTXTSemente(lote,dados,result,padrãorelatorio)


# Apresenta lista de todos os lotes registrados
def ListaCompletaPlantacao() -> None:
    lista = []
    bd_comando.execute('SELECT * FROM plantacao')
    tabela = bd_comando.fetchall()

    for dt in tabela:
        lista.append(dt)

    # ordena a lista
    lista = sorted(lista)

    # Formatação para apresentar todas a tabela sem exceção
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', None)

    # Gera um DataFrame com os dados da lista utilizando o Pandas
    DadosFormatados = pd.DataFrame.from_records(lista, columns=["ID","Data registro","Fósforo","Potássio","Umidade(%)","pH Solo","Bomba água"], index='ID')

    if DadosFormatados.empty:
        st.warning("Nenhum registro encontrado!\n")
    else:
        st.dataframe(DadosFormatados)


# Chama modelo treinado do Yolov5
def ModeloYolo(imagem):

    # Corrige incompatibilidade com PosixPath no Windows (sugerido pelo ChatGPT)
    pathlib.PosixPath = pathlib.WindowsPath

    model = torch.hub.load("ultralytics/yolov5", 'custom', path='best.pt', force_reload=True)
    result = model(imagem)
    return result


# Apresenta resultado da Visão Computacional
def ResultadoVisao(results):

    c1,c2 = st.columns(2)

    with c1:
        st.image(results.render()[0],use_container_width=True)

    with c2:
        st.markdown("### Classes detectadas:")
        df = results.pandas().xyxy[0][['name', 'confidence']]
        df.columns = ['Classe', 'Confiança']
        st.dataframe(df, use_container_width=True)


# Realiza o teste da visão computacional do
def VisaoComputacional() -> None:
    # Interface de upload
    arquivo = st.file_uploader("📸 Faça o upload de uma imagem da lavoura (laranja)",
                                     type=["jpg", "png", "jpeg"])

    # Carregamento da imagem para teste de visão
    if arquivo is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(arquivo.read())
            temp_image_path = temp_file.name
        st.success("Imagem carregada com sucesso.")


        if st.button("ANALISAR IMAGEM"):
            with st.spinner("Visão Computacional em processamento..."):
                resultado = ModeloYolo(temp_image_path)
                ResultadoVisao(resultado)




#-------------------------------------------------------------------------------------------------------

#============================================================================================================
#                                          PROGRAMA PRINCIPAL
#============================================================================================================

# Título da dashboard
st.set_page_config(page_title="Sistema Agronegócio - Fase 7", layout="wide")

# Aplica estilo aos botões
EstiloBotao()

#Conexão com o servidor
conexao = ConexaoServidor(user,password,server)

# Controle do Menu lateral com botões
fase = MenuLateral()

# Escolha do menu conforme comando do usuário
match fase:

    # =================================== Visão Geral =============================================
    case "Visão Geral":
        SubMenu(submenu[0][0],submenu[1][0])

    # ================================ Cálculo de Insumos ========================================
    case "Insumos":
        # Apresentação da seleção da página
        SubMenu(submenu[0][1], submenu[1][1])

        # Entrada do valores
        cultura = st.selectbox("Escolha a tipo de cultura", ["Laranja"])
        raio = st.number_input("raio da plantação (m):", min_value=0)
        st.write("📏: {} m".format(raio))

        # Confirma o raio para calculo
        if st.button("CALCULAR"):
            ConsumoInsumo(raio)


    # ================================ Banco de dados ========================================
    case "Banco de Sementes":
        # Apresentação da seleção da página
        SubMenu(submenu[0][2], submenu[1][2])

        # Status de conexão do banco de dados
        if conexao == True:

            #Seleção do comando CRUD para o banco de sementes
            menusem = MenuSementes()
            match menusem:

                # ------------------------------- Inserir lote ------------------------------------
                case "Inserir lote":
                    NovoLoteSemente()

                # ------------------------------- Atualizar lote ----------------------------------
                case "Atualizar lote":
                    ProcuraLoteSemente()
                    if st.session_state.get("lote_encontrado"):
                        AtualizaLoteSemente(st.session_state.lote_encontrado)

                # ------------------------------- Excluir lote ------------------------------------
                case "Excluir lote":
                    ProcuraLoteSemente()
                    if st.session_state.get("lote_encontrado"):
                        ExcluiDadoSemente(st.session_state.lote_encontrado)

                # ----------------------------- Exibir registros ----------------------------------
                case "Exibir registros":
                    ListaCompletaSemente()

                # ----------------------------- Excluir registros ---------------------------------
                case "Excluir registros":
                    ExcluiCompletoSemente()

                # ----------------------------- Relatório ---------------------------------
                case "Relatório":
                    ProcuraLoteSemente()
                    if st.session_state.get("lote_encontrado"):
                        GeraRelatorioSemente(st.session_state.lote_encontrado,padrãorelatorio)

        # Falha na conexão do banco de dados
        else:
            st.error("Falha na conexão com o banco de dados")


    # ================================ Automação inteligente ========================================
    case "Automação IoT":
        # Apresentação da seleção da página
        SubMenu(submenu[0][3], submenu[1][3])
        ListaCompletaPlantacao()

    # ================================ Inserir lote ========================================
    case "Visão Computacional":
        # Apresentação da seleção da página
        SubMenu(submenu[0][4], submenu[1][4])
        VisaoComputacional()


# Finalização da página
st.divider()
st.caption("Desenvolvido por Diego Veiga - Projeto FIAP Fase 7")






