# 🌾 Sistema Integrado de Gestão Agrícola – Fase 7 (FIAP)

## 📌 Objetivo Geral

Este projeto consolida as entregas das Fases 1 a 6 em uma única aplicação interativa e funcional, construída com Python e Streamlit. A aplicação visa modernizar o monitoramento agrícola, integrando controle de insumos, banco de sementes, sensores, análise visual por visão computacional e alertas automatizados via AWS.

O sistema proporciona uma plataforma única para análise, tomada de decisão e resposta a eventos críticos no ambiente de cultivo.

---


---

## 🎯 Escopo da Atividade – Fase 7

Este projeto tem como objetivos principais:

- Aprimorar a dashboard da Fase 4 (realizada preferencialmente em Python), integrando os serviços de cada Fase (1, 2, 3 e 6)
  usando botões ou comandos de terminal, mas de modo que todos os programas estejam em uma única pasta de projeto no seu
  VS Code ou outra IDE de desenvolvimento que o grupo tem preferência. Caso alguma entrega entre as Fases 1 e 6 não tenha
  sido feita, é a sua chance de tentar fazê-la e pontuar por isso.

- Gerar um serviço de alerta aproveitando a infraestrutura AWS criada na Fase 5 para monitorar os sensores das Fases 1 ou 3
  ou, ainda, os resultados das análises visuais da visão computacional da Fase 6, isto é, implementar um serviço de mensageria
  na AWS que integre a dashboard geral da fazenda, sugerindo aos funcionários ações corretivas a partir dos dados das Fases 1, 3 ou 6.
  Os funcionários da fazenda precisam receber um e-mail ou um SMS com os devidos alertas e indicando as ações. As ações devem
  ser definidas pelo grupo.


## 🔄 Funcionalidades por Fase

| Fase | Integração no Software |
|------|-------------------------|
| **Fase 1 – Insumos** | Cálculo da área de plantio e estimativa de insumos (fertilizantes e defensivos), com base no raio informado pelo usuário |
| **Fase 2 – Banco de Dados** | CRUD completo em um banco Oracle: cadastro, consulta, atualização, exclusão e geração de relatório dos lotes de sementes |
| **Fase 3 – IoT e Automação** | Visualização de dados da plantação simulada com sensores de fósforo, potássio, umidade e pH, incluindo acionamento de bomba |
| **Fase 4 – Dashboard Interativa** | Interface em Streamlit, com menu lateral dinâmico, campos reativos, e visualização integrada por fases |
| **Fase 5 – AWS SNS (em implementação)** | Envio de alertas por e-mail quando parâmetros de sensores estão fora do padrão (ex: potássio baixo e pH < 5.5) |
| **Fase 6 – Visão Computacional (YOLOv5)** | Análise de imagens via rede YOLO para detectar pragas ou falhas visuais nas plantações, com retorno visual interativo |

---

## 🧰 Bibliotecas Necessárias

Para rodar o sistema corretamente, utilize o ambiente virtual e instale os seguintes pacotes:

```bash
# Criação e ativação do ambiente virtual
python -m venv .venv
# Ativação no Windows
.venv\Scripts\activate
# Ativação no Unix/macOS
source .venv/bin/activate

# Instalação das bibliotecas essenciais
pip install oracledb pandas numpy streamlit torch opencv-python seaborn
```

> O modelo YOLOv5 é carregado com `torch.hub` e requer conexão com a internet no primeiro uso.

---

## 🖥️ Interface do Usuário (Streamlit)

A aplicação é carregada em uma página com menu lateral, permitindo acesso às seguintes seções:

- **Visão Geral** – Informações do sistema e funcionalidades
- **Insumos** – Entrada de área (raio) e cálculo da necessidade de insumos
- **Banco de Sementes** – Cadastro, atualização, consulta, exclusão e relatório de qualidade em `.txt`
- **Automação IoT** – Visualização dos dados da plantação com sensores simulados
- **AWS** – Interface para disparo de alertas via SNS
- **Visão Computacional** – Análise de imagens de lavoura utilizando modelo treinado em YOLO

---

## 🤖 Visão Computacional – YOLOv5

O sistema carrega o modelo `best.pt` treinado com `torch.hub.load()` e realiza inferência sobre imagens de lavoura:

- Arquivo utilizado: `best.pt`
- O resultado da detecção é apresentado diretamente na interface
- Classificações são retornadas com coordenadas e rótulos sobrepostos

---

## 🌐 Integração com AWS (SNS)

O sistema permite envio de alertas quando detectadas condições críticas como:

- Fósforo ou potássio classificados como “Baixo”
- pH do solo abaixo de 5.5

A integração utiliza:

- `boto3` para enviar mensagens
- AWS SNS com tópico previamente criado
- Confirmação de assinatura (e-mail ou SMS) necessária

---

## 📦 Estrutura do Projeto

```
├── main.py                     # Código principal com todas as fases integradas
├── README.md                   # Documentação completa do sistema
├── best.pt                     # Modelo YOLOv5 treinado para visão computacional
├── AtividadeFase7.ipynb        # Notebook de treinamento do modelo YOLOv5
```

---

## 💡 Observações Finais

- O código é modular, escalável e adaptável para qualquer outro setor além do agronegócio
- Foco em experiência fluida para o usuário, com feedback visual em todas as ações
- Todas as fases estão integradas em um único ambiente Python com interface visual Streamlit

---

## 🧠 Treinamento do Modelo de Visão Computacional

O modelo utilizado na Fase 6 (Visão Computacional) foi treinado separadamente no ambiente Google Colab, por meio do notebook:

- **Arquivo:** `AtividadeFase7.ipynb`

Esse notebook foi responsável por:
- Montar o Google Drive com os dados anotados
- Carregar e configurar o modelo YOLOv5
- Realizar o treinamento utilizando imagens de lavoura (com anotações feitas em plataformas como MakeSense.ai ou Roboflow)
- Gerar o arquivo `best.pt` com os pesos finais para inferência

Esse modelo é posteriormente carregado dentro do `main.py` na seção de Visão Computacional, realizando a predição de pragas ou falhas diretamente sobre imagens enviadas pelo usuário.

---

## 🎥 Demonstração em Vídeo

Um vídeo de até 10 minutos foi gravado demonstrando todas as funcionalidades implementadas no sistema, incluindo:

- Navegação pelo menu
- Execução das fases de 1 a 6
- Geração de relatórios
- Integração com o banco de dados
- Visão Computacional com uso do YOLOv5

🔗 **Acesse o vídeo no YouTube pelo link:** https://youtu.be/geW1g1LxzsI

