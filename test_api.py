"""
Script de prueba para la API Bloq
Ejecuta esto después de iniciar la API con: python main.py
"""
import requests
import time

# URL base (cambiar según donde esté corriendo)
BASE_URL = "http://localhost:8000"

print("🧪 Probando API Bloq\n")

# 1. Probar endpoint raíz
print("1️⃣ Probando GET /")
response = requests.get(f"{BASE_URL}/")
print(f"   Status: {response.status_code}")
print(f"   Respuesta: {response.json()}\n")

# 2. Obtener información del código
print("2️⃣ Probando GET /info")
response = requests.get(f"{BASE_URL}/info")
print(f"   Status: {response.status_code}")
print(f"   Respuesta: {response.json()}\n")

# 3. Obtener el código actual (usando admin endpoint)
print("3️⃣ Obteniendo código actual (admin)")
response = requests.get(f"{BASE_URL}/admin/get-code", params={"admin_key": "tu-clave-secreta-12345"})
if response.status_code == 200:
    code_data = response.json()
    current_code = code_data['code']
    print(f"   ✅ Código actual: {current_code}\n")
else:
    print(f"   ❌ Error: {response.json()}\n")
    current_code = None

# 4. Probar validación con código correcto
if current_code:
    print(f"4️⃣ Probando validación con código CORRECTO: {current_code}")
    response = requests.get(f"{BASE_URL}/bloq", params={"code": current_code})
    print(f"   Status: {response.status_code}")
    print(f"   Respuesta: {response.json()}\n")

# 5. Probar validación con código incorrecto
print("5️⃣ Probando validación con código INCORRECTO")
response = requests.get(f"{BASE_URL}/bloq", params={"code": "codigo-falso-123"})
print(f"   Status: {response.status_code}")
print(f"   Respuesta: {response.json()}\n")

# 6. Probar sin parámetro code
print("6️⃣ Probando sin parámetro 'code'")
response = requests.get(f"{BASE_URL}/bloq")
print(f"   Status: {response.status_code}")
print(f"   Respuesta: {response.json()}\n")

# 7. Probar rate limiting (hacer muchas requests rápidas)
print("7️⃣ Probando rate limiting (11 requests rápidas)")
for i in range(11):
    response = requests.get(f"{BASE_URL}/bloq", params={"code": "test"})
    print(f"   Request {i+1}: Status {response.status_code}")
    if response.status_code == 429:
        print(f"   ⚠️  Rate limit alcanzado! {response.json()}")
        break
    time.sleep(0.1)

print("\n✅ Pruebas completadas!")
