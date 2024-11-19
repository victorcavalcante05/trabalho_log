import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o arquivo Excel
caminho = "C:\\Users\\wanes\\Downloads\\LOGCP_-_base_tickets_manutencao_historico.xlsx"
df = pd.read_excel(caminho)

# Selecionar colunas necessárias
colunas = ["des_assunto", "des_tipo_servico", "dat_criacao", "des_status", "des_condominio", "des_atendimento", "dat_resolucao", "des_status_etapa", "cod_uf"]
df = df[colunas]

# Filtrar por status não deletado
df = df[df["des_status"] != "deleted"]

# Criar função para gráficos de todas as UFs
def graficos_todas_ufs(df):
    # Garantir que datas estão no formato correto
    df["dat_criacao"] = pd.to_datetime(df["dat_criacao"], errors="coerce")
    df["dat_resolucao"] = pd.to_datetime(df["dat_resolucao"], errors="coerce")
    df = df.dropna(subset=["dat_criacao", "dat_resolucao"])
    
    # Calcular tempo de resolução em horas
    df["tempo_resolucao_horas"] = (df["dat_resolucao"] - df["dat_criacao"]).dt.total_seconds() / 3600

    # Gráfico de tempo médio por UF
    st.write("### Tempo Médio de Resolução por UF")
    tempo_medio_por_uf = df.groupby("cod_uf")["tempo_resolucao_horas"].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    tempo_medio_por_uf.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title("Tempo Médio de Resolução por UF")
    ax.set_xlabel("UF")
    ax.set_ylabel("Tempo Médio de Resolução (Horas)")
    ax.grid(axis='y')
    st.pyplot(fig)

    # Gráfico de quantidade de chamados por UF
    st.write("### Quantidade de Chamados por UF")
    quantidade_chamados_por_uf = df["cod_uf"].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    quantidade_chamados_por_uf.plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title("Quantidade de Chamados por UF")
    ax.set_xlabel("UF")
    ax.set_ylabel("Quantidade")
    ax.grid(axis='y')
    st.pyplot(fig)

# Criar abas para exibição de tabelas e gráficos
tab1, tab2 = st.tabs(["Tabela de Dados", "Gráficos e Estatísticas"])

with tab1:
    st.write("### Tabela de Dados Filtrada")
    st.dataframe(df)

with tab2:
    # Combobox para selecionar tipo de visualização (UF específica ou todas)
    opcoes = ["Selecione uma UF", "Todas as UFs"]
    uf_escolhida = st.selectbox("Selecione a Visualização:", opcoes + list(df["cod_uf"].dropna().unique()))

    if uf_escolhida == "Todas as UFs":
        graficos_todas_ufs(df)
    elif uf_escolhida != "Selecione uma UF":
        # Filtrar por UF específica e gerar gráficos
        def gerar_graficos(df, uf):
            # Filtrar dados para a UF selecionada e converter as datas corretamente
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

            # Exibir os resultados
            st.write(f"**{uf} - Média de tempo de resolução (horas):** {media:.2f}")
            st.write(f"**{uf} - Desvio padrão de tempo de resolução (horas):** {desvio:.2f}")
            st.write(f"**{uf} - Coeficiente de variação:** {cv:.2f}")

            # Gerando o histograma do tempo de resolução
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(tempo_resolucao, kde=True, bins=30, color='blue', ax=ax)
            ax.set_title(f'Distribuição do Tempo de Resolução dos Chamados ({uf})')
            ax.set_xlabel('Tempo de Resolução (Horas)')
            ax.set_ylabel('Frequência')
            ax.grid(True)
            st.pyplot(fig)

            # Gerando o boxplot do tempo de resolução
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x=tempo_resolucao, color='lightblue', ax=ax)
            ax.set_title(f'Boxplot do Tempo de Resolução dos Chamados ({uf})')
            ax.set_xlabel('Tempo de Resolução (Horas)')
            ax.grid(True)
            st.pyplot(fig)

        gerar_graficos(df, uf_escolhida)
