from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import PaidHistory
import csv
import hashlib

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/seed/paid-history")
async def seed_paid_history(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Seed initial paid history from a CSV file.
    Expected CSV columns: service,mes_competencia,cnpj_cliente,nome_cliente,numero_referencia,valor_informado,colaborador_ref,status_pagamento
    """
    try:
        contents = await file.read()
        # Decode bytes to string and create a CSV reader
        text = contents.decode("utf-8")
        reader = csv.DictReader(text.splitlines())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {e}")

    inserted = 0
    skipped = 0
    for row in reader:
        # Build duplicate key based on service, CNPJ, reference and month
        dup_key = f"{row['service']}|{row['cnpj_cliente']}|{row['numero_referencia']}|{row['mes_competencia']}"
        dup_hash = hashlib.sha256(dup_key.encode("utf-8")).hexdigest()
        # Check if already exists
        existing = db.query(PaidHistory).filter_by(dup_hash=dup_hash).first()
        if existing:
            skipped += 1
            continue
        # Convert value to float if possible
        valor = None
        if row.get("valor_informado"):
            try:
                valor = float(row["valor_informado"].replace(",", "."))
            except ValueError:
                valor = None
        ph = PaidHistory(
            service=row.get("service"),
            mes_competencia=row.get("mes_competencia"),
            cnpj_cliente=row.get("cnpj_cliente"),
            nome_cliente=row.get("nome_cliente"),
            numero_referencia=row.get("numero_referencia"),
            valor_informado=valor,
            colaborador_ref=row.get("colaborador_ref"),
            status_pagamento=row.get("status_pagamento", "PAGO"),
            dup_key=dup_key,
            dup_hash=dup_hash,
        )
        db.add(ph)
        inserted += 1
    db.commit()
    return {"inserted": inserted, "skipped": skipped}
