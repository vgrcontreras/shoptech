import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎')

navbar()

st.title('Análise de Vendas por Estado')
st.subheader('🎯 Objetivo da Análise')
st.write("""
Esta análise tem como objetivo entender o volume total de vendas por estado (UF) e o percentual de participação 
de cada estado em relação ao total de vendas, permitindo identificar mercados mais ou menos relevantes 
para a Shoptech.
""")

# 2. Descrição da Tabela
st.subheader('🗂️ Descrição da Tabela')
st.write("""
A consulta retorna as seguintes colunas:
""")
st.markdown("""
- **Estado (UF)**: Código do estado onde o pedido foi realizado
- **Total Vendas**: Quantidade total de vendas (pedidos) associados a cada estado.
- **Distribuição (%)**: Participação percentual de cada estado no total de vendas, variando de 0 a 100%.
""")

# 3. Metodologia
st.subheader('🛠️ Metodologia')
st.write("""
Os dados foram extraídos e processados para identificar a distribuição geográfica das vendas da Shoptech. 
Com base nessas informações, é possível avaliar quais estados geram mais pedidos e qual é a participação de cada um 
no total de vendas. Essa análise possibilita entender melhor o comportamento de compra dos clientes por região 
e definir estratégias de vendas e marketing focadas nas áreas de maior relevância.
""")

# 4. Como Interpretar os Dados
st.subheader('📌 Como Interpretar os Dados')
st.markdown("""
- **Estado (UF)**: Informa a unidade federativa do cliente responsável pelo pedido.
- **Total Vendas**: Indica quantos pedidos ocorreram em cada estado; quanto maior, maior a relevância.
- **Distribuição (%)**: Demonstra a participação de cada estado no total de vendas. Um valor alto sugere 
  que o estado é relevante para o faturamento da Shoptech.
""")


st.subheader('Relatório')

conn = st.connection('postgresql', type='sql')

df = conn.query(
    'SELECT * FROM marts.sales_by_region;',
    show_spinner='Carregando dados...',
    ttl=0,
)

s = df.style.format({
    'total_orders': lambda x: '{:.0f}'.format(x),
    'total_buying_order_value': lambda x: '{:,.2f}'.format(x),
    'state_share': lambda x: '{:.2%}'.format(x),
})

st.dataframe(
    s,
    column_config={
        'state': 'Estado (UF)',
        'total_orders': 'Total Vendas',
        'state_share': 'Distribuição (%)',
    },
)

# 5. Código SQL
st.subheader('📜 Código SQL')
st.text(
    'A consulta abaixo obtém o número total de vendas por estado e calcula o percentual de participação:'
)

sql_query = """
WITH sales_by_region AS (
    SELECT
        t2.state,
        COUNT(t1.id) AS total_orders
    FROM staging.stg_shoptech__orders t1
    INNER JOIN staging.stg_shoptech__customers t2
        ON t1.customer_id = t2.customer_id
    GROUP BY t2.state
    ORDER BY total_orders DESC
),
sales_by_region_share AS (
    SELECT
        state,
        total_orders,
        SUM(total_orders) OVER () AS grand_total_orders
    FROM sales_by_region
    GROUP BY state, total_orders
),
sales_by_region_share_percent AS (
    SELECT
        state,
        total_orders,
        ROUND((total_orders / grand_total_orders), 4) AS state_share
    FROM sales_by_region_share
    ORDER BY total_orders DESC
)
SELECT * 
FROM sales_by_region_share_percent;
"""

st.code(sql_query, language='sql')

# 6. Explicação da Consulta SQL
st.subheader('🛠️ Explicação da Consulta SQL')
st.markdown("""
1. **sales_by_region**:
   - Agrupa os pedidos (`orders`) por estado (`state`), calculando a contagem de pedidos em cada estado 
     por meio de `COUNT(t1.id)`.

2. **sales_by_region_share**:
   - Aplica uma função de janela `SUM(total_orders) OVER ()` para calcular o total de pedidos em todos os estados, 
     armazenando o resultado em `grand_total_orders`.

3. **sales_by_region_share_percent**:
   - Calcula a participação percentual de cada estado dividindo `total_orders` por `grand_total_orders`, 
     arredondando para quatro casas decimais.
   - Classifica o resultado em ordem decrescente de pedidos (`ORDER BY total_orders DESC`).

O resultado final exibe cada estado com o total de vendas e o percentual de participação no total de vendas, 
permitindo identificar rapidamente os principais mercados para a Shoptech.
""")
