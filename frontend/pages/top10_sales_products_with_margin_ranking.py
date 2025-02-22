import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎')

navbar()

# Título da documentação
st.title('Análise de Produtos Vendidos e Margens')

# Objetivo da análise
st.subheader('🎯 Objetivo da Análise')
st.write("""
Esta análise tem como objetivo identificar quais são os produtos mais vendidos e suas respectivas margens de lucro.
A partir dessas informações, é possível entender quais produtos geram mais receita e quais possuem melhor margem de lucro.
""")

# Descrição da tabela
st.subheader('🗂️ Descrição da Tabela')
st.write("""
A tabela gerada neste relatório contém as seguintes colunas:
""")

# Lista com a descrição das colunas
st.markdown("""
- **Nome Produto**: Nome do produto vendido.
- **Total Pedidos**: Quantidade total de vendas realizadas para este produto.
- **Total Faturamento**: Total faturado historicamente para este produto.
- **Margem Média**: Margem média de lucro deste produto.
- **Rank Margem**: Ranking do produto com base na margem média (quanto menor o número, maior a margem).
""")

# Metodologia da Análise
st.subheader('🛠️ Metodologia')
st.write("""
Para identificar os produtos mais vendidos e suas respectivas margens de lucro, seguimos os seguintes passos:

1. **Consolidação das informações**: Unimos os dados de pedidos e produtos para criar uma base única de análise.
2. **Cálculo do faturamento e margem**: Calculamos a quantidade de pedidos, o valor total faturado e a margem média para cada produto.
3. **Classificação dos produtos**: Aplicamos um ranking para ordenar os produtos com base na margem média de lucro.

""")

# Como interpretar os dados
st.subheader('📌 Como Interpretar os Dados')
st.markdown("""
- Produtos com **maior `Total Pedidos`** são os mais vendidos.
- Produtos com **maior `Total Faturamento`** geram mais receita para a empresa.
- Produtos com **maior `Margem Média`** são mais lucrativos individualmente.
- Produtos com **menor `Rank Margem`** possuem a melhor margem de lucro, já que o ranking é crescente (1 é a maior margem).
- O cruzamento entre os rankings permite identificar os produtos mais estratégicos: aqueles que vendem muito e possuem alta margem de lucro.
""")

# Mensagem final
st.success(
    '🔍 Utilize estas informações para analisar e tomar decisões estratégicas com base no perfil dos clientes da Shoptech.'
)

st.subheader('Relatório')

conn = st.connection('postgresql', type='sql')

df = conn.query(
    'SELECT * FROM marts.top10_sales_products_with_margin_ranking;',
    show_spinner='Carregando dados...',
    ttl=0,
)

s = df.style.format({
    'total_orders': lambda x: '{:.0f}'.format(x),
    'total_value_sold': lambda x: '${:,.2f}'.format(x),
    'ranking_margin': lambda x: '{:.0f}'.format(x),
    'avg_margin': lambda x: '{:.2%}'.format(x),
})

st.dataframe(
    s,
    column_config={
        'product_name': 'Nome Produto',
        'total_orders': 'Total Pedidos',
        'total_value_sold': 'Total Faturamento',
        'avg_margin': 'Margem Média',
        'ranking_margin': 'Rank Margem',
    },
)

st.subheader('Código SQL')

st.text(
    'Abaixo está o código SQL utilizado para a criação da tabela OBT com informações de produto e clientes unificadas'
)
st.text(
    'A construção da tabela foi realizada unificando informações da tabela produtos e clientes'
)

sql_query = """
with teste as (
	
select
	orders.id
	,products.product_name
	,orders.products_quantity
	,round(orders.order_value::numeric, 2) as order_value
	,products.price as product_buying_price
	,round((orders.order_value::numeric / orders.products_quantity), 2) as product_selling_price
from
	staging.stg_shoptech__orders as orders
inner join
	staging.stg_shoptech__products products
	on products.product_id = orders.product_id
	
),

teste2 as (

	select
		*
		,((product_selling_price - product_buying_price) / product_buying_price) * 100 as margin
	from
		teste
	
),

teste3 as (

	select
		product_name
		,count(id) as total_orders
		,sum(product_selling_price) as total_value_sold
		,avg(margin::numeric) as avg_margin
	from
		teste2
	group by product_name
	order by total_orders desc

)

select
	product_name
	,total_orders
	,total_value_sold
	,round(avg_margin, 2) avg_margin
	,RANK() OVER(ORDER BY total_orders DESC) as ranking_total_orders
from
	teste3
order by avg_margin desc
limit 10
"""

st.code(sql_query)
