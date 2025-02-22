import streamlit as st


def navbar():
    url_github = "https://github.com/vgrcontreras/shoptech"

    with st.sidebar:

        st.markdown("[Acessar Github](%s)" % url_github)
        st.page_link('main.py', label='🏠 Página Inicial')
        st.header('🔎 Relatórios', divider='gray')
        st.page_link('pages/customer_profile.py', label='ICP - Ideal Customer Profile')
        st.page_link('pages/top10_sales_products_with_margin_ranking.py', label='Produtos Mais Vendidos e Margens')
        st.page_link('pages/revenue_tier_per_customer.py', label='Tier de Clientes por Faturamento')
        st.page_link('pages/mom_variance.py', label='Variação Mês a Mês')
        st.page_link('pages/yoy_variance.py', label='Variação Ano a Ano')
        st.page_link('pages/sales_by_region.py', label='Vendas por Estado')
        st.page_link('pages/sub_category_sales_and_margin.py', label='Vendas e Margem por Subcategoria')
