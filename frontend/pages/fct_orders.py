import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎', layout='wide')

navbar()


st.title('Overview Vendas')

st.subheader('Relatório')

conn = st.connection('postgresql', type='sql')

df = conn.query(
    'SELECT * FROM marts.fct_orders;',
    show_spinner='Carregando dados...',
    ttl=0,
)

st.dataframe(
    df,
    column_config={
        'order_id': 'ID',
        'customer_name': 'Nome Cliente',
        'customer_gender': 'Gênero Cliente',
        'customer_state': 'UF Cliente',
        'product_name': 'Nome Produto',
        'product_category': 'Categoria Produto',
        'product_subcategory': 'Subcategoria Produto',
        'product_brand': 'Marca Produto',
        'products_quantity': 'Qtde. Produtos',
        'order_value': 'Valor Pedido',
        'payment_status': 'Status Pagamento',
        'status': 'Status Pedido',
        'payment_method': 'Metodo Pagamento',
        'shipping_method': 'Metodo Envio',
        'shipping_fee': 'Taxa Entrega',
        'shipping_date': 'Data Envio',
        'estimated_delivery_date': 'Data Estimada Entrega',
        'delivery_date': 'Data Entrega',
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
with 

source as (

    select *
	from
		staging.stg_shoptech__orders

),

renamed as (

select
	t1.id as order_id
	,concat(t2.first_name, ' ', t2.last_name) as customer_name
	,t2.gender as customer_gender
	,t2.state as customer_state
	,t3.product_name as product_name
	,t3.category as product_category
	,t3.sub_category as product_subcategory
	,t3.brand as product_brand
	,t1.products_quantity
	,t1.order_value
	,t1.payment_status
	,t1.status
	,t1.payment_method
	,t1.shipping_method
	,t1.shipping_fee
	,t1.shipping_date
	,t1.estimated_delivery_date
	,t1.delivery_date
from
	source t1
inner join
	staging.stg_shoptech__customers t2
	on t1.customer_id = t2.customer_id
inner join
	staging.stg_shoptech__products t3
	on t1.product_id = t3.product_id

)

select * from renamed
"""

st.code(sql_query)
