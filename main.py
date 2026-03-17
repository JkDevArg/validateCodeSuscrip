from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime, timedelta
import random
import string
import json
import os

# Inicializar FastAPI
app = FastAPI(title="Bloq API")

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Archivo para persistir el código y fecha
CODE_FILE = "code_data.json"

def generate_code(length=12):
    """Genera un código aleatorio de números y letras"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def load_code_data():
    """Carga el código y fecha desde archivo"""
    if os.path.exists(CODE_FILE):
        with open(CODE_FILE, 'r') as f:
            data = json.load(f)
            data['created_at'] = datetime.fromisoformat(data['created_at'])
            return data
    return None

def save_code_data(code, created_at):
    """Guarda el código y fecha en archivo"""
    with open(CODE_FILE, 'w') as f:
        json.dump({
            'code': code,
            'created_at': created_at.isoformat()
        }, f)

def get_current_code():
    """Obtiene el código actual o genera uno nuevo si han pasado 5 días"""
    data = load_code_data()
    now = datetime.now()
    
    # Si no existe código o han pasado 5 días, generar uno nuevo
    if data is None or (now - data['created_at']) > timedelta(days=5):
        new_code = generate_code()
        save_code_data(new_code, now)
        return new_code, now
    
    return data['code'], data['created_at']

@app.get("/")
def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Bloq API - Validación de código",
        "endpoints": {
            "/bloq": "Valida un código (parámetro: code)",
            "/info": "Información sobre el código actual"
        }
    }

@app.get("/bloq")
@limiter.limit("10/minute")  # Máximo 10 requests por minuto
async def validate_code(request: Request, code: str = None):
    """
    Valida el código enviado
    Parámetros:
        code: Código a validar
    """
    if code is None:
        raise HTTPException(
            status_code=400, 
            detail="Parámetro 'code' es requerido. Ejemplo: /bloq?code=abc123"
        )
    
    current_code, created_at = get_current_code()
    
    # Validar el código
    if code == current_code:
        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "message": "Código válido",
                "validated_at": datetime.now().isoformat()
            }
        )
    else:
        raise HTTPException(
            status_code=401,
            detail="Código inválido"
        )

@app.get("/info")
@limiter.limit("5/minute")
async def code_info(request: Request):
    """Información sobre el código actual (sin revelar el código)"""
    current_code, created_at = get_current_code()
    days_remaining = 5 - (datetime.now() - created_at).days
    
    return {
        "code_length": len(current_code),
        "created_at": created_at.isoformat(),
        "days_until_refresh": max(0, days_remaining),
        "will_refresh_at": (created_at + timedelta(days=5)).isoformat()
    }

# Endpoint secreto para obtener el código actual (solo para desarrollo/testing)
@app.get("/admin/get-code")
@limiter.limit("5/hour")
async def get_code_admin(request: Request, admin_key: str = None):
    """
    Endpoint administrativo para obtener el código actual
    En producción, debes proteger esto con autenticación real
    """
    # Cambiar esta clave por una segura en producción
    ADMIN_KEY = os.getenv("ADMIN_KEY", "tu-clave-secreta-12345")
    
    if admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    current_code, created_at = get_current_code()
    return {
        "code": current_code,
        "created_at": created_at.isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
