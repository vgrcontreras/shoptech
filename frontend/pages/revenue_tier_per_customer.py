# -- Separe os clientes em 5 grupos de acordo com o valor pago por cliente

import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎')

navbar()

st.title('Classificação de Clientes por Faixa de Faturamento')

# 1. Objetivo da Análise
st.subheader('🎯 Objetivo da Análise')
st.write("""
Esta análise tem como objetivo classificar os clientes em grupos (tiers) com base no total de faturamento.
A partir dessa classificação, é possível entender melhor o perfil de cada cliente e criar estratégias de acordo
com a faixa de faturamento em que se encaixa.
""")

# 2. Descrição da Tabela
st.subheader('🗂️ Descrição da Tabela')
st.write("""
A tabela gerada neste relatório contém as seguintes colunas:
""")

st.markdown("""
- **Nome Completo**: Nome do cliente.
- **Gênero**: Indica o gênero do cliente (exemplo: "Feminino", "Masculino", "Outros").
- **Estado (UF)**: Representa o estado de residência do cliente.
- **Total Faturamento**: Quantia total faturada para cada cliente.
- **Tier**: Classificação do cliente de acordo com o faturamento, variando de 1 (menor) a 5 (maior).
""")

# 3. Metodologia
st.subheader('🛠️ Metodologia')
st.write("""
1. **Coleta e Consolidação**: Foram unidas as informações cadastrais (Nome, Gênero, Estado) com os dados de faturamento.
2. **Cálculo do Total de Faturamento**: Para cada cliente, somou-se o valor total de pedidos ao longo do período analisado.
3. **Definição de Faixas de Faturamento (Tiers)**:
   - Com base no valor total, cada cliente foi classificado em faixas (Tiers), variando de 1 a 5, onde cada faixa abrange um intervalo de faturamento.
4. **Classificação**: Atribuímos a cada cliente o Tier correspondente à sua faixa de faturamento.
""")

# 4. Como Interpretar os Dados
st.subheader('📌 Como Interpretar os Dados')
st.markdown("""
- **Clientes com Tier 1**: Geralmente possuem faturamento mais baixo.
- **Clientes com Tier 5**: São os que possuem o maior faturamento.
- **Cruzamento de informações**: Ao analisar Gênero, Estado e Faturamento, é possível identificar padrões de consumo
  e promover ações de marketing segmentadas por Tier ou por localização.
- **Nome Completo**: Permite identificar individualmente cada cliente para ações específicas.
""")

# Mensagem final
st.success(
    '🔍 Utilize estas informações para analisar e tomar decisões estratégicas com base no perfil dos clientes da Shoptech.'
)

st.subheader('Relatório')

conn = st.connection('postgresql', type='sql')

df = conn.query(
    'SELECT * FROM marts.revenue_tier_per_customer;',
    show_spinner='Carregando dados...',
    ttl=0,
)

s = df.style.format({
    'total_revenue': lambda x: '${:,.2f}'.format(x),
    'tier': lambda x: '{:.0f}'.format(x),
})


st.dataframe(
    s,
    column_config={
        'complete_name': 'Nome Completo',
        'customer_gender': 'Genero Cliente',
        'gender': 'Gênero',
        'state': 'Estado (UF)',
        'total_revenue': 'Total Faturamento',
        'group_number': 'Tier',
    },
)

# 6. Código SQL
st.subheader('📜 Código SQL')
st.text(
    'O código abaixo foi utilizado para gerar a classificação por faixa de faturamento (NTILE(5)):'
)

sql_query = """
WITH total_revenue_per_customer_tier AS (
    SELECT
        customer_id,
        SUM(order_value::numeric) AS total_revenue,
        NTILE(5) OVER (ORDER BY SUM(order_value) DESC) AS group_number
    FROM staging.stg_shoptech__orders
    GROUP BY customer_id
    ORDER BY total_revenue DESC
)
SELECT
    CONCAT(t2.first_name, ' ', t2.last_name) AS complete_name,
    t2.gender,
    t2.state,
    t1.total_revenue,
    t1.group_number
FROM total_revenue_per_customer_tier t1
INNER JOIN staging.stg_shoptech__customers t2
    ON t1.customer_id = t2.customer_id
ORDER BY t1.total_revenue DESC;
"""

st.code(sql_query, language='sql')

# 5. Explicação da Consulta SQL
st.subheader('🛠️ Explicação da Consulta SQL')
st.write("""
1. **CTE total_revenue_per_customer_tier**:
   - Agrupa os pedidos por `customer_id`.
   - Calcula o total de faturamento (`total_revenue`) para cada cliente somando a coluna `order_value`.
   - A função `NTILE(5)` distribui os clientes em cinco grupos conforme o total de faturamento, 
     ordenado de forma decrescente (maior para menor).

2. **Consulta Final**:
   - Faz um `JOIN` entre essa CTE e a tabela de clientes (`stg_shoptech__customers`) para unir informações como 
     nome completo, gênero e estado.
   - Ordena o resultado pela coluna `total_revenue` em ordem decrescente.
""")
