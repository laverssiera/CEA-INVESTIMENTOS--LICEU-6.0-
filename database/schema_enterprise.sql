-- CEA 6.0 Enterprise Schema Extensions

-- FINANCE OS CORE
CREATE TABLE IF NOT EXISTS wallets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL,
    owner_type VARCHAR(50) NOT NULL, -- 'SUPPLIER', 'USER', 'HOLDING', 'PROJECT'
    balance NUMERIC(20,2) DEFAULT 0,
    currency VARCHAR(10) DEFAULT 'BRL',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ledger_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_id UUID REFERENCES wallets(id),
    entry_type VARCHAR(50), -- 'DEBIT', 'CREDIT'
    amount NUMERIC(20,2),
    description TEXT,
    reference_type VARCHAR(50), -- 'PIX', 'RWA_YIELD', 'LOAN'
    reference_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RWA & TOKENIZATION
CREATE TABLE IF NOT EXISTS rwa_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID, -- ARCHIMEDES Project Ref
    asset_name VARCHAR(255),
    asset_type VARCHAR(100), -- 'REAL_ESTATE', 'ENERGY', 'LOGISTICS'
    token_supply NUMERIC(20,2),
    token_price NUMERIC(20,2),
    roi_projection NUMERIC(10,2),
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- VENTURE LAB
CREATE TABLE IF NOT EXISTS venture_startups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    startup_name VARCHAR(255),
    founder_name VARCHAR(255),
    valuation NUMERIC(20,2),
    incubation_stage VARCHAR(100),
    ecosystem_synergy_score NUMERIC(10,2),
    investment_status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
