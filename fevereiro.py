import pandas as pd
import streamlit as st

fev = pd.read_csv('faturas/Fatura2025-02-10.csv', sep = ';')
jan = pd.read_csv('faturas/Fatura2025-01-10.csv', sep = ';')

fev['Valor'] = fev['Valor'].apply(lambda x: float(x.split()[1].replace('.','').replace(',','.')))
fev = fev[fev['Valor'] > 0]
fev.set_index('Data', inplace=True)

pai = ['CONECTCAR   *CONECTCAR', 'PG *BR DID','MP*VISUALUNIFORMESCWB','MP*2PRODUTOS','EBN    *AMAZON RETAIL', 'PET MED', 'MP*BAKMARELETRONICALTDA']

fev.loc[fev['Estabelecimento'].isin(pai), 'Portador'] = 'PERICLES IMATO'
fev.loc[fev['Estabelecimento'] == 'MENDES DE FARIAS CLIN', 'Portador'] = 'VICTORIA IMATO'
jan.loc[jan['Estabelecimento'].isin(pai), 'Portador'] = 'PERICLES IMATO'
jan.loc[jan['Estabelecimento'] == 'MENDES DE FARIAS CLIN', 'Portador'] = 'VICTORIA IMATO'


st.set_page_config(layout='wide')
st.title('Gasto')


gabriel = fev[fev['Portador']=='GABRIEL IMATO']
victoria = fev[fev['Portador']=='VICTORIA IMATO']
pericles = fev[fev['Portador']=='PERICLES IMATO']

grupo = fev.groupby('Portador')['Valor'].sum()


jan['Valor'] = jan['Valor'].apply(lambda x: float(x.split()[1].replace('.','').replace(',','.')))
jan = jan[jan['Valor'] > 0]
jan.set_index('Data', inplace = True)


meses = st.selectbox(
    'Mes',
    ['Jan', 'Fev']
)

option = st.selectbox(
    'Qual portador voce deseja ver?',
    ['GABRIEL IMATO','VICTORIA IMATO', 'PERICLES IMATO']
)

df_fev = fev[fev['Portador'] == f'{option}']
df_jan = jan[jan['Portador'] == f'{option}']

if meses == 'Fev':
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_fev)

    with col2:
        st.header(f'R$ {fev[fev['Portador'] == f'{option}']['Valor'].sum()}')

if meses == 'Jan':
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_jan)
    
    with col2:
        st.header(f'R$ {jan[jan['Portador'] == f'{option}']['Valor'].sum()}')

        
