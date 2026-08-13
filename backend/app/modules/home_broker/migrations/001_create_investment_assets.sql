CREATE TABLE investment_assets (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(32) NOT NULL,
    name VARCHAR(150) NOT NULL,
    price NUMERIC(14,2) NOT NULL,
    yield NUMERIC(5,2) NOT NULL,
    risk VARCHAR(20) NOT NULL
);
