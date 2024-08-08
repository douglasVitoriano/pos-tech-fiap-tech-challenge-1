# %%

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import glob
from pathlib import Path



# Configuração da página
st.set_page_config(
    page_title="Análise de Dados de Vinhos",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Verificar o diretório (usado para debug)
# current_dir = os.getcwd() #Pega o diretorio atual
# parent_dir = os.path.dirname(current_dir) #Pega o diretorio (anterior, no caso ficou /src)
# parent_dir = os.path.dirname(parent_dir)
# current_dir = os.path.join(parent_dir, 'files') #localiza o files
# current_dir

#nao funcionará se vc rodar o streamlit run src/services/dash.py , utilizar dir acima
current_dir = Path.cwd()
current_dir = current_dir.parent / 'pos-tech-fiap-tech-challenge-1' / 'files'

# Definir os caminhos dos arquivos
file_path_1 = os.path.join(current_dir, 'Producao.csv')
file_path_2 = os.path.join(current_dir, 'Comercio.csv')
file_path_3 = os.path.join(current_dir, 'ImpVinhos.csv')
file_path_4 = os.path.join(current_dir, 'ExpVinho.csv')
file_path_5 = os.path.join(current_dir, 'ProcessaViniferas.csv')
#file_path_5 = glob.glob(os.path.join(current_dir, 'Processa*.csv'))

# Função para renomear as colunas
def renomear_colunas(df): 
    df.columns = [col[:4] for col in df.columns] 
    #faz com que o df não tenha colunas duplicadas
    df = df.loc[:,~df.columns.duplicated()]

    return df



# Carregar os arquivos CSV
df_1 = pd.read_csv(file_path_1, sep=';', decimal=',') if os.path.exists(file_path_1) else None
df_2 = pd.read_csv(file_path_2, sep=';', decimal=',') if os.path.exists(file_path_2) else None
df_3 = pd.read_csv(file_path_3, sep=';', decimal=',') if os.path.exists(file_path_3) else None
df_4 = pd.read_csv(file_path_4, sep=';', decimal=',') if os.path.exists(file_path_4) else None
df_5 = pd.read_csv(file_path_5, sep=';', decimal=',') if os.path.exists(file_path_5) else None

#para o glob
# for file in file_path_5:
#     df_5 = pd.read_csv(file, sep='\t', decimal=',')
#     df_5 = renomear_colunas(df_5)


#Planilhas que tem valores com .1, .2, precisa chamar funcao antes
df_3 = renomear_colunas(df_3)
df_4 = renomear_colunas(df_4)
df_5 = renomear_colunas(df_5)

# Obter os anos disponíveis por coluna coluna
anos_1 = df_1.columns[3:] if df_1 is not None else []
anos_2 = df_2.columns[3:] if df_2 is not None else []
anos_3 = df_3.columns[2:] if df_3 is not None else []
anos_4 = df_4.columns[2:] if df_4 is not None else []
anos_5 = df_5.columns[1:] if df_5 is not None else []



# Criar uma lista de anos únicos combinados
anos_combinados = sorted(set(anos_1).union(set(anos_2)).union(set(anos_3)), reverse=True)

ano_selecionado = st.sidebar.selectbox('Selecione o Ano', anos_combinados, key='selectbox_ano')



if os.path.exists(file_path_1):
    df = pd.read_csv(file_path_1, sep=';', decimal=',')
    
 
    
    # Filtrar o DataFrame pelo ano selecionado
    df_ano_selecionado = df.iloc[:, [2, df.columns.get_loc(ano_selecionado)]].head(10)
    

    x_produtos = df_ano_selecionado.iloc[:, 0]  # col1
    y_valores = df_ano_selecionado.iloc[:, 1]
    df_ano_selecionado = df_ano_selecionado.groupby(x_produtos)[ano_selecionado].sum().reset_index()
    df_ano_selecionado = df_ano_selecionado.sort_values(by=df_ano_selecionado.columns[1], ascending=False)
    
    # Exibir o DataFrame filtrado
    st.write(f"Dados para o ano {ano_selecionado}:")

    fig_prod = px.bar(df_ano_selecionado, x=y_valores, y=x_produtos, 
                  title="Produção de vinhos, sucos e derivados do Rio Grande do Sul por Quantidade (L.)")

    st.plotly_chart(fig_prod, use_container_width=True)
    #Para verificar o retorno recebido no grafico
    #st.dataframe(df_ano_selecionado)
    
else:
    st.write(f"Arquivo {file_path_1} não encontrado.")

file_path_2 = os.path.join(current_dir, 'Comercio.csv')


if os.path.exists(file_path_2):
    df_comercio = pd.read_csv(file_path_2, sep=';', decimal=',')
    
    anos_2 = df.columns[3:]
    
    #id, control, 1970
    #id, control, paises, 1970
    #for leia_um_arquivo in dir:
    #   
    df_ano_selecionado_comercio = df_comercio.iloc[:, [2, df_comercio.columns.get_loc(ano_selecionado)]].head(10)
    
    x_produtos_comercio = df_ano_selecionado_comercio.iloc[:, 0]  # col1
    y_valores_comercio = df_ano_selecionado_comercio.iloc[:, 1] # col2

    df_ano_selecionado_comercio = df_ano_selecionado_comercio.groupby(x_produtos_comercio)[ano_selecionado].sum().reset_index()
    df_ano_selecionado_comercio = df_ano_selecionado_comercio.sort_values(by=df_ano_selecionado_comercio.columns[1], ascending=False)

    fig_prod_comercio = px.bar(df_ano_selecionado_comercio, x=y_valores_comercio, y=x_produtos_comercio, title="Comercialização de vinhos e derivados no Rio Grande do Sul por Quantidade (L.)")
    st.plotly_chart(fig_prod_comercio, use_container_width=True)
    
else:
    st.write(f"Arquivo {file_path_2} não encontrado.")

if os.path.exists(file_path_3):
    df_imp_vinhos = pd.read_csv(file_path_3, sep=';', decimal=',')

    df_imp_vinhos = renomear_colunas(df_imp_vinhos)
    
    anos_3 = df.columns[2:]

    df_ano_selecionado_imp_vinhos = df_imp_vinhos.iloc[:, [1, df_imp_vinhos.columns.get_loc(ano_selecionado)]]
    
    x_produtos_imp_vinhos = df_ano_selecionado_imp_vinhos.iloc[:, 0]  # col1
    y_valores_imp_vinhos = df_ano_selecionado_imp_vinhos.iloc[:, 1] # col2
    
    df_ano_selecionado_imp_vinhos = df_ano_selecionado_imp_vinhos.groupby(x_produtos_imp_vinhos)[ano_selecionado].sum().reset_index()

    

    df_ano_selecionado_imp_vinhos = df_ano_selecionado_imp_vinhos.sort_values(by=df_ano_selecionado_imp_vinhos.columns[1], ascending=False)
    df_ano_selecionado_imp_vinhos = df_ano_selecionado_imp_vinhos.head(10)
    df_ano_selecionado_imp_vinhos.head()


    cores_personalizadas = px.colors.qualitative.Dark24

    #Crie um grafico bubble chart
    bubble_chart = px.scatter(df_ano_selecionado_imp_vinhos, 
                              x=df_ano_selecionado_imp_vinhos.iloc[:, 1], 
                              y=df_ano_selecionado_imp_vinhos.iloc[:, 0], 
                              size=df_ano_selecionado_imp_vinhos.iloc[:, 1],
                              color=df_ano_selecionado_imp_vinhos.iloc[:, 0], 
                              hover_name=df_ano_selecionado_imp_vinhos.iloc[:, 0], 
                              size_max=60, 
                              color_discrete_sequence=cores_personalizadas,
                              title="Importação de vinhos de mesa por Países em Quantidade (Kg)")
    bubble_chart.update_layout(
    width=1000,  # Largura da figura
    height=800   # Altura da figura
    )
    st.plotly_chart(bubble_chart, use_container_width=True)

else:
    st.write(f"Arquivo {file_path_3} não encontrado.")

if os.path.exists(file_path_4):
    df_exp_vinho = pd.read_csv(file_path_4, sep=';', decimal=',')
    
    df_exp_vinho = renomear_colunas(df_exp_vinho)
    
    anos_4 = df.columns[2:]

    df_ano_selecionado_exp_vinho = df_exp_vinho.iloc[:, [1, df_exp_vinho.columns.get_loc(ano_selecionado)]]
    
    x_produtos_exp_vinho = df_ano_selecionado_exp_vinho.iloc[:, 0]  # col1
    y_valores_exp_vinho = df_ano_selecionado_exp_vinho.iloc[:, 1] # col2
    
    df_ano_selecionado_exp_vinho = df_ano_selecionado_exp_vinho.groupby(x_produtos_exp_vinho)[ano_selecionado].sum().reset_index()

    df_ano_selecionado_exp_vinho = df_ano_selecionado_exp_vinho.sort_values(by=df_ano_selecionado_exp_vinho.columns[1], ascending=False)
    df_ano_selecionado_exp_vinho = df_ano_selecionado_exp_vinho.head(10)
    df_ano_selecionado_exp_vinho.head()

    #df_ano_selecionado_exp_vinho['log_valores'] = np.log1p(df_ano_selecionado_exp_vinho.iloc[:, 1])

    cores_personalizadas = px.colors.qualitative.T10

    #Crie um grafico bubble chart
    bubble_chart_exp = px.scatter(df_ano_selecionado_exp_vinho, 
                              x=df_ano_selecionado_exp_vinho.iloc[:, 1], 
                              y=df_ano_selecionado_exp_vinho.iloc[:, 0], 
                              size=df_ano_selecionado_exp_vinho.iloc[:, 1],
                              color=df_ano_selecionado_exp_vinho.iloc[:, 0], 
                              hover_name=df_ano_selecionado_exp_vinho.iloc[:, 0], 
                              size_max=60, 
                              color_discrete_sequence=cores_personalizadas,
                              title="Exportação de vinhos de mesa por Países em Quantidade (Kg)")
    bubble_chart_exp.update_layout(
    width=1000,  # Largura da figura
    height=800   # Altura
    )
    st.plotly_chart(bubble_chart_exp, use_container_width=True)
else:
    st.write(f"Arquivo {file_path_4} não encontrado.")

if os.path.exists(file_path_5):
    df_processa_viniferas = pd.read_csv(file_path_5, sep=';', decimal=',')
    
    df_processa_viniferas = renomear_colunas(df_processa_viniferas)

    
    
    df_ano_selecionado_processa_viniferas = df_processa_viniferas.iloc[:, [2, df_processa_viniferas.columns.get_loc(ano_selecionado)]].sort_values(by=ano_selecionado, ascending=False).head(10)
    
    x_produtos_processa_viniferas = df_ano_selecionado_processa_viniferas.iloc[:, 0]  # col1
    y_valores_processa_viniferas = df_ano_selecionado_processa_viniferas.iloc[:, 1] # col2
    df_ano_selecionado_processa_viniferas = df_ano_selecionado_processa_viniferas.groupby(x_produtos_processa_viniferas)[ano_selecionado].sum().reset_index()

    df_ano_selecionado_processa_viniferas = df_ano_selecionado_processa_viniferas.sort_values(by=df_ano_selecionado_processa_viniferas.columns[1], ascending=False)

    

    #Crie um grafico bubble chart
    fig_bar = px.bar(df_ano_selecionado_processa_viniferas,
                        x=y_valores_processa_viniferas,
                        y=x_produtos_processa_viniferas,
                        title="Processamento de uvas viníferas por variedade em Quantidade (Kg)")
    st.plotly_chart(fig_bar, use_container_width=False)

# %%