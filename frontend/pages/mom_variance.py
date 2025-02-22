import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎')

navbar()

# 1. Objetivo da Análise
st.title('Análise de Vendas Mensais e Acumulado (YTD)')
st.subheader('🎯 Objetivo da Análise')
st.write("""
Esta análise tem como objetivo demonstrar se as vendas estão crescendo ou caindo ao longo dos meses 
(e em relação ao mês anterior), além de apresentar o total acumulado de vendas desde o início do ano (YTD).
""")

# 2. Descrição da Tabela
st.subheader('🗂️ Descrição da Tabela')
st.write("""
A consulta retorna as seguintes colunas:
""")
st.markdown("""
- **Mês**: Identifica o mês (1 a 12) no ano vigente.
- **Total Vendas**: Total de vendas (neste caso, o número de pedidos) no respectivo mês.
- **Variação MoM (Month-Over-Month)**: Taxa de crescimento ou queda em relação ao mês anterior.
- **Total Vendas YTD**: Soma total das vendas ao longo do ano até a data atual.
""")

# 3. Metodologia
st.subheader('🛠️ Metodologia')
st.write("""
Os dados foram extraídos e processados para identificar a evolução das vendas mensais e o total acumulado no ano (YTD) para a Shoptech. 
Com base nessas informações, é possível avaliar se as vendas estão crescendo ou diminuindo ao longo dos meses 
e quais estratégias podem ser adotadas para melhorar o desempenho de vendas.
""")

# 4. Como Interpretar os Dados
st.subheader('📌 Como Interpretar os Dados')
st.markdown("""
- **Mês**: Indica o período do ano (de 1 a 12).  
- **Total Vendas**: Quanto maior o valor, maior o volume de vendas. 
- **Variação MoM**: 
  - Valor positivo indica aumento em relação ao mês anterior.  
  - Valor negativo indica queda.  
- **Total Vendas YTD**: Exibe o acumulado ao longo do ano, facilitando a análise da evolução das vendas 
  no período.  
""")

st.subheader('Relatório')

conn = st.connection('postgresql', type='sql')

df = conn.query(
    'SELECT * FROM marts.mom_variance;',
    show_spinner='Carregando dados...',
    ttl=0,
)

s = df.style.format({
    'order_month': lambda x: '{:.0f}'.format(x),
    'total_orders': lambda x: '{:.0f}'.format(x),
    'sum_total_orders': lambda x: '{:.0f}'.format(x),
    'percentage_variance': lambda x: '{:.2%}'.format(x),
})

st.dataframe(
    s,
    column_config={
        'order_month': 'Mes',
        'total_orders': 'Total Vendas',
        'percentage_variance': 'Variação MoM',
        'sum_total_orders': 'Total Vendas YTD',
    },
)

# 5. Código SQL
st.subheader('📜 Código SQL')
st.text(
    'A consulta abaixo obtém as vendas do ano atual, calcula a variação mensal e o acumulado (YTD).'
)

sql_query = """
WITH current_year_sales AS (
    SELECT
        id,
        EXTRACT(MONTH FROM order_date) AS order_month
    FROM
        staging.stg_shoptech__orders
    WHERE 1=1
        AND DATE_PART('year', order_date) = DATE_PART('year', CURRENT_DATE)
),
total_orders_per_month AS (
    SELECT
        order_month,
        COUNT(id) AS total_orders
    FROM current_year_sales
    GROUP BY order_month
),
lag_total_orders_per_month AS (
    SELECT
        order_month,
        total_orders,
        LAG(total_orders) OVER() AS previous_total_order
    FROM total_orders_per_month
),
mom_variance AS (
    SELECT
        order_month,
        total_orders,
        (
            (total_orders::numeric - previous_total_order::numeric)
            / NULLIF(previous_total_order::numeric, 0)
        ) AS percentage_variance
    FROM lag_total_orders_per_month
)
SELECT
    order_month,
    total_orders,
    percentage_variance AS percentage_variance,
    SUM(total_orders) OVER () AS sum_total_orders
FROM mom_variance;
"""

st.code(sql_query, language='sql')

# 6. Explicação da Consulta SQL
st.subheader('🛠️ Explicação da Consulta SQL')
st.markdown("""
1. **current_year_sales**:
   - Seleciona apenas os pedidos do ano atual e extrai o número do mês (`order_month`).
   
2. **total_orders_per_month**:
   - Agrupa os pedidos por mês e conta quantos pedidos foram feitos em cada mês (`total_orders`).

3. **lag_total_orders_per_month**:
   - Utiliza a função de janela `LAG` para recuperar o valor (`total_orders`) do mês anterior 
     e compará-lo com o mês atual.

4. **mom_variance**:
   - Calcula a variação percentual (\\( \frac{\text{atual} - \text{anterior}}{\text{anterior}} \\)) 
     para medir a diferença entre os meses consecutivos.

5. **Seleção Final**:
   - Retorna o mês (`order_month`), as vendas do mês (`total_orders`), a variação mensal (`percentage_variance`) 
     e o total acumulado (`sum_total_orders`) no ano vigente.
""")
