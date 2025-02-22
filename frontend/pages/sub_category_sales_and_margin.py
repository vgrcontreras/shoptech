import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎')

navbar()

# 1. Objetivo da Análise
st.title('Vendas e Margens por Subcategoria')
st.subheader('🎯 Objetivo da Análise')
st.write("""
Esta análise tem como objetivo identificar, para cada subcategoria de produto, o faturamento total (vendas),
o valor total de compra (custo dos produtos) e o faturamento bruto (diferença entre o faturamento e o custo).
Essas informações ajudam a avaliar a lucratividade de cada subcategoria, permitindo tomadas de decisão mais
informadas sobre quais linhas de produtos são mais vantajosas.
""")

# 2. Descrição da Tabela
st.subheader('🗂️ Descrição da Tabela')
st.write("""
A consulta retorna as seguintes colunas principais:
""")
st.markdown("""
- **Subcategoria**: Subcategoria à qual cada produto pertence.
- **Total Faturamento**: Soma dos valores de venda relacionados à subcategoria.
- **Total Valor de Compra**: Soma dos custos de aquisição dos produtos da subcategoria.
- **Faturamento Bruto**: Diferença entre o total faturado e o valor de compra (custo).
""")
st.write("""
**Observação**: O resultado também inclui a coluna `total_orders` (quantidade de pedidos na subcategoria),
mas o foco principal desta análise está nos valores financeiros.
""")

# 3. Metodologia
st.subheader('🛠️ Metodologia')
st.write("""
Os dados foram extraídos e processados para identificar o faturamento e a margem de lucro por subcategoria de produto na Shoptech. 
Com base nessas informações, é possível avaliar quais subcategorias geram mais receita, quais possuem maiores custos de aquisição 
e quais são mais lucrativas. Essa análise auxilia na tomada de decisões estratégicas para precificação, otimização de estoque 
e definição de investimentos em produtos de alto retorno financeiro.
""")

# 4. Como Interpretar os Dados
st.subheader('📌 Como Interpretar os Dados')
st.markdown("""
- **Subcategoria**: Segmenta o resultado de acordo com a categorização dos produtos.
- **Total Faturamento**: Quanto maior esse valor, maior a receita gerada pela subcategoria.
- **Total Valor de Compra**: Informa o custo total de aquisição dos produtos daquela subcategoria.
- **Faturamento Bruto**:
  - Se for elevado, significa que a subcategoria é mais lucrativa em termos de margem bruta.
  - Um valor baixo ou negativo indica que o custo está muito próximo (ou acima) do faturamento,
    sugerindo menor atratividade ou necessidade de ajustes no preço de venda.
""")

st.subheader('Relatório')

conn = st.connection('postgresql', type='sql')

df = conn.query(
    'SELECT * FROM marts.sub_category_sales_and_margin;',
    show_spinner='Carregando dados...',
    ttl=0,
)

s = df.style.format({
    'total_orders': lambda x: '{:.0f}'.format(x),
    'total_selling_order_value': lambda x: '${:,.2f}'.format(x),
    'total_buying_order_value': lambda x: '${:,.2f}'.format(x),
    'gross_profit': lambda x: '${:,.2f}'.format(x),
})

st.dataframe(
    s,
    column_config={
        'sub_category': 'Subcategoria',
        'total_orders': 'Total Pedidos',
        'total_selling_order_value': 'Total Faturamento',
        'total_buying_order_value': 'Total Valor de Compra',
        'gross_profit': 'Faturamento Bruto',
    },
)

# 5. Código SQL
st.subheader('📜 Código SQL')
st.text(
    'A consulta abaixo calcula o faturamento e custos por subcategoria, bem como o faturamento bruto:'
)

sql_query = """
WITH fct_orders AS (
    SELECT
        orders.id,
        products.sub_category,
        ROUND(orders.order_value::numeric, 2) AS total_selling_order_value,
        (orders.products_quantity * products.price) AS total_buying_order_value
    FROM
        staging.stg_shoptech__orders orders
    INNER JOIN
        staging.stg_shoptech__products products
        ON orders.product_id = products.product_id
),
agg_orders_subcategory_data AS (
    SELECT
        sub_category,
        COUNT(id) AS total_orders,
        SUM(total_selling_order_value) AS total_selling_order_value,
        SUM(total_buying_order_value::numeric) AS total_buying_order_value
    FROM fct_orders
    GROUP BY sub_category
),
gross_profit AS (
    SELECT
        sub_category,
        total_orders,
        total_selling_order_value,
        total_buying_order_value,
        (total_selling_order_value - total_buying_order_value) AS gross_profit
    FROM agg_orders_subcategory_data
)
SELECT * 
FROM gross_profit;
"""

st.code(sql_query, language='sql')

# 6. Explicação da Consulta SQL
st.subheader('🛠️ Explicação da Consulta SQL')
st.markdown("""
1. **fct_orders**:
   - Une as tabelas de pedidos (`orders`) e produtos (`products`) para calcular, em nível de pedido,
     o valor de venda (`total_selling_order_value`) e o custo de compra (`total_buying_order_value`).

2. **agg_orders_subcategory_data**:
   - Agrupa os dados por `sub_category` e soma os valores de venda (`total_selling_order_value`) e de
     custo (`total_buying_order_value`). Também conta o número de pedidos (`COUNT(id)`).

3. **gross_profit**:
   - Cria a coluna `gross_profit` subtraindo o custo (`total_buying_order_value`) do faturamento
     (`total_selling_order_value`), resultando no faturamento bruto de cada subcategoria.

4. **Consulta Final**:
   - Retorna todas as colunas (subcategoria, número total de pedidos, faturamento total, custo total e
     faturamento bruto), permitindo comparar a lucratividade entre diferentes subcategorias de produtos.
""")
