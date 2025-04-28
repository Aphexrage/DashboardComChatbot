import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Config da page
st.set_page_config(
    page_title="Unilever - NASDAQ",
    page_icon="./assets/download.jpg",
    layout="wide",  
    initial_sidebar_state="expanded",
)

# Esconder o header padrao do streamlit:
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Funcao para carregar os dados corrigidos
def carregarDados():
    df = pd.read_csv("./arquivosCsv/UnileverNASDAQ.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.strftime('%B')
    return df

df = carregarDados()

# Definindo os anos:
anosDisponiveis = sorted(df["Year"].unique())

# Organizando os meses:
mesesOrdenados = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

mesesDisponiveis = [mes for mes in mesesOrdenados if mes in df["Month"].unique()]

st.sidebar.image("./assets/unileverIcon.png")

st.logo('./assets/unileverIcon.png')

st.markdown(
    """
    <style>
    .header {
        background-color: #172133;
        padding: 10px;
        color: white;
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        border-radius: 9px;
    }
    </style>

    <div class="header">
        Análise de Ações - Unilever
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .info-box {
            background-color: #172133;  /* Fundo escuro */
            padding: 15px;  /* Espaçamento interno */
            border-radius: 10px; /* Bordas arredondadas */
            text-align: center;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100px; /* Altura fixa para manter proporção */
            font-weight: bold;
        }

        /* Estiliza o título (label) da métrica */
        .info-box .info-label {
            font-weight: bold;
            font-size: 21px;
            margin-bottom: 5px; /* Pequeno espaço entre o título e o valor */
            display: flex;
            justify-content: center;
            width: 100%;
        }

        /* Estiliza o valor da métrica */
        .info-box .info-value {
            font-size: 17px;
            font-weight: bold;
        }

    </style>
""", unsafe_allow_html=True)

# Multiseletc na sidebar para os anos
anosSelecionados = st.sidebar.multiselect(
    "**Selecione os anos:**",
    options=["Todos os anos"] + anosDisponiveis,
    default=["Todos os anos"]
)

# Multiseletc na sidebar para os meses
mesesSelecionados = st.sidebar.multiselect(
    "**Selecione os meses:**",
    options=["Todos os meses"] + mesesDisponiveis,
    default=["Todos os meses"]
)

def filtrarDados(df, anosSelecionados, mesesSelecionados):
    if "Todos os anos" in anosSelecionados:
        anosSelecionados = anosDisponiveis
    if "Todos os meses" in mesesSelecionados:
        mesesSelecionados = mesesDisponiveis

    df_filtrado = df[df["Year"].isin(anosSelecionados)]
    df_filtrado = df_filtrado[df_filtrado["Month"].isin(mesesSelecionados)]
    return df_filtrado

def calcularMetricas(df_filtrado):
    totalVolume = df_filtrado["Volume"].sum()
    totalVolumef = f"${totalVolume:,.2f}"
    return totalVolumef

def ultimaData(df):
    return df["Date"].max().strftime("%d/%m/%Y")

def agruparPorMes(df_filtrado):
    dfAgrupado = df_filtrado.groupby("Month")["Volume"].sum().reset_index()
    dfAgrupado["Month"] = pd.Categorical(dfAgrupado["Month"], categories=mesesOrdenados, ordered=True)
    dfAgrupado = dfAgrupado.sort_values("Month")
    return dfAgrupado

def texto():
    texto = """
            A Unilever PLC é uma gigante global de bens de consumo, e suas ações são negociadas na Bolsa de Nova York (NYSE) sob o código "UL". Atualmente, estão cotadas a US$ 59,33, com crescimento de 25,56% no último ano. Seus indicadores financeiros mostram um índice Preço/Lucro (P/L) de 11,17 e um Dividend Yield (DY) de 3,15%, refletindo um desempenho sólido. Recentemente, o novo CEO anunciou cortes de custos e a venda de segmentos de alimentos de baixo desempenho para economizar 800 milhões de euros. Para mais detalhes, visite a aba "Assistente".
            """

df_filtrado = filtrarDados(df, anosSelecionados, mesesSelecionados)

totalVolumef = calcularMetricas(df_filtrado)
mostrarUltimaDt = ultimaData(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''
        <div class="info-box">
            <div class="info-label">Total do Volume:</div>
            <div class="info-value">{totalVolumef}</div>
        </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
        <div class="info-box">
            <div class="info-label">Atualizado em:</div>
            <div class="info-value">{mostrarUltimaDt}</div>
        </div>
    ''', unsafe_allow_html=True)
with col3:
    st.markdown(f'''
        <div class="info-box info-box-margin-top">
            <div class="info-label">Anos exibidos:</div>
            <div class="info-value">{", ".join(map(str, anosSelecionados))}</div>
        </div>
    ''', unsafe_allow_html=True)
with col4:
    st.markdown(f'''
        <div class="info-box info-box-margin-top">
            <div class="info-label">Meses exibidos:</div>
            <div class="info-value">{", ".join(mesesSelecionados)}</div>
        </div>
    ''', unsafe_allow_html=True)

df_agrupado = agruparPorMes(df_filtrado)

st.divider()

def grafSeparados():
    fig_close = px.line(
        df_filtrado, 
        x="Date", 
        y="Close/Last", 
        title="Evolução do Preço de Fechamento", 
        labels={"Close/Last": "Preço de Fechamento", "Date": "Data"},
        line_shape="linear",
        color_discrete_sequence=["white"]
    )
    st.plotly_chart(fig_close, use_container_width=True, key="grafico_fechamento")

    fig = px.bar(
        df_agrupado,
        x="Month",
        y="Volume",
        title="Total do Volume por Mês:",
        labels={"Volume": "Total do Volume", "Month": "Mês"},
        text_auto=True,
        color_discrete_sequence=["white"]
    )

    fig.update_traces(
        textfont_size=12  
    )

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Total do Volume",
        bargap=0.2,
    )

    st.plotly_chart(fig, use_container_width=True)

def grafJuntos():
    col1, col2 = st.columns(2)

    with col1:
        fig_close = px.line(
            df_filtrado, 
            x="Date", 
            y="Close/Last", 
            title="Evolução do Preço de Fechamento", 
            labels={"Close/Last": "Preço de Fechamento", "Date": "Data"},
            line_shape="linear",
            color_discrete_sequence=["white"]
        )
        st.plotly_chart(fig_close, use_container_width=True, key="grafico_fechamento")

    with col2:
        fig = px.bar(
            df_agrupado,
            x="Month",
            y="Volume",
            title="Total do Volume por Mês:",
            labels={"Volume": "Total do Volume", "Month": "Mês"},
            text_auto=True,
            color_discrete_sequence=["white"]
        )

        fig.update_traces(
            textfont_size=12  
        )

        fig.update_layout(
            xaxis_title="Mês",
            yaxis_title="Total do Volume",
            bargap=0.2,
        )

        st.plotly_chart(fig, use_container_width=True)

with st.sidebar:
    selected = option_menu(
        menu_title='Menu:',
        options=['Formatacao 1', 'Formatacao 2']
    )

if selected == 'Formatacao 1':
    grafJuntos()
if selected == 'Formatacao 2':
    grafSeparados()

    
st.divider()

st.markdown(
    """
    **Dev:** Gustavo Mendes dos Santos - Versão: 5.0
    """
)

st.markdown(
    """
    **LinkedIn:** [Clique aqui](https://www.linkedin.com/in/gustavo-mendes-117767250)
    """
)

st.markdown(
    """
    **Dados:** [NASDAQ - Unilever PLC Common Stock (UL)](https://www.nasdaq.com/market-activity/stocks/ul/historical?page=1&rows_per_page=10&timeline=y10)
    """
)
