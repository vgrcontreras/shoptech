from datetime import date, datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Customer:
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    postal_code: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    order_id: Mapped[List['Order']] = relationship(init=False)  # type: ignore


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    sub_category: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    order_id: Mapped[List['Order']] = relationship(init=False)  # type: ignore


@table_registry.mapped_as_dataclass
class Order:
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    order_date: Mapped[date] = mapped_column(nullable=False)
    products_quantity: Mapped[int] = mapped_column(nullable=False)
    order_value: Mapped[float] = mapped_column(nullable=False)
    payment_status: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    payment_method: Mapped[str] = mapped_column(nullable=False)
    shipping_method: Mapped[str] = mapped_column(nullable=False)
    shipping_fee: Mapped[float] = mapped_column(nullable=False)
    shipping_date: Mapped[date] = mapped_column(nullable=True)
    estimated_delivery_date: Mapped[date] = mapped_column(nullable=True)
    delivery_date: Mapped[date] = mapped_column(nullable=True)
