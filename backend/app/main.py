from fastapi import Depends, FastAPI

from app import config
from app.routers import smiles_router
from app.utils import get_logger
from app.oracle import OracleConnection

logger = get_logger(__name__)


app = FastAPI(title="ChemCompoundsSMILES", version="1.0")
app.include_router(smiles_router)


@app.get("/")
async def home():
    return {"home": "Home endpoint"}


@app.get("/health-check")
async def health_check(settings: config.Settings = Depends(config.get_settings)):
    try:
        with OracleConnection(settings.oracle_username,
                              settings.oracle_password,
                              settings.oracle_host,
                              settings.oracle_port,
                              settings.oracle_sid) as con:
            sql_stmt = "SELECT sys_context('USERENV', 'CURRENT_USER') FROM dual"
            with con.cursor() as cursor:
                cursor.execute(sql_stmt)
                output = cursor.fetchall()
                output = output[0][0]
    except Exception as e:
        logger.exception(f"error running health-check - {e}")
        output = None
    return {"testing": settings.testing,
            "environment": settings.environment,
            "return": output}
