import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add project root + app folder to PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # D:/agrichain-connect
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

# Alembic Config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import Base
from app.database.connection import Base

# Import models so Alembic can see tables
try:
    from app.models.user import User
    from app.models.farmer import Farmer
    from app.models.vendor import Vendor
    from app.models.produce import Produce
    from app.models.activity_logs import ActivityLog
    from app.models.order import Order

except ImportError as e:
    print("Model import warning:", e)

# Metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
