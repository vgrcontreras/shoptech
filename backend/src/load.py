import sys
from datetime import datetime

from loguru import logger
from sqlalchemy.orm import Session
from src.data.customers import generate_customer_data
from src.data.orders import generate_orders_data
from src.data.products import generate_products_data
from src.database import get_session
from src.models import Customer, Order, Product
from src.schemas import CustomerSchema, OrderSchema, ProductSchema

logger.remove(0)
log_format = (
    '{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {file}:{line} - {message}'
)
logger.add('src.log', format=log_format)
logger.add(sys.stderr, format=log_format)


def populate_table(
    session: Session, model, schema, data_generator, num_records: int
) -> None:
    """
    Generic function to populate a database table.
    - session: SQLAlchemy session
    - model: SQLAlchemy ORM models
    - schema: Pydantic schema
    - data_generator: Function that generates random data
    - num_records: Number of records to generate
    """
    try:
        logger.info(
            f'Generating {num_records} records for {model.__name__}...'
        )
        data = [data_generator() for _ in range(num_records)]

        # Validate data using Pydantic
        validated_data = [schema.model_validate(d) for d in data]

        # Convert to ORM models
        models = [model(**d.model_dump()) for d in validated_data]

        session.bulk_save_objects(models)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.exception(f'Error inserting into {model.__tablename__}: {e}')
    finally:
        session.close()


def load_data(session: Session) -> None:
    """Loads data into all tables."""
    populate_table(
        session,
        Customer,
        CustomerSchema,
        generate_customer_data,
        num_records=1_000,
    )
    populate_table(
        session,
        Product,
        ProductSchema,
        generate_products_data,
        num_records=100,
    )
    populate_table(
        session, Order, OrderSchema, generate_orders_data, num_records=10_000
    )


if __name__ == '__main__':
    start_time = datetime.now()

    with get_session() as session:
        load_data(session)

    end_time = datetime.now()
    execution_time = end_time - start_time
    logger.info(f'Tempo de execução: {execution_time}')
