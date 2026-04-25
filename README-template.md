# 🇪🇨 MCP \[Nombre del Servicio\] (ej. SRI Nativo)

Servidor Model Context Protocol (MCP) para la integración con **\[Nombre de la empresa/servicio\]**.

Parte del ecosistema oficial de [MCP Hub Ecuador](https://github.com/mcphub-ec/hub "null").

> \[!IMPORTANT\] **🤖 Nota para Agentes IA:** Antes de interactuar con este servidor, por favor revisa el [Agent Cheatsheet](https://github.com/mcphub-ec/hub/blob/main/agent-cheatsheet.md "null") en nuestro Hub principal para comprender las reglas de negocio, cálculo de IVA (15%) y formatos de identificación de Ecuador.

## 🚀 Características

-   \[Característica 1 - ej. Generación automática de XML v2.1.0\]
-   \[Característica 2 - ej. Firma electrónica local XAdES-BES\]
-   \[Característica 3 - ej. Consulta pública de RUC\]
-   **Arquitectura Enterprise:** Imágenes Docker ultra-ligeras con _Healthchecks_ nativos, logs estructurados en JSON y validación continua de seguridad.

## 🛠️ Herramientas Disponibles

-   `[tool_name_1]`: Descripción clara de lo que hace la herramienta y cuándo el agente debe usarla.
-   `[tool_name_2]`: Descripción.
-   `[tool_name_3]`: Descripción.

## 📦 Instalación y Configuración

### 1\. Variables de Entorno

Este servidor es completamente _stateless_. Copia el archivo `.env.example` a `.env` y configura tus datos. **Nunca hagas commit de este archivo.**

```
[VARIABLE_1]=tu_valor
[VARIABLE_2]=tu_valor
```

### 2\. Despliegue con Docker (Recomendado)

Para entornos de producción o pruebas limpias, recomendamos usar nuestra imagen oficial alojada en GitHub Container Registry (`ghcr.io`).

**Vía Docker CLI:**

```
docker run -d \
  --name mcp-[nombre] \
  --env-file .env \
  ghcr.io/mcphub-ec/mcp-[nombre]:latest
```

**Vía Docker Compose:**

```
services:
  mcp-[nombre]:
    image: ghcr.io/mcphub-ec/mcp-[nombre]:latest
    container_name: mcp-[nombre]
    env_file:
      - .env
    restart: unless-stopped
```

### 3\. Uso con Claude Desktop (Local)

Si deseas conectarlo directamente a tu cliente de Claude para desarrollo local, añade la siguiente configuración a tu archivo `claude_desktop_config.json`:

```
{
  "mcpServers": {
    "mcp-[nombre]": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/ruta/absoluta/a/tu/.env",
        "ghcr.io/mcphub-ec/mcp-[nombre]:latest"
      ]
    }
  }
}
```

_(Nota: También puedes correrlo directamente con `python -m [modulo]` si clonas el repositorio y manejas tu propio entorno virtual)._

## 🔒 Seguridad y Gobernanza

Este proyecto sigue estándares estrictos de seguridad:

-   **Stateless:** No almacena credenciales ni certificados en bases de datos.
-   **Escaneo de Vulnerabilidades:** Cada Pull Request es analizado automáticamente con `bandit` y `detect-secrets`.
-   **Responsible Disclosure:** Si encuentras una vulnerabilidad, por favor no abras un Issue público. Revisa nuestro [SECURITY.md](https://github.com/mcphub-ec/hub/blob/main/SECURITY.md "null") y contáctanos directamente a `security@mcphub.ec`.

## 🤝 Contribuir

Si deseas proponer mejoras, por favor revisa nuestra [Guía de Contribución](https://github.com/mcphub-ec/hub/blob/main/CONTRIBUTING.md "null") en el repositorio central. ¡Todos los Pull Requests que pasen los checks de CI/CD son bienvenidos!