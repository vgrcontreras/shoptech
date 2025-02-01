from sqlalchemy.orm import Session

from src.data.customers import generate_customer_data
from src.data.orders import generate_orders_data
from src.data.products import generate_products_data
from src.database import get_session
from src.models import Customer, Order, Product
from src.schemas import CustomerSchema, OrderSchema, ProductSchema


def populate_customers_table(session: Session, num_records: int) -> None:
    customers = [generate_customer_data() for _ in range(num_records)]

    validated_customers = [CustomerSchema.model_validate(c) for c in customers]

    customers_models = [
        Customer(**c.model_dump()) for c in validated_customers
    ]

    session.add_all(customers_models)
    session.commit()


def populate_products_table(session: Session, num_records: int) -> None:
    products = [generate_products_data() for _ in range(num_records)]

    validated_products = [ProductSchema.model_validate(p) for p in products]

    products_models = [Product(**p.model_dump()) for p in validated_products]

    session.add_all(products_models)
    session.commit()


def populate_orders_table(session: Session, num_records: int) -> None:
    orders = [generate_orders_data() for _ in range(num_records)]

    validated_orders = [OrderSchema.model_validate(o) for o in orders]

    orders_models = [Order(**o.model_dump()) for o in validated_orders]

    session.add_all(orders_models)
    session.commit()


def load_data(session) -> None:
    populate_customers_table(session, num_records=1_000)
    populate_products_table(session, num_records=5_000)
    populate_orders_table(session, num_records=10_000)


if __name__ == '__main__':
    with get_session() as session:
        load_data(session)
