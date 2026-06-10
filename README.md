# Pipeline de Optimización y Analítica: Call Center

<p align="center">
  <img src="img\Representación_Caso_Call_Center.png" alt="Arquitectura del Pipeline" width="100%">
</p>

Este proyecto despliega un flujo de procesamiento de datos distribuido (**ETL**) estructurado profesionalmente para el Centro de Contacto de una empresa del rubro Seguro/Banca. El objetivo principal es extraer, consolidar, limpiar y transformar las métricas de telefonía de la plataforma **Genesys** cruzándolas con los perfiles comerciales del **CRM corporativo**, garantizando la disponibilidad de KPIs críticos y bases de marcación optimizadas para tableros de control en **Power BI**.

---

## Reto del Negocio e Impacto Operacional
En la operación diaria de un Call Center de rubro Seguro/Banca, la integridad y la velocidad de los datos determinan la calidad del servicio. Este pipeline resuelve problemas críticos de calidad de datos transaccionales:
* **Depuración de Logs Inconsistentes:** Corrección automatizada de falsos abandonos (llamadas caídas con tiempo registrado por desincronización de red).
* **Sanitización de Contactos (Data Wrangling):** Estandarización y purga de caracteres alfanuméricos en números telefónicos mediante expresiones regulares (**Regex**).
* **Métricas Core de Gestión:** Automatización del cálculo del **AHT (Average Handling Time)** y la **Tasa de Abandono** particionado por colas de atención.
* **Estrategia de Recupero Comercial:** Generación dinámica de bases de marcación saliente para el contacto proactivo de clientes de alto valor (**Premium/Gold**).

---

## Ecosistema Tecnológico
El pipeline está diseñado bajo una arquitectura híbrida optimizada tanto para desarrollo ágil local (**VS Code / Google Colab**) como para el despliegue a gran escala en un Lakehouse corporativo (**Databricks**):

* **Python 3.x:** Motor principal de automatización y scripting.
* **Apache Spark (PySpark & Spark SQL):** Procesamiento distribuido para la manipulación eficiente de Big Data.
* **Pandas:** Conversión y estructuración para reportería secundaria y análisis interactivo.
* **Regex (`re`):** Validaciones complejas de integridad en cadenas de texto.
* **Logging & Try-Except:** Control estricto de excepciones para ejecuciones desatendidas en producción.

---

## Diccionario de Datos

### 1. Tabla: `Log_Interacciones.csv` (Métricas de Telefonía - Genesys)
Registra el rastro transaccional e histórico de cada llamada entrante y saliente.
* **`Interaction_ID` (String):** Identificador único de la llamada (**Llave Primaria**). Permite la auditoría individual de los contactos.
* **`Customer_ID` (String):** Código de identificación único del cliente (**Llave Foránea**). Conecta la llamada con los datos comerciales.
* **`Call_Date` (Date):** Fecha de ejecución de la llamada. Esencial para análisis de series de tiempo y particionamiento físico de la data.
* **`Duration_Seconds` (Integer):** Tiempo de conversación neto en segundos. Base analítica para el cálculo de la eficiencia de los asesores.
* **`Status` (String):** Estado final de la interacción. Valores permitidos:
  * `Answered`: Conversación establecida de forma exitosa.
  * `Abandoned`: El cliente finalizó la llamada en cola de espera antes de ser atendido.
* **`Queue` (String):** Línea de negocio asignada a la llamada (`Ventas`, `Soporte`, `Retenciones`, `Reclamos`).

### 2. Tabla: `Maestro_Clientes.csv` (Perfil Comercial - CRM)
Contiene la información demográfica y la estrategia comercial del cliente.
* **`Customer_ID` (String):** Identificador único del cliente (**Llave Primaria**). Garantiza unicidad en la capa dimensional.
* **`Customer_Name` (String):** Nombre completo del usuario Seguro/Banca.
* **`Segment` (String):** Clasificación de valor comercial del cliente (`Premium`, `Gold`, `Regular`). Define la prioridad en las reglas de ruteo y colas de espera.
* **`Phone_Number` (String):** Teléfono registrado. Es el objetivo principal del proceso de sanitización para las campañas de salida.
* **`Has_Active_Campaign` (String):** Flag comercial (`SI` / `NO`) que denota si el cliente cuenta con una oferta o producto aprobado disponible para venta cruzada.

---

## Arquitectura del Pipeline (Procesamiento ETL)

El flujo opera bajo un modelo de integración continua para optimizar canales de atención:

**Entradas (Inputs Dedicados):**
   * `Log_Interacciones.csv`: Métricas transaccionales de telefonía y canales de atención.
   * `Maestro_Clientes.csv`: Datos demográficos y capas comerciales del CRM.

**Procesamiento (Engine):**
   * Consolidación en memoria mediante Spark SQL y transformaciones nativas de Python.

**Salidas (Outputs de Impacto):**
   * **Analítica Operativa:** KPIs de productividad (AHT, Tasas de Abandono) directo a tableros de Power BI.
   * **Base de Marcación Saliente Limpia:** Lista depurada y priorizada comercialmente que se reinyecta al marcador automático para campañas de recupero de clientes críticos.

Es necesario entender el siguiente flujo y consideraciones que se abordaran en esta casuísitica:

1. **Extracción (Extract):** Inicialización del entorno mediante `SparkSession` y lectura optimizada de planos CSV con inferencia de esquemas y tipado estricto.
2. **Transformación (Transform):**
   * **Limpieza:** Regla de negocio que fuerza `Duration_Seconds = 0` cuando `Status = 'Abandoned'`.
   * **Estandarización:** Expresiones regulares para limpiar campos de contacto mal digitados y mapeo de excepciones con la etiqueta `REVISAR_TELEFONO`.
   * **Analítica Avanzada:** Ventanas lógicas con `ROW_NUMBER()` para calcular la reincidencia e identificar problemas crónicos no resueltos en el primer contacto.
   * **Clasificación:** Segmentación analítica por nivel de complejidad operativa mediante cláusulas `CASE WHEN`.
3. **Carga (Load):** Disponibilización de las capas limpias en vistas temporales compatibles con **Spark SQL** y exportación automatizada de reportes particionados por colas críticas.

---

## Estructura del Proyecto

Jerarquía de directorios diseñada en **Visual Studio Code** para asegurar modularidad y permitir pruebas interactivas mediante kernels de Jupyter locales:

```text
negocio-callcenter-pipeline/
│
├── data/                             <-- Almacenamiento local de datos (Ignorado en Git)
│   ├── raw/                          <-- Archivos crudos de entrada (CSV)
│   │   ├── Log_Interacciones.csv
│   │   └── Maestro_Clientes.csv
│   └── processed/                    <-- Salidas limpias generadas por el pipeline
│
├── logs/                             <-- Bitácoras de errores de los servidores
│   └── error_pipeline.txt
│
├── notebooks/                        <-- Cuadernos de experimentación y análisis
│   └── sandbox_etl.ipynb             <-- Código interactivo (Compatible con Google Colab)
│
├── src/                              <-- Código fuente modular ejecutable en producción
│   ├── __init__.py
│   ├── extraction.py                 <-- Inicialización de Spark y lecturas
│   ├── transformation.py             <-- Lógicas de limpieza, Regex y Queries SQL
│   └── load.py                       <-- Escritura y generación de reportes
│
├── .gitignore                        <-- Exclusión de archivos pesados de data y entorno
├── main.py                           <-- Orquestador principal del pipeline ETL
├── README.md                         <-- Documentación principal del proyecto
└── requirements.txt                  <-- Lista de librerías esenciales para pip