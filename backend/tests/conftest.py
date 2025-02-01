import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.data.customers import generate_customer_data
from src.data.products import generate_products_data
from src.models import table_registry


@pytest.fixture
def customer():
    return generate_customer_data()


@pytest.fixture
def product():
    return generate_products_data()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
