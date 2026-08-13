import os


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/cea")
    NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")
    NATS_STREAM = os.getenv("NATS_STREAM", "CEA_EVENTS")
    NATS_CONSUMER = os.getenv("NATS_CONSUMER", "cea_finance_consumer")


settings = Settings()
