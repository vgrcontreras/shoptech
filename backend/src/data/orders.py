import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import Customer, Order, Product

fake = Faker()


def create_customer_id_data(session: Session) -> int:
    customers_row_count = session.query(func.count(Customer.id)).scalar()

    customer_id = fake.random_int(min=1, max=customers_row_count)

    return customer_id


def create_product_id_data(session: Session) -> int:
    products_row_count = session.query(func.count(Product.id)).scalar()

    product_id = fake.random_int(min=1, max=products_row_count)

    return product_id


def create_order_date_date(session: Session, customer_id: int) -> int:
    db_customer = session.scalar(
        select(Customer).where(Customer.id == customer_id)
    )

    order_date = fake.date_between(
        start_date=db_customer.created_at, end_date=date.today()
    )

    return order_date


def create_products_quantity() -> int:
    return fake.random_int(min=1, max=4)


def create_order_value_data(
    session: Session, product_id: int, products_quantity: int
) -> float:
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )

    product_value = db_product.price

    product_margin = (products_quantity * product_value) * round(
        random.uniform(0.01, 1), 2
    )

    order_value = product_value + product_margin

    return order_value


def create_payment_status() -> str:
    payment_status = random.choices(
        population=['Paid', 'Pending', 'Failed'], weights=[0.7, 0.2, 0.1], k=1
    )

    return payment_status[0]


def create_status_data(payment_status):
    if payment_status in {'Pending', 'Failed'}:
        status = 'Pending'
    else:
        status = random.choices(
            population=['Processing', 'Shipped', 'Delivered', 'Cancelled'],
            weights=[0.1, 0.1, 0.7, 0.1],
            k=1,
        )[0]

    return status


def create_shipping_method_data() -> str:
    return fake.random_element(elements=['Standard', 'Express'])


def create_shipping_fee_data(shipping_method: str) -> float:
    if shipping_method == 'Standard':
        return round(random.uniform(10.0, 20.0), 2)
    else:
        return round(random.uniform(25.0, 40.0), 2)


def create_shipping_date_data(
    status: str, shipping_method: str, order_date: date
) -> date:
    if status in {'Pending', 'Processing', 'Cancelled'}:
        return None
    elif status in {'Shipped', 'Delivered'} and shipping_method == 'Express':
        return order_date + timedelta(days=1)
    elif status in {'Shipped', 'Delivered'} and shipping_method == 'Standard':
        return order_date + timedelta(days=2)


def create_eta_data(shipping_date, shipping_method):
    if shipping_date is None:
        return None
    if shipping_method == 'Standard':
        return shipping_date + timedelta(days=4)
    else:
        return shipping_date + timedelta(days=2)


def create_delivery_date_data(
    status: str, shipping_method: str, shipping_date: date
) -> date:
    if shipping_date is None or status == 'Shipped':
        return None
    elif shipping_method == 'Standard':
        diff_days = fake.random_int(min=3, max=5)
        return shipping_date + timedelta(days=diff_days)
    else:
        diff_days = fake.random_int(min=1, max=3)
        return shipping_date + timedelta(days=diff_days)


def generate_orders_data():
    with Session(engine) as session:
        customer_id = create_customer_id_data(session)
        product_id = create_product_id_data(session)
        order_date = create_order_date_date(session, customer_id)
        products_quantity = create_products_quantity()
        order_value = create_order_value_data(
            session, product_id, products_quantity
        )
        payment_status = create_payment_status()
        status = create_status_data(payment_status)
        shipping_method = create_shipping_method_data()
        shipping_fee = create_shipping_fee_data(shipping_method)
        shipping_date = create_shipping_date_data(
            status, shipping_method, order_date
        )
        estimated_delivery_date = create_eta_data(
            shipping_date, shipping_method
        )
        delivery_date = create_delivery_date_data(
            status, shipping_method, shipping_date
        )

    orders = Order(
        customer_id=customer_id,
        product_id=product_id,
        order_date=order_date,
        products_quantity=products_quantity,
        order_value=order_value,
        payment_status=payment_status,
        status=status,
        payment_method=fake.random_element(
            elements=['Credit Card', 'PayPal', 'Bank Transfer']
        ),
        shipping_method=shipping_method,
        shipping_fee=shipping_fee,
        shipping_date=shipping_date,
        estimated_delivery_date=estimated_delivery_date,
        delivery_date=delivery_date,
    )

    return orders
