# Shoptech: Projeto de Caso de Estudo em Engenharia de Dados

Bem-vindo ao repositório do projeto fictício Shoptech, um e-commerce especializado em eletrônicos e gadgets, criado para fins de estudo e aplicação prática de conceitos de Engenharia de Dados.

## Conteúdos

- [Sobre o Projeto](#sobre-projeto)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Objetivo do Caso de Estudo](#objetivo-do-caso-de-estudo)
- [Como Executar o Projeto](#como-executar-o-projeto)
<!-- - [Further Improvements](#further-improvements) -->

## Sobre o Projeto

O objetivo deste projeto é simular um cenário realista de um e-commerce, onde grandes volumes de dados precisam ser coletados, processados, armazenados e analisados. A Shoptech serve como pano de fundo para demonstrar habilidades técnicas e práticas relacionadas a pipelines de dados, modelagem de banco de dados, transformações ETL e análises de dados.

Os dados utilizados no projeto são gerados randomicamente e não representam informações reais. Este projeto é idealizado como um case fictício para demonstrar conhecimento técnico em um contexto realista e relevante para o mercado.

## Objetivo do Caso de Estudo

O principal objetivo do projeto Shoptech é criar um ambiente completo para:

- Simular o fluxo de dados de um e-commerce: da captura (compra do cliente) até a análise de métricas de desempenho.
- Demonstrar boas práticas em engenharia de dados, incluindo ingestão, transformação e armazenamento de dados.
- Aplicar ferramentas e frameworks modernos utilizados no setor, como Python, SQL, dbt, Airflow e mais.
- Visualizar insights gerados a partir dos dados processados, simulando relatórios para acompanhamento de métricas de negócios.

## Principais Etapas do Projeto

1. Geração de Dados Sintéticos

  Uso de bibliotecas como Faker ou scripts customizados para criar dados realistas.

2. Ingestão de Dados
  
  Construção de pipelines para ingestão de dados brutos provenientes de múltiplas fontes simuladas (ex.: logs de navegação, transações, inventário).

3. Transformação de Dados

  Aplicação de processos ETL/ELT para limpeza, normalização e enriquecimento dos dados.

4. Modelagem e Armazenamento

  Design de um Data Warehouse com esquema estrela para análise eficiente.

5. Análise e Visualização

  Criação de dashboards para medir KPIs como:

- Taxa de conversão.
- Receita total por período.
- Produtos mais vendidos.
- Retenção de clientes.

## Tecnologias Utilizadas

- 💻 **Backend**
  - [Faker](https://fastapi.tiangolo.com/) para criação de dados transacionais fictícios da Shoptech.
  - [SQLAlchemy](https://www.sqlalchemy.org/) para interações com bancos de dados SQL em Python (ORM).
  - [PostgreSQL](https://www.postgresql.org/)
  - [Alembic](https://alembic.sqlalchemy.org/en/latest/) para migração de banco de dados
  - Testes com [Pytest](https://docs.pytest.org/en/stable/) e [Testcontainers](https://testcontainers-python.readthedocs.io/en/latest/).
  - [Pre-commit](https://pre-commit.com/) com [Ruff](https://docs.astral.sh/ruff/) para análises estáticas e formatações de código.
  - CI (Integração contínua) com GitHub Actions.

- 🌐 **Frontend**


#### Estrutura do Projeto

```

```

## Como Executar o Projeto

Antes de rodar o projeto, você precisa ter o Docker Compose instalado. Se ainda não tiver, siga o guia de instalação oficial:

[Como instalar Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clonar o Repositório

Clone o repositório para sua máquina local:

```bash
git clone git@github.com:vgrcontreras/shoptech.git
```

### 2. Acesse o repositório do projeto

Depois de clonar o repositório, entre no diretório do projeto:

```bash
cd shoptech
```

### 3. Subir os Containers com Docker Compose

Agora, use o Docker Compose para construir e rodar os containers do projeto:

```bash
docker-compose up --build
```

Isso irá iniciar todos os serviços necessários para rodar o projeto. Aguarde até que todos os containers estejam em execução.