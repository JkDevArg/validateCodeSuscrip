# Bloq API - Validación de Códigos

API REST en Python con FastAPI para validar códigos que se regeneran automáticamente cada 5 días.

## 🚀 Características

- ✅ Código aleatorio de letras y números (12 caracteres)
- ✅ Se regenera automáticamente cada 5 días
- ✅ Rate limiting (10 requests/minuto en `/bloq`)
- ✅ Persistencia del código en archivo JSON
- ✅ Endpoints protegidos

## 📋 Endpoints

### 1. **GET /** 
Información de la API
```
https://tu-app.onrender.com/
```

### 2. **GET /bloq?code=TU_CODIGO**
Valida un código
```
https://tu-app.onrender.com/bloq?code=abc123XYZ456
```

**Respuesta exitosa (200):**
```json
{
  "status": "ok",
  "message": "Código válido",
  "validated_at": "2024-03-16T10:30:00"
}
```

**Respuesta error (401):**
```json
{
  "detail": "Código inválido"
}
```

### 3. **GET /info**
Información sobre el código actual (sin revelarlo)
```
https://tu-app.onrender.com/info
```

**Respuesta:**
```json
{
  "code_length": 12,
  "created_at": "2024-03-10T08:00:00",
  "days_until_refresh": 3,
  "will_refresh_at": "2024-03-15T08:00:00"
}
```

### 4. **GET /admin/get-code?admin_key=TU_CLAVE**
Obtener el código actual (admin)
```
https://tu-app.onrender.com/admin/get-code?admin_key=tu-clave-secreta-12345
```

## 🛠️ Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la API
python main.py
```

La API estará disponible en: `http://localhost:8000`

## 🌐 Desplegar en Render (GRATIS)

### Paso 1: Subir a GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/bloq-api.git
git push -u origin main
```

### Paso 2: Configurar Render

1. Ve a [Render.com](https://render.com) y regístrate
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name:** `bloq-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

5. En **Environment Variables** (opcional):
   - `ADMIN_KEY` = `tu-clave-super-secreta`

6. Click en **"Create Web Service"**

### Paso 3: Esperar el deploy
En 2-3 minutos tu API estará lista en:
```
https://bloq-api.onrender.com/bloq?code=TU_CODIGO
```

## 📝 Ejemplo de Uso

```python
import requests

# URL de tu API en Render
API_URL = "https://tu-app.onrender.com"

# Validar código
response = requests.get(f"{API_URL}/bloq", params={"code": "abc123XYZ456"})

if response.status_code == 200:
    print("✅ Código válido!")
    print(response.json())
else:
    print("❌ Código inválido")
```

```javascript
// En JavaScript
fetch('https://tu-app.onrender.com/bloq?code=abc123XYZ456')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

## 🔒 Rate Limiting

- `/bloq`: 10 requests por minuto por IP
- `/info`: 5 requests por minuto por IP
- `/admin/get-code`: 3 requests por hora por IP

Si excedes el límite recibirás error `429 Too Many Requests`.

## 📊 Cómo funciona el código

1. Al iniciar, se genera un código aleatorio de 12 caracteres
2. El código se guarda en `code_data.json` con su fecha de creación
3. Cada vez que alguien consulta `/bloq`, se verifica:
   - Si han pasado más de 5 días → se genera un nuevo código
   - Si no → se usa el código existente
4. El código se valida comparando exactamente (case-sensitive)

## 🔧 Personalización

En `main.py` puedes modificar:

```python
# Longitud del código (línea 22)
return ''.join(random.choice(characters) for _ in range(12))  # Cambiar 12

# Días para regenerar (líneas 49, 103)
timedelta(days=5)  # Cambiar 5

# Rate limits (líneas 71, 94, 108)
@limiter.limit("10/minute")  # Cambiar el límite
```

## ⚠️ Notas Importantes

- **Render Free Tier** se duerme después de 15 minutos de inactividad. La primera request después de dormir puede tardar ~30 segundos.
- El archivo `code_data.json` persiste entre reinicios en Render usando volúmenes.
- Cambia `ADMIN_KEY` por algo seguro en producción.

## 🆘 Soporte

Si tienes problemas:
1. Verifica los logs en Render Dashboard
2. Prueba localmente primero con `python main.py`
3. Asegúrate de tener Python 3.8+

---
Creado con FastAPI ❤️
