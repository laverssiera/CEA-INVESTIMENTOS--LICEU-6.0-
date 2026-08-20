import os


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        os.getenv(
            "CANONICAL_EVENT_STORE_DATABASE_URL",
            "postgresql://db_core_os:5432/liceu_core_os",
        ),
    )
    NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")
    NATS_STREAM = os.getenv("NATS_STREAM", "CEA_EVENTS")
    NATS_CONSUMER = os.getenv("NATS_CONSUMER", "cea_finance_consumer")


settings = Settings()
