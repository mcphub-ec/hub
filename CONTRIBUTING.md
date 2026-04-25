🤝 Guía de Contribución para MCP Hub Ecuador

¡Gracias por tu interés en contribuir a MCP Hub Ecuador! Tu ayuda es fundamental para construir el estándar de interoperabilidad de Agentes IA en el país.

Esta guía explica cómo puedes participar, ya sea reportando errores, sugiriendo mejoras o enviando código para nuevos servidores MCP.

🏗️ Reglas de Arquitectura (Obligatorias)

Para mantener la seguridad y fiabilidad del ecosistema, todos los MCPs oficiales deben cumplir con estas reglas:

Diseño Stateless (Sin Estado): Los servidores no deben usar bases de datos locales ni remotas (PostgreSQL, SQLite, MongoDB) para almacenar información de los usuarios.

Manejo de Credenciales: Toda llave API, token o ruta a un certificado (.p12) debe ser inyectada exclusivamente a través de variables de entorno locales (ej. leyendo un archivo .env).

Cálculos Locales: Siempre que sea posible, el servidor debe hacer validaciones previas (ej. verificar que la cédula tenga 10 dígitos) antes de gastar cuota de red consultando APIs externas.

Independencia: Cada MCP debe ser un proyecto autónomo. No dependas de librerías cruzadas entre repositorios.

🐛 Reportar un Bug o Solicitar una Característica

Utiliza la pestaña de Issues en el repositorio correspondiente.
Si el problema es general o quieres solicitar un MCP nuevo, abre el Issue en el repositorio principal (hub). Por favor, utiliza las plantillas proporcionadas.

💻 Proceso de Pull Requests (PR)

Si deseas arreglar un error o mejorar el código:

Haz un Fork del repositorio que deseas modificar (ej. mcp-payphone).

Crea una rama para tu característica: git checkout -b feature/nueva-herramienta o git checkout -b fix/error-timeout.

Haz tus cambios y asegúrate de documentar las nuevas funciones en el código.

Haz Commit de tus cambios: git commit -m 'feat: añade soporte para reversos en payphone'.

Haz Push a la rama en tu fork: git push origin feature/nueva-herramienta.

Abre un Pull Request hacia la rama main del repositorio oficial.

🚀 Proponer un MCP Completamente Nuevo

Si has creado un servidor MCP para una plataforma ecuatoriana que aún no está en nuestro catálogo (ej. Banco Pichincha, un software médico, etc.):

Ve a la pestaña Issues de este repositorio (hub).

Haz clic en "New Issue" y selecciona la plantilla "Proponer Nuevo MCP".

Discutiremos la viabilidad de la API y, si es aprobada, crearemos un repositorio oficial bajo mcphub-ec para que subas tu código, ¡y te daremos los créditos correspondientes!