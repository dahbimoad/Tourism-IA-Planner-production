from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importez vos métadonnées ici
from app.db.database import Base  # Chemin vers vos métadonnées
from app.db.models import Plans, Preferences, User, Villes, Activities, Itineraires, Hotels, VilleItineraire, LieuxToVisit  # Assurez-vous d'importer tous vos modèles

# Ce `Base.metadata` sera utilisé pour l'autogénération
target_metadata = Base.metadata

# Configuration Alembic
config = context.config

# Configurez le fichier de log
fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
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

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
