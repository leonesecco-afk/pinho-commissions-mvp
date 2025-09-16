-- SQL migrations for Pinho Commissions MVP
-- Create paid_history table to store historical commissions already paid
CREATE TABLE IF NOT EXISTS paid_history (
    id SERIAL PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    mes_competencia VARCHAR(20) NOT NULL,
    cnpj_cliente VARCHAR(50) NOT NULL,
    nome_cliente VARCHAR(255),
    numero_referencia VARCHAR(255),
    valor_informado NUMERIC,
    colaborador_ref VARCHAR(255),
    status_pagamento VARCHAR(50),
    dup_key VARCHAR(512),
    dup_hash VARCHAR(64) UNIQUE
);
