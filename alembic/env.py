import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ─────────────────────────────────────────────────────────────
# Add project root to PYTHONPATH so Alembic can import app modules
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # D:/agrichain-connect
sys.path.append(BASE_DIR)

# ─────────────────────────────────────────────────────────────
# Alembic Config object
# ─────────────────────────────────────────────────────────────
config = context.config

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ─────────────────────────────────────────────────────────────
# Import Base + ALL Models
# ─────────────────────────────────────────────────────────────
from app.database.connection import Base

# Import all models so Alembic knows the tables
# Add your models here as they are created
try:
    from app.models.user import User
    from app.models.farmer import Farmer
    # from app.models.vendor import Vendor
    # from app.models.product import Product
    # from app.models.order import Order
    # from app.models.activity_log import ActivityLog
except ImportError:
    # Safe fallback – prevents Alembic crashes when models don't exist yet
    pass

# Alembic needs this to autogenerate migrations
target_metadata = Base.metadata


# ─────────────────────────────────────────────────────────────
# OFFLINE MIGRATIONS
# ─────────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """Run migrations without connecting to the DB."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ─────────────────────────────────────────────────────────────
# ONLINE MIGRATIONS
# ─────────────────────────────────────────────────────────────
def run_migrations_online() -> None:
    """Run migrations with actual DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ─────────────────────────────────────────────────────────────
# MODE SWITCH
# ─────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
