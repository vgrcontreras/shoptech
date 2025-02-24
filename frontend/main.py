import os

import streamlit as st
from dotenv import load_dotenv
from modules.nav import navbar

load_dotenv()

STREAMLIT_URL = os.getenv('STREAMLIT_URL', 'localhost:8501')

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

url_table2 = f"http://{STREAMLIT_URL}/customer_profile"
url_table3 = f"http://{STREAMLIT_URL}/mom_variance"
url_table4 = f"http://{STREAMLIT_URL}/revenue_tier_per_customer"
url_table5 = f"http://{STREAMLIT_URL}/sales_by_region"
url_table6 = f"http://{STREAMLIT_URL}/sub_category_sales_and_margin"
url_table8 = f"http://{STREAMLIT_URL}/top10_product_sales"
url_table9 = f"http://{STREAMLIT_URL}/top10_sales_products_with_margin_ranking"
url_table10 = f"http://{STREAMLIT_URL}/yoy_variance"


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
