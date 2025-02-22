import streamlit as st
from modules.nav import navbar

st.set_page_config(page_title='Relatórios', page_icon='🔎')

navbar()


st.title('Variação Ano a Ano (YoY)')
st.subheader('🎯 Objetivo da Análise')
st.write("""
Esta análise visa mostrar a quantidade total de vendas (pedidos) em cada ano e comparar esse volume 
com o ano anterior, tanto em valores absolutos quanto em variação percentual, para verificar se as vendas 
estão crescendo ou diminuindo ao longo do tempo.
""")

# 2. Descrição da Tabela
st.subheader('🗂️ Descrição da Tabela')
st.write("""
A consulta gera uma tabela com as seguintes colunas:
""")
st.markdown("""
- **Ano**: Indica o ano das vendas.
- **Total Pedidos**: Número total de pedidos realizados naquele ano.
- **Total Pedidos Ano Anterior**: Quantidade total de pedidos do ano imediatamente anterior.
- **Variação Ano Anterior**: Diferença percentual em relação ao ano anterior (pode ser positiva ou negativa).
""")

# 3. Metodologia
st.subheader('🛠️ Metodologia')
st.write("""
Os dados foram extraídos e processados para identificar a evolução das vendas ano a ano (YoY) na Shoptech.
Com base nessas informações, é possível verificar o crescimento ou a queda no número de pedidos entre um ano e outro. 
Esse insight permite avaliar a performance do negócio ao longo do tempo e apoiar decisões estratégicas de expansão,
investimento e otimização das operações.
""")

# 4. Como Interpretar os Dados
st.subheader('📌 Como Interpretar os Dados')
st.markdown("""
- **Ano**: Mostra o período exato de análise.
- **Total Pedidos**: Quantifica o volume de pedidos efetivados em cada ano.
- **Total Pedidos Ano Anterior**: Fornece a base para comparação direta, permitindo avaliar se houve 
  aumento ou redução.
- **Variação Ano Anterior**:
  - Acima de 0%: Indica crescimento em relação ao ano anterior.
  - Abaixo de 0%: Indica queda no volume de vendas em relação ao ano anterior.
  - Igual a 0%: Significa estabilidade.
""")


tabs_title = ['Variação Year-To-Date', 'Variação Month-To-Date']

tabs = st.tabs(tabs_title)


with tabs[0]:
    st.write(
        '❗Este relatório demonstra o total de vendas YTD, os dados serão demonstrados até o dia atual.'
    )
    st.write(
        'Para os meses/anos anteriores, os valores estarão completos contemplando todos os dias dos meses e anos anteriores.'
    )

    st.subheader('Relatório')

    conn = st.connection('postgresql', type='sql')

    df = conn.query(
        'SELECT * FROM marts.yoy_variance_ytd;',
        show_spinner='Carregando dados...',
        ttl=0,
    )

    s = df.style.format({
        'ano': lambda x: '{:.0f}'.format(x),
        'previous_total_order': lambda x: '{:.0f}'.format(x),
        'yoy': lambda x: '{:.0%}'.format(x),
    })

    st.dataframe(
        s,
        column_config={
            'ano': 'Ano',
            'total_order': 'Total Pedidos',
            'previous_total_order': 'Total Pedidos Ano Anterior',
            'yoy': 'Variação Ano Anterior',
        },
    )

    # 5. Código SQL
    st.subheader('📜 Código SQL')
    st.text(
        'A consulta abaixo realiza o cálculo de variação Ano a Ano com base no total de pedidos por ano:'
    )

    sql_query = """
	WITH year_per_order_id AS (
		SELECT
			id,
			EXTRACT(YEAR FROM order_date) AS year
		FROM
			staging.stg_shoptech__orders
	),
	total_order_per_year AS (
		SELECT
			year,
			COUNT(id) AS total_order
		FROM
			year_per_order_id
		GROUP BY year
		ORDER BY year
	),
	lag_total_order_per_year AS (
		SELECT
			year,
			total_order,
			LAG(total_order) OVER() AS previous_total_order
		FROM total_order_per_year
	),
	tb_yoy_variance AS (
		SELECT
			year,
			total_order,
			previous_total_order,
			(
				(total_order::numeric - previous_total_order::numeric)
				/ NULLIF(previous_total_order::numeric, 0)
			) AS percentage_variance
		FROM lag_total_order_per_year
	),
	tb_rounded_yoy_variance AS (
		SELECT
			CAST(year AS INTEGER) AS ano,
			total_order,
			previous_total_order,
			ROUND(percentage_variance, 2) AS yoy
		FROM tb_yoy_variance
	)
	SELECT * 
	FROM tb_rounded_yoy_variance;
	"""

    st.code(sql_query, language='sql')

    # 6. Explicação da Consulta SQL
    st.subheader('🛠️ Explicação da Consulta SQL')
    st.markdown("""
	1. **year_per_order_id**:
	- Extrai o ano do campo `order_date` de cada pedido, criando uma base para agrupar.

	2. **total_order_per_year**:
	- Agrupa os pedidos pelo campo `year` e calcula o total (COUNT(id)) para cada ano.

	3. **lag_total_order_per_year**:
	- Aplica a função `LAG` para recuperar o total de pedidos do ano anterior (`previous_total_order`).

	4. **tb_yoy_variance**:
	- Calcula a variação percentual entre o ano atual e o anterior usando:
		\\[
		\frac{\text{total_atual} - \text{total_anterior}}{\text{total_anterior}}
		\\]
	- Usa `NULLIF` para evitar divisão por zero quando `previous_total_order` for 0 ou nulo.

	5. **tb_rounded_yoy_variance**:
	- Converte `year` para inteiro (coluna `ano`) e arredonda a variação (`percentage_variance`) para duas casas decimais.
	- Prepara os dados para a seleção final.

	O resultado final apresenta cada ano, a quantidade de pedidos, o total de pedidos do ano anterior e a variação percentual 
	(que pode ser positiva ou negativa). Esse tipo de análise torna mais simples visualizar e entender a evolução das vendas 
	ao longo dos anos.
	""")

