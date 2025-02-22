# -- qual é a faixa etaria de clientes que mais compram conosco e sua média de faturamento?

import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎')

navbar()

import streamlit as st

# Título da documentação
st.title('Análise de Perfil de Clientes da Shoptech')

# Objetivo da análise
st.subheader('🎯 Objetivo da Análise')
st.write("""
O objetivo desta análise é identificar qual é o perfil ideal dos clientes da Shoptech. 
Para isso, foram consideradas informações como gênero, localidade por estado, idade média e total de vendas por perfil de cliente.
""")

# Descrição da tabela
st.subheader('🗂️ Descrição da Tabela')
st.write("""
A tabela gerada neste relatório contém as seguintes colunas:
""")

# Lista com a descrição das colunas
st.markdown("""
- **Gênero**: Indica o gênero do perfil de cliente (exemplo: "Feminino", "Masculino", "Outros").
- **Estado (UF)**: Representa o estado de residência do perfil de cliente.
- **Total Pedidos**: Exibe o total de vendas realizadas por cada perfil de cliente.
- **Idade Média**: Mostra a idade média dos clientes dentro de cada perfil.
- **Ticket Médio**: Apresenta o valor médio dos pedidos para cada perfil de cliente.
- **Rank Vendas**: Classificação do perfil com base no total de pedidos, onde menor valor indica maior quantidade de pedidos.
- **Rank Ticket Médio**: Classificação do perfil em relação ao ticket médio, onde menor valor indica maior ticket médio.
""")

# Metodologia
st.subheader('🛠️ Metodologia')
st.write("""
Os dados foram extraídos e processados para identificar padrões de compra dos clientes da Shoptech. 
Com base nessas informações, é possível avaliar quais perfis geram mais vendas e possuem maior ticket médio.
""")

# Como interpretar os dados
st.subheader('📌 Como Interpretar os Dados')
st.markdown("""
- Perfis com **menor `Rank Vendas`** representam aqueles que possuem o maior número de pedidos.
- Perfis com **menor `Rank Ticket Médio`** representam aqueles que possuem o maior ticket médio por compra.
- O cruzamento entre os rankings permite identificar os clientes mais valiosos para a Shoptech.
""")

# Mensagem final
st.success(
    '🔍 Utilize estas informações para analisar e tomar decisões estratégicas com base no perfil dos clientes da Shoptech.'
)

conn = st.connection('postgresql', type='sql')

df = conn.query(
    'SELECT * FROM marts.customer_profile;',
    show_spinner='Carregando dados...',
    ttl=0,
)

st.subheader('Relatório')

s = df.style.format({
    'total_orders': lambda x: '{:.0f}'.format(x),
    'avg_age': lambda x: '{:.0f}'.format(x),
    'avg_order_value': lambda x: 'R${:.2f}'.format(x),
    'rank_total_orders': lambda x: '{:.0f}'.format(x),
    'rank_avg_order_value': lambda x: '{:.0f}'.format(x),
})


st.dataframe(
    s,
    column_config={
        'gender': 'Gênero',
        'state': 'Estado (UF)',
        'total_orders': 'Pedidos',
        'avg_age': 'Idade Média',
        'avg_order_value': 'Ticket Médio',
        'rank_total_orders': 'Rank Vendas',
        'rank_avg_order_value': 'Rank Ticket Médio',
    },
)

sql_query = """
with

total_orders_per_customer as (

select
	t2.gender
	,t2.state
	,count(t2.customer_id) as total_orders
	,round(cast(avg(date_part('year', age(t2.date_of_birth))) as numeric), 0) as avg_age
	,round(avg(t1.order_value::numeric), 2) as avg_order_value
from
	staging.stg_shoptech__orders t1
inner join
	staging.stg_shoptech__customers t2
	on t1.customer_id = t2.customer_id
group by t2.gender,t2.state
order by total_orders desc

)

select 
	*
	,rank() over (order by total_orders desc) as rank_total_orders
	,rank() over (order by avg_order_value) as rank_avg_order_value
from 
	total_orders_per_customer
order by total_orders desc
"""

# Exibir código SQL no Streamlit
st.subheader('Código SQL')
st.text('O código abaixo foi utilizado para gerar a tabela de análise:')
st.code(sql_query, language='sql')

# Explicação da consulta SQL
st.subheader('Explicação da Consulta SQL')
st.text(
    'O código SQL abaixo foi utilizado para criar a tabela de análise de perfil dos clientes da Shoptech.'
)
st.text(
    'Ele consolida dados da tabela de pedidos e da tabela de clientes para gerar informações agregadas.'
)

st.markdown("""
A consulta SQL pode ser dividida em duas etapas principais:

1. **Agregação dos dados de pedidos e clientes**:
   - A consulta começa criando a CTE (`total_orders_per_customer`), onde unimos a tabela de pedidos (`stg_shoptech__orders`) com a tabela de clientes (`stg_shoptech__customers`).
   - Nesta etapa, calculamos:
     - O número total de pedidos por perfil de cliente (`total_orders`).
     - A idade média do cliente (`avg_age`), extraindo o ano de nascimento da data de nascimento (`date_of_birth`).
     - O valor médio do pedido (`avg_order_value`), utilizando a média dos valores dos pedidos.

2. **Classificação dos perfis de clientes**:
   - Após a agregação dos dados, utilizamos a função `RANK()` para criar duas classificações:
     - `rank_total_orders`: Classificação do perfil com base no total de pedidos (do maior para o menor).
     - `rank_avg_order_value`: Classificação do perfil com base no ticket médio (do menor para o maior).

O resultado final exibe os perfis ordenados pelo total de pedidos, permitindo identificar os clientes mais relevantes para a Shoptech.
""")
