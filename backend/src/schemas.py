from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from backend.src.models import (
    PaymentMethodState,
    PaymentStatusState,
    ShippingMethodState,
    StatusState,
)


class CustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    gender: str
    date_of_birth: date
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProductSchema(BaseModel):
    name: str
    category: str
    sub_category: str
    brand: str
    price: float
    model_config = ConfigDict(from_attributes=True)


class OrderSchema(BaseModel):
    customer_id: int
    product_id: int
    order_date: date
    products_quantity: int
    order_value: float
    payment_status: PaymentStatusState
    status: StatusState
    payment_method: PaymentMethodState
    shipping_method: ShippingMethodState
    shipping_fee: float
    shipping_date: Optional[date]
    estimated_delivery_date: Optional[date]
    delivery_date: Optional[date]
    model_config = ConfigDict(from_attributes=True)
