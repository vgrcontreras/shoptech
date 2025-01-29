from sqlalchemy.orm import Session

from src.data.customers import generate_customer_data
from src.data.orders import generate_orders_data
from src.data.products import generate_products_data
from src.database import engine


def populate_customers_table(session: Session, num_records: int) -> None:
    customers = [generate_customer_data() for _ in range(num_records)]

    session.add_all(customers)
    session.commit()


def populate_products_table(session: Session, num_records: int) -> None:
    products = [generate_products_data() for _ in range(num_records)]

    session.add_all(products)
    session.commit()


def populate_orders_table(session: Session, num_records: int) -> None:
    orders = [generate_orders_data() for _ in range(num_records)]

    session.add_all(orders)
    session.commit()


def load_data() -> None:
    with Session(engine) as session:
        populate_customers_table(session, num_records=1_000)
        populate_products_table(session, num_records=5_000)
        populate_orders_table(session, num_records=50_000)


if __name__ == '__main__':
    load_data()
