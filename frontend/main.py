import os

import streamlit as st
from dotenv import load_dotenv
from modules.nav import navbar

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

st.set_page_config(page_title='Página inicial', page_icon='🏠')

navbar()

st.title('Bem vindo a Shoptech Analytics!')

st.divider()

st.text("""
O objetivo desta aplicação Streamlit é servir como um dashboard interativo e abrangente para a ShopTech — uma plataforma fictícia de e-commerce especializada em eletrônicos e gadgets. 
""")

st.text("""
Ao agregar e transformar dados por meio de um robusto pipeline dbt, este aplicativo fornece insights claros e acionáveis sobre as principais métricas de negócios, capacitando os stakeholders a tomar decisões informadas. 
""")

st.text("""
Das tendências de vendas e comportamentos dos clientes ao desempenho dos produtos, cada elemento do dashboard foi projetado para dar vida aos dados.
""")

st.subheader('Análises disponíveis')

url_table2 = "http://localhost:8501/customer_profile"
url_table3 = "http://localhost:8501/mom_variance"
url_table4 = "http://localhost:8501/revenue_tier_per_customer"
url_table5 = "http://localhost:8501/sales_by_region"
url_table6 = "http://localhost:8501/sub_category_sales_and_margin"
url_table8 = "http://localhost:8501/top10_product_sales"
url_table9 = "http://localhost:8501/top10_sales_products_with_margin_ranking"
url_table10 = "http://localhost:8501/yoy_variance"


st.markdown(f"""
- [ICP - Ideal Customer Profile]({url_table2})
- [Variação Month-Over-Month]({url_table3})
- [Tier de Clientes por Faturamento]({url_table4})
- [Vendas por Região]({url_table5})
- [Vendas e Margens por Subcategoria]({url_table6})
- [Produtos Mais Vendidos e Margens]({url_table9})
- [Variação Over-Over-Year]({url_table10})
""")

st.divider()

st.subheader('Criador Por')

st.text('Victor Contreras')

url_github = "https://github.com/vgrcontreras"
url_linkedin = "https://linkedin.com/in/vgr-contreras"

st.markdown(f"""
- [Github]({url_github})
- [Linkedin]({url_linkedin})

""")
