from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import requests
import time
from datetime import datetime
import os

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})

#CONFIGURACIÓN
API_KEY = "AIzaSyDeRizFJtUiyOjpTafp4ZMtdffWclmj6nU" 

GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
MAX_RETRIES = 3
IGV_RATE = 0.18

SYSTEM_PROMPT = """
Actúa como un asistente contable y agente de facturación de estilo SUNAT en Perú. 
Tu tarea es extraer los datos clave de facturación del texto proporcionado y devolver la información ESTRICTAMENTE en el formato JSON definido en el esquema.
1. Si el usuario no da RUC, usa '20123456789'.
2. Precios son unitarios sin IGV.
3. Extrae la moneda (S/ o $), si no se menciona asume 'S/'.
"""

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "cliente": { "type": "STRING" },
        "ruc_simulado": { "type": "STRING" },
        "moneda": { "type": "STRING" },
        "items_extraidos": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "descripcion": {"type": "STRING"},
                    "cantidad": {"type": "NUMBER"},
                    "precio_unitario_sin_igv": {"type": "NUMBER"}
                },
                "required": ["descripcion", "cantidad", "precio_unitario_sin_igv"]
            }
        },
        "fecha_emision": { "type": "STRING" }
    },
    "required": ["cliente", "ruc_simulado", "items_extraidos"]
}

def call_gemini_api(prompt):
    """Conecta con Google Gemini para extraer datos"""
    if API_KEY == "TU_API_KEY_AQUI" or not API_KEY:
        print("[ERROR] Falta la API KEY en app.py")
        return None

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA
        },
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]}
    }
    
    url_with_key = f"{API_URL}?key={API_KEY}"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(url_with_key, json=payload)
            response.raise_for_status()
            
            json_text = response.json()['candidates'][0]['content']['parts'][0]['text']
            return json.loads(json_text)
        except Exception as e:
            print(f"[Intento {attempt+1}] Error conectando a Gemini: {e}")
            time.sleep(1) # Esperar un poco antes de reintentar
            
    return None

def calculate_totals(extracted_data):
    """Calcula IGV y Totales (Lógica de Negocio)"""
    subtotal_general = 0.0
    processed_items = []
    
    # Obtener moneda o usar Soles por defecto
    moneda = extracted_data.get("moneda", "S/")

    for item in extracted_data.get("items_extraidos", []):
        try:
            cant = float(item.get("cantidad", 0))
            prec = float(item.get("precio_unitario_sin_igv", 0))
            sub = cant * prec
            subtotal_general += sub
            
            processed_items.append({
                "descripcion": item.get("descripcion", "Item sin nombre"),
                "cantidad": cant,
                "precio_unitario_sin_igv": prec,
                "sub_total_item": round(sub, 2)
            })
        except ValueError:
            continue # Saltar items con datos corruptos

    igv = subtotal_general * IGV_RATE
    total = subtotal_general + igv

    # Estructura final para el Frontend
    return {
        "cliente": extracted_data.get("cliente", "Cliente Genérico"),
        "ruc_simulado": extracted_data.get("ruc_simulado", "00000000000"),
        "fecha_emision": extracted_data.get("fecha_emision", datetime.now().strftime('%Y-%m-%d')),
        "moneda": moneda,
        "items": processed_items,
        "subtotal": round(subtotal_general, 2),
        "igv": round(igv, 2),
        "total": round(total, 2),
        "igv_porcentaje": IGV_RATE * 100
    }

# --- RUTAS DEL SERVIDOR ---

@app.route('/')
def home():
    """Ruta principal: Sirve el archivo HTML"""
    # IMPORTANTE: Asegúrate de que tu archivo se llame 'Cuestionario.html' 
    # y esté en la misma carpeta.
    try:
        return send_file('Cuestionario.html')
    except FileNotFoundError:
        return "<h1>Error: No encuentro el archivo 'Cuestionario.html'. Verifica el nombre.</h1>"

@app.route('/api/generar-factura', methods=['POST'])
def generar_factura():
    """Endpoint API que recibe el texto y devuelve la factura calculada"""
    data = request.json
    prompt_text = data.get('prompt', '')

    if not prompt_text:
        return jsonify({"error": "El prompt está vacío"}), 400

    print(f"[INFO] Procesando solicitud: {prompt_text[:30]}...")
    
    # 1. Llamar a la IA
    extracted_data = call_gemini_api(prompt_text)
    
    if not extracted_data:
        return jsonify({"error": "Error al procesar con la IA (Verifica tu API Key o conexión)"}), 500

    # 2. Calcular montos
    final_invoice = calculate_totals(extracted_data)

    print("[INFO] Factura generada y enviada al front.")
    return jsonify(final_invoice)

if __name__ == '__main__':
    # Ejecutar en modo debug en el puerto 5001
    print("--- SERVIDOR INICIADO ---")
    print("Entra a: http://localhost:5001")
    app.run(debug=True, port=5001)