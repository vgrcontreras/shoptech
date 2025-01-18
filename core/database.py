from sqlalchemy import create_engine
from sqlalchemy.orm import registry

from core.settings import settings

table_registry = registry()

engine = create_engine(settings.DATABASE_URL)
