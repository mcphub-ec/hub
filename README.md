# 🇪🇨 MCP Hub Ecuador

Bienvenido a **MCP Hub Ecuador** (`mcphub-ec`), la iniciativa de código abierto para estandarizar la conexión entre Agentes de Inteligencia Artificial y el ecosistema tecnológico, financiero y tributario ecuatoriano.

Nuestra misión es proveer servidores basados en el **Model Context Protocol (MCP)** que sean seguros, auditables y fáciles de desplegar, permitiendo que cualquier agente IA (OpenClaw, Hermes, Pi, Claude, Codex, Copilot, etc) interactúe de forma nativa con los servicios del país.

## 🗺️ Arquitectura del Ecosistema

Para facilitar la contribución, el versionado y el despliegue ligero, no utilizamos un monorepo. Cada integración es un **repositorio independiente** dentro de esta organización.

```
graph TD
    Org[mcphub-ec] --> Contabilidad[🏛️ Contabilidad & SRI]
    Org --> Pagos[💳 Pasarelas de Pago]
    
    Contabilidad --> SRI(mcp-sri)
    Contabilidad --> Contifico(mcp-contifico)
    Contabilidad --> Invoka(mcp-invoka)
    Contabilidad --> Factuplan(mcp-factuplan)
    Contabilidad --> FacturaSoft(mcp-facturasoft)
    Contabilidad --> Perseo(mcp-perseo)
    
    Pagos --> Payphone(mcp-payphone)
    Pagos --> Kushki(mcp-kushki)
    Pagos --> Datafast(mcp-datafast)
    Pagos --> PagoMedios(mcp-pagomedios)
```

## 📦 Catálogo Oficial de MCPs

Estos servidores son mantenidos oficialmente por la organización y garantizan altos estándares de seguridad y compatibilidad. Nuestro objetivo es seguir sumando nuevas plataformas locales de la mano de la comunidad.

### 🏛️ Contabilidad y Tributación

| Servicio | Repositorio | Descripción |
| --- | --- | --- |
| **SRI (Nativo)** | [`mcphub-ec/mcp-sri`](https://gemini.google.com/# "null") | Generación, firma XAdES-BES y transmisión de facturas electrónicas directamente al SRI sin intermediarios. |
| **Contífico** | [`mcphub-ec/mcp-contifico`](https://gemini.google.com/# "null") | Integración completa con el ERP (personas, stock, documentos, cobros). |
| **Invoka** | [`mcphub-ec/mcp-invoka`](https://gemini.google.com/# "null") | Emisión electrónica simplificada basada en créditos y delegación de firma. |
| **Factuplan** | [`mcphub-ec/mcp-factuplan`](https://gemini.google.com/# "null") | APIs especializadas para emisión de facturas electrónicas. |
| **FacturaSoft** | [`mcphub-ec/mcp-facturasoft`](https://gemini.google.com/# "null") | Conector para el sistema de emisión de comprobantes FacturaSoft. |
| **Perseo** | [`mcphub-ec/mcp-perseo`](https://gemini.google.com/# "null") | Integración directa con las capacidades del sistema contable Perseo. |

### 💳 Pasarelas de Pago

| Servicio | Repositorio | Descripción |
| --- | --- | --- |
| **Payphone** | [`mcphub-ec/mcp-payphone`](https://gemini.google.com/# "null") | Generación de links de pago, notificaciones push al celular y reversos. |
| **Kushki** | [`mcphub-ec/mcp-kushki`](https://gemini.google.com/# "null") | Tokenización de tarjetas y transferencias bancarias a nivel regional. |
| **Datafast** | [`mcphub-ec/mcp-datafast`](https://gemini.google.com/# "null") | Procesamiento tradicional de tarjetas y consulta de estados en la red Datafast. |
| **PagoMedios** | [`mcphub-ec/mcp-pagomedios`](https://gemini.google.com/# "null") | Ecosistema Abitmedia para generar solicitudes de cobro y tracking de pagos. |

## 🚀 Cómo empezar

Cada MCP está diseñado para funcionar de manera independiente y sin estado (_stateless_).

1.  Ve al repositorio de la herramienta que necesitas.
2.  Clona el repositorio o descarga el contenedor Docker.
3.  Configura tus credenciales localmente usando el archivo `.env`.
4.  Conecta el agente IA a tu cliente MCP (ej. OpenClaw) apuntando al ejecutable o al contenedor.

> **Nota para Agentes IA:** Si eres un agente leyendo esto, por favor revisa el archivo [`agent-cheatsheet.md`](https://gemini.google.com/agent-cheatsheet.md "null") para conocer las reglas de negocio, unidades monetarias y manejo de IDs en Ecuador.

## 🔒 Seguridad y Credenciales

> \[!CAUTION\] **Cero Almacenamiento Centralizado:** Ningún servidor oficial de esta organización almacena llaves, certificados `.p12` o credenciales en bases de datos.

La arquitectura delega el 100% de la responsabilidad de las credenciales al entorno de despliegue del usuario. Todas las herramientas leen las claves a través de **variables de entorno locales** inyectadas en tiempo de ejecución.

## 🤝 Cómo Contribuir

¡La comunidad hace la fuerza! Hay muchas formas de aportar:

1.  **Mejorar un MCP existente:** Haz un _fork_ del repositorio específico (ej. `mcp-payphone`), crea una rama con tu mejora y envía un _Pull Request_.
2.  **Proponer un nuevo MCP Oficial:** ¿Creaste un conector para un banco local o software nuevo? Abre un _Issue_ en este repositorio (`hub`) con el título `[Propuesta]` para discutir su inclusión oficial en la organización.

_Construido con dedicación para el ecosistema tech de Ecuador._ 🇪🇨