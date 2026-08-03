-- Ledger (double entry)
CREATE TABLE IF NOT EXISTS ledger_entries (
    id UUID PRIMARY KEY,
    entity_id UUID,
    debit_account VARCHAR(100),
    credit_account VARCHAR(100),
    amount NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Wallets
CREATE TABLE IF NOT EXISTS wallets (
    id UUID PRIMARY KEY,
    owner VARCHAR(100),
    balance NUMERIC DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Investments
CREATE TABLE IF NOT EXISTS investments (
    id UUID PRIMARY KEY,
    entity_id UUID,
    amount NUMERIC,
    expected_roi FLOAT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
