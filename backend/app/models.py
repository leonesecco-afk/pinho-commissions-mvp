from sqlalchemy import Column, Integer, String, Float
from .db import Base


class PaidHistory(Base):
    __tablename__ = "paid_history"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String(255), nullable=False)
    mes_competencia = Column(String(7), nullable=False)  # YYYY-MM
    cnpj_cliente = Column(String(20), nullable=False)
    nome_cliente = Column(String(255), nullable=True)
    numero_referencia = Column(String(255), nullable=False)
    valor_informado = Column(Float, nullable=True)
    colaborador_ref = Column(String(255), nullable=True)
    status_pagamento = Column(String(50), nullable=False, default="PAGO")
    dup_key = Column(String(255), nullable=False, unique=True)
    dup_hash = Column(String(64), nullable=False, unique=True)
