from datetime import date, datetime

import pytest

from src.data.customers import generate_customer_data


@pytest.fixture
def customer():
    return generate_customer_data()


def test_customer_structure_not_empty(customer):
    assert customer.first_name
    assert customer.last_name
    assert customer.email
    assert customer.phone_number
    assert customer.gender
    assert customer.date_of_birth
    assert customer.address
    assert customer.city
    assert customer.state
    assert customer.country
    assert customer.postal_code
    assert customer.created_at


def test_customer_datatypes(customer):
    assert isinstance(customer.first_name, str)
    assert isinstance(customer.last_name, str)
    assert isinstance(customer.email, str)
    assert isinstance(customer.phone_number, str)
    assert isinstance(customer.gender, str)
    assert isinstance(customer.date_of_birth, date)
    assert isinstance(customer.address, str)
    assert isinstance(customer.city, str)
    assert isinstance(customer.state, str)
    assert isinstance(customer.country, str)
    assert isinstance(customer.postal_code, str)
    assert isinstance(customer.created_at, datetime)


def test_email_format(customer):
    assert '@' in customer.email
    assert '.' in customer.email.split('@')[1]


def test_gender_value(customer):
    assert customer.gender in {'Masculino', 'Feminino', 'Outros'}


def test_address_newline_replacement(customer):
    assert '\n' not in customer.address