with tabs[1]:
    st.write(
        '❗❗Este relatório demonstra o total de vendas somente até o dia atual para todos os meses e anos anteriores.'
    )

    st.subheader('Relatório')

    conn = st.connection('postgresql', type='sql')

    df = conn.query(
        'SELECT * FROM marts.yoy_variance_mtd;',
        show_spinner='Carregando dados...',
        ttl=0,
    )

    s = df.style.format({
        'ano': lambda x: '{:.0f}'.format(x),
        'previous_total_order': lambda x: '{:.0f}'.format(x),
        'yoy': lambda x: '{:.0%}'.format(x),
    })

    st.dataframe(
        s,
        column_config={
            'ano': 'Ano',
            'total_order': 'Total Pedidos',
            'previous_total_order': 'Total Pedidos Ano Anterior',
            'yoy': 'Variação Ano Anterior',
        },
    )

    # 5. Código SQL
    st.subheader('📜 Código SQL')
    st.text(
        'A consulta abaixo calcula o total de pedidos por ano considerando os mesmos dias de cada ano (MTD) e compara com o ano anterior:'
    )

    sql_query = """
	WITH year_per_order_id AS (
		SELECT
			id,
			EXTRACT(YEAR FROM order_date) AS year,
			EXTRACT(DAY FROM order_date) AS dia,
			EXTRACT(DAY FROM CURRENT_DATE) AS dia_atual
		FROM
			staging.stg_shoptech__orders
		WHERE 1=1
	),
	year_per_order_id_mtd AS (
		SELECT
			id,
			year
		FROM
			year_per_order_id
		WHERE 1=1
			AND dia <= dia_atual
	),
	total_order_per_year AS (
		SELECT
			year,
			COUNT(id) AS total_order
		FROM
			year_per_order_id_mtd
		GROUP BY year
		ORDER BY year
	),
	lag_total_order_per_year AS (
		SELECT
			year,
			total_order,
			LAG(total_order) OVER() AS previous_total_order
		FROM total_order_per_year
	),
	tb_yoy_variance AS (
		SELECT
			year,
			total_order,
			previous_total_order,
			(
				(total_order::numeric - previous_total_order::numeric)
				/ NULLIF(previous_total_order::numeric, 0)
			) AS percentage_variance
		FROM lag_total_order_per_year
	),
	tb_rounded_yoy_variance AS (
		SELECT
			CAST(year AS INTEGER) AS ano,
			total_order,
			previous_total_order,
			ROUND(percentage_variance, 2) AS yoy
		FROM tb_yoy_variance
	)
	SELECT *
	FROM tb_rounded_yoy_variance;
	"""

    st.code(sql_query, language='sql')

    # 6. Explicação da Consulta SQL
    st.subheader('🛠️ Explicação da Consulta SQL')
    st.markdown("""
	1. **year_per_order_id**:
	- Extrai o ano (`year`) e o dia (`dia`) de cada pedido, além do dia atual do sistema (`dia_atual`). 
		Isso permite comparar períodos equivalentes (por exemplo, até o mesmo dia de cada ano).

	2. **year_per_order_id_mtd** (*Month-to-Date* ou *Matching Days*):
	- Filtra os registros para incluir apenas os pedidos cujo dia (`dia`) seja menor ou igual 
		ao dia atual (`dia_atual`). Assim, analisamos o mesmo intervalo de dias de cada ano.

	3. **total_order_per_year**:
	- Agrupa os pedidos por ano e conta (`COUNT(id)`) o número total de pedidos para cada ano, 
		respeitando o intervalo definido no passo anterior.

	4. **lag_total_order_per_year**:
	- Aplica a função de janela `LAG` para recuperar o valor de `total_order` do ano anterior 
		e armazená-lo em `previous_total_order`.

	5. **tb_yoy_variance**:
	- Calcula a variação percentual entre o ano atual e o anterior usando a fórmula:
		\\[
		\frac{\text{total_atual} - \text{total_anterior}}{\text{total_anterior}}
		\\]
	- Utiliza `NULLIF` para evitar divisão por zero.

	6. **tb_rounded_yoy_variance**:
	- Converte o ano para inteiro (`ano`) e arredonda a variação (`percentage_variance`) 
		para duas casas decimais (`yoy`). 
	- É a etapa final antes de selecionar e exibir os resultados.

	O resultado apresenta cada ano com o total de pedidos até a mesma data (`total_order`), 
	o total do ano anterior no mesmo intervalo de dias (`previous_total_order`) 
	e a variação percentual comparada ao ano anterior (`yoy`). 
	Dessa forma, é possível analisar se as vendas estão crescendo ou diminuindo 
	quando comparamos exatamente o mesmo período de cada ano.
	""")
