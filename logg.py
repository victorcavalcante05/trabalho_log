# import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o arquivo Excel
caminho = "C:\\Users\\wanes\\Downloads\\LOGCP_-_base_tickets_manutencao_historico.xlsx"
df = pd.read_excel(caminho)

# Análise exploratória dos dados
print(df.shape)
print(df.head())
print(df.columns[:100])

# Selecionar colunas necessárias
colunas = ["des_assunto", "des_tipo_servico", "dat_criacao", "des_status", "des_condominio", "des_atendimento", "dat_resolucao", "des_status_etapa", "cod_uf"]
df = df[colunas]

# Verificar valores únicos e filtrar por status não deletado
print(df["des_status_etapa"].unique())
df = df[df["des_status"] != "deleted"]

# Função para gerar gráficos para cada estado (MG e DF)
def gerar_graficos(df, uf):
    # Filtrar dados para o estado específico e garantir que as datas estão no formato correto
    df_uf = df[(df["cod_uf"] == uf) & (~df["dat_resolucao"].isnull())]
    df_uf["dat_criacao"] = pd.to_datetime(df_uf["dat_criacao"], errors="coerce")
    df_uf["dat_resolucao"] = pd.to_datetime(df_uf["dat_resolucao"], errors="coerce")

    # Remover linhas com datas inválidas (NaT)
    df_uf = df_uf.dropna(subset=["dat_criacao", "dat_resolucao"])

    # Calcular o tempo de resolução em segundos e converter para horas
    tempo_resolucao = (df_uf["dat_resolucao"] - df_uf["dat_criacao"]).dt.total_seconds() / 3600
    media = tempo_resolucao.mean()
    desvio = tempo_resolucao.std()
    cv = desvio / media

    # Resultados
    print(f"{uf} - Média de tempo de resolução (horas):", media)
    print(f"{uf} - Desvio padrão de tempo de resolução (horas):", desvio)
    print(f"{uf} - Coeficiente de variação:", cv)

    # Gerando o histograma do tempo de resolução
    plt.figure(figsize=(10, 6))
    sns.histplot(tempo_resolucao, kde=True, bins=30, color='blue')
    plt.title(f'Distribuição do Tempo de Resolução dos Chamados ({uf})')
    plt.xlabel('Tempo de Resolução (Horas)')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Gerando o boxplot do tempo de resolução
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=tempo_resolucao, color='lightblue')
    plt.title(f'Boxplot do Tempo de Resolução dos Chamados ({uf})')
    plt.xlabel('Tempo de Resolução (Horas)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Gerar gráficos para MG e DF
for uf in ["MG", "DF"]:
    gerar_graficos(df, uf)
