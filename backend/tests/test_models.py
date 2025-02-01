from datetime import date, datetime

from sqlalchemy import select

from src.models import Customer


def test_create_customer(session):
    customer = Customer(
        first_name='teste',
        last_name='teste',
        email='test@test.com',
        phone_number='teste',
        gender='teste',
        date_of_birth=date(2025, 1, 1),
        address='teste',
        city='test',
        state='test',
        country='test',
        postal_code='test',
        created_at=datetime(2024, 1, 1),
    )

    session.add(customer)
    session.commit()
    session.refresh(customer)

    result = session.scalar(
        select(Customer).where(Customer.first_name == 'teste')
    )

    assert result.first_name == 'teste'
