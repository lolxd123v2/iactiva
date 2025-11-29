# Generador de Facturas Electrónicas SUNAT con IA

## Descripción

Esta aplicación permite generar facturas electrónicas según los estándares de la SUNAT (Superintendencia Nacional de Aduanas y de Administración Tributaria) del Perú, utilizando inteligencia artificial para procesar textos descriptivos y convertirlos en facturas estructuradas.

## Características

- 🚀 Extracción automática de datos de facturación a partir de texto libre
- 🤖 Integración con la API de Google Gemini para procesamiento de lenguaje natural
- 📄 Generación de facturas electrónicas en formato PDF
- 🧮 Cálculo automático de IGV (18%) y totales
- 🆔 Generación de RUC simulados cuando no se proporciona
- 🖥 Interfaz de línea de comandos y API web

## Requisitos

- Python 3.7 o superior
- Conexión a Internet (para acceder a la API de Google Gemini)
- Una clave de API de Google Gemini

## Instalación

1. Clona el repositorio:
   bash
   git clone [URL_DEL_REPOSITORIO]
   cd AppIA
   

2. Instala las dependencias:
   bash
   pip install fpdf requests python-dotenv
   

3. Crea un archivo .env en la raíz del proyecto con tu clave de API de Google Gemini:
   
   GEMINI_API_KEY=tu_clave_aquí
   

## Uso

### Modo Línea de Comandos

1. Ejecuta el script principal:
   bash
   python app.py
   

2. Ingresa la descripción de la factura cuando se te solicite. Por ejemplo:
   
   Factura a Tech Solutions SAC con RUC 20567894563 por 5 laptops a 3500 soles cada una
   

### Como API Web

1. Inicia el servidor web:
   bash
   python app.py
   

2. Realiza una petición POST a http://localhost:5000/generar-factura con el siguiente formato:
   json
   {
     "descripcion": "Factura a Tech Solutions SAC con RUC 20567894563 por 5 laptops a 3500 soles cada una"
   }
   

## Estructura del Proyecto

- app.py: Aplicación principal con la lógica de negocio y la API web
- factura_pdf.py: Clase para generar facturas en formato PDF
- invoice_agent.py: Módulo para interactuar con la API de Google Gemini
- Cuestionario.html: Interfaz de usuario web (si está implementada)

## Formato de Salida

La aplicación genera facturas en formato PDF con la siguiente estructura:
- Información del emisor
- Datos del cliente
- Tabla de ítems con descripción, cantidad, precio unitario y subtotal
- Totales (subtotal, IGV y total)

## Configuración

Puedes modificar las siguientes constantes en app.py:
- GEMINI_MODEL: Modelo de Gemini a utilizar
- IGV_RATE: Tasa de IGV (actualmente 18% para Perú)
- API_URL: URL de la API de Google Gemini

## Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu característica (git checkout -b feature/nueva-funcionalidad)
3. Haz commit de tus cambios (git commit -am 'Añade nueva funcionalidad')
4. Haz push a la rama (git push origin feature/nueva-funcionalidad)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más información.