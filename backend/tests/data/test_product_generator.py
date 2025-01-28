import pytest
from faker import Faker

from src.data.products import brands_by_category, generate_products_data

fake = Faker()


@pytest.fixture
def product():
    return generate_products_data()


def test_product_structure_not_empty(product):
    assert product.name
    assert product.category
    assert product.sub_category
    assert product.brand
    assert product.price


def test_product_datatypes(product):
    assert isinstance(product.name, str)
    assert isinstance(product.category, str)
    assert isinstance(product.sub_category, str)
    assert isinstance(product.brand, str)
    assert isinstance(product.price, float)


def test_product_category_membership(product):
    assert product.category in brands_by_category.keys()


def test_product_subcategory_membership(product):
    assert product.sub_category in brands_by_category[product.category].keys()


def test_valid_brand(product):
    assert (
        product.brand
        in brands_by_category[product.category][product.sub_category]
    )


def test_price_value(product):
    MIN_VALUE = 50
    MAX_VALUE = 1000

    assert product.price >= MIN_VALUE
    assert product.price <= MAX_VALUE


def test_product_name(product):
    name_parts = product.name.split()

    MIN_WORDS = 2

    assert len(name_parts) >= MIN_WORDS
    assert ' '.join(name_parts[1:]) == product.sub_category
    assert name_parts[0][0].isupper()
