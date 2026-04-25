import os

TEMPLATE = """# 🇪🇨 MCP {title}

Servidor Model Context Protocol (MCP) para la integración con **{integration_name}**.

Parte del ecosistema oficial de [MCP Hub Ecuador](https://github.com/mcphub-ec/hub).

> [!IMPORTANT]
> **🤖 Nota para Agentes IA:** Antes de interactuar con este servidor, por favor revisa el [Agent Cheatsheet](https://github.com/mcphub-ec/hub/blob/main/agent-cheatsheet.md) en nuestro Hub principal para comprender las reglas de negocio, cálculo de IVA (15%) y formatos de identificación de Ecuador.

## 🚀 Características

{features}
-   **Arquitectura Enterprise:** Imágenes Docker ultra-ligeras con _Healthchecks_ nativos, logs estructurados en JSON y validación continua de seguridad.

## 🛠️ Herramientas Disponibles

{tools}

## 📦 Instalación y Configuración

### 1\\. Variables de Entorno

Este servidor es completamente _stateless_. Copia el archivo `.env.example` a `.env` y configura tus datos. **Nunca hagas commit de este archivo.**

```env
{env_vars}
```

### 2\\. Despliegue con Docker (Recomendado)

Para entornos de producción o pruebas limpias, recomendamos usar nuestra imagen oficial alojada en GitHub Container Registry (`ghcr.io`).

**Vía Docker CLI:**

```bash
docker run -d \\
  --name {docker_name} \\
  --env-file .env \\
  ghcr.io/mcphub-ec/{docker_name}:latest
```

**Vía Docker Compose:**

```yaml
services:
  {docker_name}:
    image: ghcr.io/mcphub-ec/{docker_name}:latest
    container_name: {docker_name}
    env_file:
      - .env
    restart: unless-stopped
```

### 3\\. Uso con Claude Desktop (Local)

Si deseas conectarlo directamente a tu cliente de Claude para desarrollo local, añade la siguiente configuración a tu archivo `claude_desktop_config.json`:

```json
{{
  "mcpServers": {{
    "{docker_name}": {{
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/ruta/absoluta/a/tu/.env",
        "ghcr.io/mcphub-ec/{docker_name}:latest"
      ]
    }}
  }}
}}
```

_(Nota: También puedes correrlo directamente con `python -m server` si clonas el repositorio y manejas tu propio entorno virtual)._

## 🔒 Seguridad y Gobernanza

Este proyecto sigue estándares estrictos de seguridad:

-   **Stateless:** No almacena credenciales ni certificados en bases de datos.
-   **Escaneo de Vulnerabilidades:** Cada Pull Request es analizado automáticamente con `bandit` y `detect-secrets`.
-   **Responsible Disclosure:** Si encuentras una vulnerabilidad, por favor no abras un Issue público. Revisa nuestro [SECURITY.md](https://github.com/mcphub-ec/hub/blob/main/SECURITY.md) y contáctanos directamente a `security@mcphub.ec`.

## 🤝 Contribuir

Si deseas proponer mejoras, por favor revisa nuestra [Guía de Contribución](https://github.com/mcphub-ec/hub/blob/main/CONTRIBUTING.md) en el repositorio central. ¡Todos los Pull Requests que pasen los checks de CI/CD son bienvenidos!
"""

