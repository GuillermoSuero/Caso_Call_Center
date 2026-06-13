# Pipeline de Optimización y Analítica: Call Center

<p align="center">
  <img src="img\Representación_Caso_Call_Center.png" alt="Arquitectura del Pipeline" width="100%">
</p>

### Caso Call Center: Pipeline de Procesamiento de Datos (ETL)

Este proyecto despliega un flujo de procesamiento de datos (ETL) estructurado profesionalmente para el Centro de Contacto de una empresa del rubro Seguro/Banca. El objetivo principal es extraer, consolidar, limpiar y transformar las métricas de telefonía de la plataforma de Call Center cruzándolas con los perfiles comerciales del CRM corporativo, garantizando la disponibilidad de KPIs críticos y bases de marcación optimizadas para tableros de control en Power BI.

### Reto del Negocio e Impacto Operacional
En la operación diaria de un Call Center del rubro Seguro/Banca, la integridad y la velocidad de los datos determinan la calidad del servicio. Este pipeline resuelve problemas críticos de calidad de datos transaccionales:

* **Depuración de Logs Inconsistentes:** Corrección automatizada de falsos abandonos (llamadas caídas con tiempo registrado por desincronización de red).
* **Sanitización de Contactos (Data Wrangling):** Estandarización y purga de caracteres alfanuméricos en números telefónicos mediante expresiones regulares (Regex).
* **Métricas Core de Gestión:** Automatización del cálculo del AHT (Average Handling Time) y la Tasa de Abandono particionado por colas de atención.
* **Estrategia de Recupero Comercial:** Generación dinámica de bases de marcación saliente para el contacto proactivo de clientes de alto valor (Premium/Gold).

### Ecosistema Tecnológico
El pipeline está diseñado bajo una arquitectura optimizada para el desarrollo ágil, control de memoria y estabilidad en entornos de desarrollo locales o contenedores (GitHub Codespaces):

* **Python 3.x:** Motor principal de automatización y scripting.
* **Pandas:** Librería central para el procesamiento en memoria, manipulación de DataFrames, transformaciones lógicas y uniones de tablas.
* **Openpyxl:** Motor de descompresión y lectura de archivos estructurados modernos de Microsoft Excel (.xlsx).
* **Regex (re):** Validaciones complejas de integridad y limpieza en cadenas de texto.
* **Logging & Try-Except:** Control estricto de excepciones para ejecuciones desatendidas en producción.

### Diccionario de Datos

#### 1. Tabla: Log_Interacciones (Métricas de Telefonía)
Registra el rastro transaccional e histórico de cada llamada entrante y saliente. Ubicado en formato Excel.

* **Interaction_ID (String):** Identificador único de la llamada (Llave Primaria). Permite la auditoría individual de los contactos.
* **Customer_ID (String):** Código de identificación único del cliente (Llave Foránea). Conecta la llamada con los datos comerciales.
* **Call_Date (Date):** Fecha de ejecución de la llamada. Esencial para análisis de series de tiempo y particionamiento físico de la data.
* **Duration_Seconds (Integer):** Tiempo de conversación neto en segundos. Base analítica para el cálculo de la eficiencia de los asesores.
* **Status (String):** Estado final de la interacción. Valores permitidos: `Answered` (Conversación establecida) o `Abandoned` (El cliente finalizó la llamada en cola de espera).
* **Queue (String):** Línea de negocio asignada a la llamada (Ventas, Soporte, Retenciones, Reclamos).

#### 2. Tabla: Maestro_Clientes (Perfil Comercial - CRM)
Contiene la información demográfica y la estrategia comercial del cliente. Ubicado en formato Excel.

* **Customer_ID (String):** Identificador único del cliente (Llave Primaria). Garantiza unicidad en la capa dimensional.
* **Customer_Name (String):** Nombre completo del usuario Seguro/Banca.
* **Segment (String):** Clasificación de valor comercial del cliente (Premium, Gold, Regular). Define la prioridad en las reglas de ruteo.
* **Phone_Number (String):** Teléfono registrado. Objetivo principal del proceso de sanitización para las campañas de salida.
* **Has_Active_Campaign (String):** Flag comercial (SI / NO) que denota si el cliente cuenta con una oferta disponible para venta cruzada.

### Arquitectura del Pipeline (Procesamiento ETL)

* **Extracción (Extract):** Validación de rutas mediante el sistema operativo y lectura optimizada de hojas de cálculo Excel (`.xlsx`) forzando la normalización de cabeceras en formato `Snake_Case` para eliminar espacios en blanco.
* **Transformación (Transform):**
  * **Limpieza:** Regla de negocio que fuerza `Duration_Seconds = 0` cuando `Status = 'Abandoned'`.
  * **Estandarización:** Uso de expresiones regulares para limpiar campos de contacto mal digitados y mapeo de excepciones con la etiqueta `REVISAR_TELEFONO`.
  * **Analítica Avanzada:** Identificación de reincidencias de contacto y problemas crónicos no resueltos.
  * **Clasificación:** Segmentación analítica por nivel de complejidad operativa.
* **Carga (Load):** Exportación automatizada de reportes limpios y unificados hacia el directorio de datos procesados.

### Estructura del Proyecto

```text
Caso_Call_Center/
│
├── data/                             <-- Almacenamiento local de datos (Ignorado en Git)
│   ├── raw/                          <-- Archivos crudos de entrada (Excel)
│   │   ├── Data_Robust_Call_Center_Log_Interacciones.xlsx
│   │   └── Data_Robust_Call_Center_Maestro_Clientes.xlsx
│   └── processed/                    <-- Salidas limpias generadas por el pipeline
│
├── notebooks/                        <-- Cuadernos de experimentación y análisis
│   └── sandbox_etl.ipynb             <-- Laboratorio de desarrollo paso a paso
│
├── src/                              <-- Código fuente modular ejecutable en producción
│   ├── __init__.py
│   ├── extraction.py                 <-- Funciones de lectura y normalización de cabeceras
│   ├── transformation.py             <-- Lógicas de limpieza, Regex y Queries
│   └── load.py                       <-- Escritura y generación de reportes finales
│
├── .gitignore                        <-- Exclusión de archivos pesados de data y entorno (venv)
├── instructions.txt                  <-- Especificaciones y requerimientos analíticos del caso
├── main.py                           <-- Orquestador principal del pipeline ETL
├── README.md                         <-- Documentación principal del proyecto
└── requirements.txt                  <-- Lista de librerías esenciales para pip