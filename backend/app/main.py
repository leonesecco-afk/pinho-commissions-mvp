from fastapi import FastAPI
from .routers import health, seed

app = FastAPI(title="Pinho Commissions API")

# Include routers
app.include_router(health.router)
app.include_router(seed.router)
