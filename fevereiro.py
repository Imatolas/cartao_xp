import pandas as pd
import streamlit as st

fatura = pd.read_csv('faturas/Fatura2025-02-10.csv', sep = ';')
nw = pd.read_csv('faturas/Fatura2025-02-10.csv', sep = ';')
nw.set_index('Data', inplace=True)

fatura['Valor'] = fatura['Valor'].apply(lambda x: float(x.split()[1].replace('.','').replace(',','.')))
fatura = fatura[fatura['Valor'] > 0]
fatura.set_index('Data', inplace=True)

pai = ['CONECTCAR   *CONECTCAR', 'PG *BR DID','MP*VISUALUNIFORMESCWB','MP*2PRODUTOS','EBN    *AMAZON RETAIL', 'PET MED', 'MP*BAKMARELETRONICALTDA']

fatura.loc[fatura['Estabelecimento'].isin(pai), 'Portador'] = 'PERICLES IMATO'
fatura.loc[fatura['Estabelecimento'] == 'MENDES DE FARIAS CLIN', 'Portador'] = 'VICTORIA IMATO'
pec = fatura[fatura['Portador'] == 'PERICLES IMATO']

st.set_page_config(layout='wide')
st.title('Gasto fevereiro')
option = st.selectbox(
    'Qual portador voce deseja ver?',
    fatura['Portador'].unique()
)

gabriel = fatura[fatura['Portador']=='GABRIEL IMATO']
victoria = fatura[fatura['Portador']=='VICTORIA IMATO']
pericles = fatura[fatura['Portador']=='PERICLES IMATO']

grupo = fatura.groupby('Portador')['Valor'].sum()


df_selecionado = nw[nw['Portador'] == f'{option}']

col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_selecionado)

with col2:
    st.header('Gabriel')
    
    st.header('Victoria')
    
    st.header('Pericles')
    
