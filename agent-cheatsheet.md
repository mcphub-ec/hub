# 🤖 MCP Hub - Agent-First Cheatsheet & Documentation

> \[!IMPORTANT\] **Contexto para Agentes de IA**: Este documento sirve como mapa mental para que los LLMs comprendan el alcance de las herramientas disponibles en el ecosistema `mcphub-ec`. Úsalo para planificar qué servidor y qué herramienta llamar según la intención del usuario.

## 🏛️ Contabilidad (Accounting & SRI MCPs)

Estos repositorios contienen servidores que interactúan con el SRI (autoridad tributaria de Ecuador) y sistemas ERP locales.

### 1\. `mcphub-ec/mcp-sri` (SRI Nativo)

-   **Objetivo**: Emisión directa al SRI usando firmas `.p12` (XAdES-BES) y consultas públicas.
-   **Herramientas Principales**:
    
    -   `consultar_informacion_ruc`: Consulta información pública del contribuyente (razón social, estado tributario) directamente desde las bases del SRI. Útil para validar clientes antes de facturar.
    -   `generar_xml_v232`: Crea el esquema XML estándar del SRI v2.1.0. Calcula totales automáticamente.
    -   `firmar_xades_bes`: Firma digitalmente el XML usando el microservicio Java integrado.
    -   `comunicar_sri_recepcion` / `comunicar_sri_autorizacion`: Flujo de transmisión y validación.

### 2\. `mcphub-ec/mcp-contifico`

-   **Objetivo**: Integración completa de gestión y ERP.
-   **Herramientas Principales**:
    
    -   `listar_personas` / `crear_persona`: Gestión de clientes (necesario antes de facturar).
    -   `listar_productos` / `obtener_stock`: Consulta de inventario en tiempo real.
    -   `crear_documento`: Generación de facturas de venta o proformas.
    -   `crear_cobro_documento`: Conciliación y registro de pagos recibidos.

### 3\. `mcphub-ec/mcp-invoka`

-   **Objetivo**: Facturación delegada simplificada.
-   **Herramientas Principales**:
    
    -   `emitir_factura` / `emitir_nota_credito`: Genera el comprobante consumiendo créditos de la plataforma.

### 4\. `mcphub-ec/mcp-factuplan`

-   **Objetivo**: APIs especializadas para emisión de facturas electrónicas mediante el proveedor Factuplan.

### 5\. `mcphub-ec/mcp-facturasoft`

-   **Objetivo**: Conector para el sistema de emisión de comprobantes FacturaSoft.

### 6\. `mcphub-ec/mcp-perseo`

-   **Objetivo**: Integración directa con las capacidades del sistema ERP y contable Perseo.

## 💳 Pagos (Payments MCPs)

Procesamiento de pagos y pasarelas de cobro para Ecuador.

> \[!WARNING\] **Unidades Monetarias**: Casi todas las APIs de pagos en estos repositorios esperan los montos en **CENTAVOS** (ej: `$1.00` = `100`). Siempre verifica la unidad en la descripción de la herramienta antes de enviar los datos numéricos.

### 1\. `mcphub-ec/mcp-payphone`

-   **Objetivo**: Cobros rápidos y fáciles, muy populares en Ecuador.
-   **Herramientas Principales**:
    
    -   `create_payment_link`: Genera una URL web para que el usuario pague.
    -   `create_payphone_sale`: Envía una notificación Push directamente al celular del cliente.
    -   `get_transaction_status`: Verifica si el pago fue exitoso o rechazado.

### 2\. `mcphub-ec/mcp-kushki`

-   **Objetivo**: Procesamiento regional robusto.
-   **Herramientas Principales**: `tokenizar_tarjeta`, `crear_cargo`, `crear_transferencia`.

### 3\. `mcphub-ec/mcp-datafast`

-   **Objetivo**: Red tradicional ecuatoriana.
-   **Herramientas Principales**: `checkout_id`, `verificar_estado`.

### 4\. `mcphub-ec/mcp-pagomedios`

-   **Objetivo**: Ecosistema Abitmedia para generar solicitudes de cobro y tracking de pagos integrados.

## 🔒 Manejo de Credenciales (Instrucción Estricta)

1.  **Variables de Entorno Locales**: Los servidores NO usan bases de datos para guardar secretos. Requieren que variables como `EMITTER_RUC`, `CERTIFICATE_PATH`, `PAYPHONE_TOKEN`, etc., existan en el entorno (generalmente pasadas a través de `.env`).
2.  **Verificación Previa**: Antes de llamar a una herramienta que falle por falta de autenticación, verifica si tienes las variables requeridas en tu contexto o si necesitas pedirle al usuario que las configure.

## 💡 Best Practices para Agentes (Reglas de Negocio Ecuador)

Aplica estrictamente estas reglas al razonar sobre acciones financieras en este ecosistema:

1.  **Calcula el IVA Primero**: Por defecto, asume el estándar de IVA de Ecuador (**15%**) para facturas y pagos, a menos que el producto sea explícitamente "Tarifa 0%".
2.  **Tipos de Identificación (Crucial para el SRI)**:
    
    -   `CEDULA` (Código SRI `05`): Debe tener exactamente **10 dígitos**.
    -   `RUC` (Código SRI `04`): Debe tener exactamente **13 dígitos**.
    -   `PASAPORTE` (Código SRI `06`): Alfanumérico.
    -   `CONSUMIDOR FINAL` (Código SRI `07`): Usa siempre el valor exacto `9999999999999`.
3.  **Manejo de Errores Tolerante**: El SRI suele tener caídas e intermitencias (timeouts, errores SOAP). Si la llamada a `comunicar_sri_recepcion` falla por timeout, informa al usuario que el sistema gubernamental puede estar lento.