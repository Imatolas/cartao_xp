import pandas as pd
import streamlit as st
import os
import glob

st.set_page_config(layout='wide')
st.title('Gastos')


arquivos = sorted(glob.glob('faturas/Fatura2025-*.csv'))
dados_faturas = {}

for arquivo in arquivos:
    mes_ref = arquivo.split('-')[1] 
    df = pd.read_csv(arquivo, sep=';')

    
    df['Valor'] = df['Valor'].apply(lambda x: float(x.split()[1].replace('.', '').replace(',', '.')))
    df = df[df['Valor'] > 0]
    df.set_index('Data', inplace=True)

    
    pai = [
        'MP*VISUALUNIFORMESCWB',
        'MP*2PRODUTOS', 'EBN    *AMAZON RETAIL', 'PET MED'
    ]
    empresa = ['PG *BR DID', 'MP*2PRODUTOS','MP*BAKMARELETRONICALTDA', 'MP*ACQUALAO', 'FIVERR COM',
               'DM*FIVERR', 'CONECTCAR   *CONECTCAR', 'EC *LGELECTRONICS'

    ]

    vic = ['MENDES DE FARIAS CLIN', 'PG *TON RAFAEL FRUTAS', 'PAPAI DO CEU', 'MUNDIAL FRUTAS']

    df.loc[df['Estabelecimento'].isin(pai), 'Portador'] = 'PERICLES IMATO'
    df.loc[df['Estabelecimento'].isin(vic), 'Portador'] = 'VICTORIA IMATO'
    df.loc[df['Estabelecimento'].isin(empresa), 'Portador'] = '3dlux'

    dados_faturas[mes_ref] = df


meses_disponiveis = {str(i + 1).zfill(2): nome for i, nome in enumerate(
    ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
)}


mes_selecionado = st.selectbox('Mês', [meses_disponiveis[m] for m in dados_faturas.keys()])
mes_codigo = list(meses_disponiveis.keys())[list(meses_disponiveis.values()).index(mes_selecionado)]
df_selecionado = dados_faturas.get(mes_codigo)


portador = st.selectbox('Qual portador você deseja ver?', df_selecionado['Portador'].unique())


df_portador = df_selecionado[df_selecionado['Portador'] == portador]
parcelados = df_portador[df_portador['Parcela'] != '-']

col1, col2 = st.columns(2)
with col1:
    parcela = st.radio('Deseja ver só as parcelas?', ['Não', 'Sim'])
    st.dataframe(parcelados if parcela == 'Sim' else df_portador)

with col2:
    total = df_portador['Valor'].sum()
    st.header(f'TOTAL: R$ {total:.2f}')
    if parcela == 'Sim':
        total_parcelado = parcelados['Valor'].sum()
        st.subheader(f'Total parcelado: R$ {total_parcelado:.2f}')