DATA = {
    "contabilidad/sri": {
        "title": "SRI Nativo",
        "integration_name": "el Servicio de Rentas Internas (SRI)",
        "docker_name": "mcp-sri",
        "features": "-   Generación automática de XML nativo según esquema oficial SRI (v2.1.0).\n-   Firma digital local XAdES-BES utilizando tu propio certificado `.p12`.\n-   Transmisión y autorización automática vía SOAP.",
        "tools": "-   `flujo_completo_factura`: Ejecuta todo el flujo de facturación electrónica en una sola llamada.\n-   `generar_factura_xml`: Genera el XML de la factura y calcula la clave de acceso.\n-   `firmar_xml`: Firma el XML generado utilizando el estándar XAdES-BES.\n-   `consultar_informacion_ruc`: Obtiene información pública de un contribuyente desde el SRI.",
        "env_vars": "EMITTER_RUC=\"0912345678001\"\nEMITTER_BUSINESS_NAME=\"Mi Empresa S.A.\"\nEMITTER_ADDRESS=\"Av. Principal 123\"\nCERTIFICATE_PATH=\"/ruta/absoluta/a/tu_firma.p12\"\nCERTIFICATE_PASSWORD=\"tu_password_de_firma\"\nSRI_ENVIRONMENT=\"TEST\""
    },
    "contabilidad/perseo": {
        "title": "Perseo",
        "integration_name": "el sistema ERP Perseo",
        "docker_name": "mcp-perseo",
        "features": "-   Integración directa con el ERP Perseo.\n-   Consulta y creación de transacciones contables.",
        "tools": "-   `consultar_datos_perseo`: Consulta de información del ERP.",
        "env_vars": "PERSEO_API_KEY=\"tu_api_key_aqui\"\nPERSEO_API_URL=\"https://api.perseo.ec\""
    },
    "contabilidad/contifico": {
        "title": "Contífico",
        "integration_name": "el sistema ERP Contífico",
        "docker_name": "mcp-contifico",
        "features": "-   Integración completa con el ERP Contífico.\n-   Manejo de personas, stock y documentos contables.\n-   Creación de cobros.",
        "tools": "-   `listar_personas`: Gestión de clientes (necesario antes de facturar).\n-   `obtener_stock`: Consulta de inventario en tiempo real.\n-   `crear_documento`: Generación de facturas de venta o proformas.\n-   `crear_cobro_documento`: Conciliación y registro de pagos recibidos.",
        "env_vars": "CONTIFICO_API_KEY=\"tu_api_key_aqui\""
    },
    "contabilidad/invoka": {
        "title": "Invoka",
        "integration_name": "Invoka",
        "docker_name": "mcp-invoka",
        "features": "-   Emisión electrónica simplificada basada en créditos.\n-   Delegación de firma electrónica.",
        "tools": "-   `emitir_factura`: Genera una factura consumiendo créditos de la plataforma.\n-   `emitir_nota_credito`: Emite una nota de crédito.",
        "env_vars": "INVOKA_API_KEY=\"tu_api_key_aqui\""
    },
    "contabilidad/factuplan": {
        "title": "Factuplan",
        "integration_name": "Factuplan",
        "docker_name": "mcp-factuplan",
        "features": "-   APIs especializadas para emisión de facturas electrónicas mediante el proveedor Factuplan.",
        "tools": "-   `emitir_factura`: Genera el comprobante usando la plataforma Factuplan.",
        "env_vars": "FACTUPLAN_API_KEY=\"tu_api_key_aqui\""
    },
    "contabilidad/facturasoft": {
        "title": "FacturaSoft",
        "integration_name": "FacturaSoft",
        "docker_name": "mcp-facturasoft",
        "features": "-   Conector para el sistema de emisión de comprobantes FacturaSoft.",
        "tools": "-   `emitir_factura`: Genera la factura en el ecosistema FacturaSoft.",
        "env_vars": "FACTURASOFT_API_KEY=\"tu_api_key_aqui\""
    },
    "pagos/payphone": {
        "title": "Payphone",
        "integration_name": "Payphone Ecuador",
        "docker_name": "mcp-payphone",
        "features": "-   Generación de links de pago web.\n-   Notificaciones push al celular del usuario (Payphone Sale).\n-   Reversos de transacciones automáticos.",
        "tools": "-   `create_payment_link`: Genera una URL web para que el usuario pague.\n-   `create_payphone_sale`: Envía una notificación Push directamente al celular del cliente.\n-   `get_transaction_status`: Verifica si el pago fue exitoso o rechazado.\n-   `reverse_transaction`: Cancela un pago y devuelve los fondos.",
        "env_vars": "PAYPHONE_TOKEN=\"tu_token_bearer_aqui\""
    },
    "pagos/kushki": {
        "title": "Kushki",
        "integration_name": "la pasarela Kushki",
        "docker_name": "mcp-kushki",
        "features": "-   Tokenización de tarjetas de crédito/débito.\n-   Creación de cargos recurrentes o únicos usando token.\n-   Transferencias bancarias.",
        "tools": "-   `tokenizar_tarjeta`: Crea un token seguro a partir de los datos de la tarjeta.\n-   `crear_cargo`: Realiza el cobro usando el token.\n-   `crear_transferencia`: Inicia un proceso de transferencia bancaria.",
        "env_vars": "KUSHKI_PRIVATE_MERCHANT_ID=\"tu_merchant_id\""
    },
    "pagos/datafast": {
        "title": "Datafast",
        "integration_name": "la red Datafast",
        "docker_name": "mcp-datafast",
        "features": "-   Procesamiento tradicional de tarjetas en Ecuador.\n-   Consulta de estados en la red Datafast.",
        "tools": "-   `checkout_id`: Genera un ID de checkout para iniciar el pago.\n-   `verificar_estado`: Verifica el estado de una transacción.",
        "env_vars": "DATAFAST_ENTITY_ID=\"tu_entity_id\"\nDATAFAST_BEARER_TOKEN=\"tu_token\""
    },
    "pagos/pagomedios": {
        "title": "PagoMedios",
        "integration_name": "PagoMedios (Abitmedia)",
        "docker_name": "mcp-pagomedios",
        "features": "-   Ecosistema Abitmedia para generar solicitudes de cobro.\n-   Tracking de pagos integrados.",
        "tools": "-   `generar_solicitud_cobro`: Crea un link de pago en PagoMedios.\n-   `verificar_pago`: Consulta el estado de una solicitud de cobro.",
        "env_vars": "PAGOMEDIOS_TOKEN=\"tu_token_aqui\""
    }
}

for path, data in DATA.items():
    file_path = f"/root/mcphub/{path}/README.md"
    content = TEMPLATE.format(**data)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Updated {file_path}")

