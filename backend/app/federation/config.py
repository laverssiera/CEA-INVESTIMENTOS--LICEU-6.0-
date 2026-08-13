from pydantic_settings import BaseSettings

class FederationSettings(BaseSettings):

    MONOLITH_NAME: str = "cea-investimentos"

    NATS_URL: str = "nats://localhost:4222"

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "liceu"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"

    BACEN_RUNTIME_ENABLED: bool = True
    CVM_RUNTIME_ENABLED: bool = True
    AML_RUNTIME_ENABLED: bool = True

    ORBITAL_BANKING_RUNTIME: bool = True
    INTERPLANETARY_TREASURY: bool = True

settings = FederationSettings()
