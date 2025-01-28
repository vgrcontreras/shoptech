from faker import Faker

from src.models import Customer

fake = Faker(locale='pt-BR')


def generate_customer_data() -> Customer:
    customers = Customer(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.safe_email(),
        phone_number=fake.cellphone_number(),
        gender=fake.random_element(['Masculino', 'Feminino', 'Outros']),
        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=50),
        address=fake.street_address(),
        city=fake.city(),
        state=fake.estado_nome(),
        country='Brasil',
        postal_code=fake.postcode(),
        created_at=fake.date_time_this_decade(),
    )

    return customers
