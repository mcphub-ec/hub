# MCP Email IMAP/SMTP

Servidor Model Context Protocol (MCP) para que agentes IA consulten correos por IMAP y envien correos por SMTP sin conocer credenciales.

## Caracteristicas

- Multiples cuentas nombradas mediante variables de entorno.
- Lectura IMAP: listar carpetas, buscar correos, leer mensajes y descargar adjuntos bajo limite.
- Envio SMTP en dos pasos: `prepare_email` genera un `send_token`; `send_prepared_email` envia solo si recibe el mismo contenido y token valido.
- Credenciales nunca se aceptan como parametros de herramientas MCP.
- Logs JSON sin passwords, tokens, cuerpos completos ni adjuntos.

## Herramientas Disponibles

- `list_accounts`: lista cuentas disponibles y capacidades sin secretos.
- `list_mailboxes`: lista carpetas IMAP de una cuenta.
- `search_emails`: busca mensajes con filtros y limite seguro.
- `get_email`: obtiene asunto, remitentes, destinatarios, fecha, cuerpo limitado y metadatos de adjuntos.
- `get_attachment`: devuelve un adjunto en Base64 si no supera `MAX_ATTACHMENT_BYTES`.
- `prepare_email`: prepara un mensaje y devuelve `send_token`; no envia.
- `send_prepared_email`: envia por SMTP si el payload coincide exactamente con el token.

## Configuracion

Este servidor es stateless. Copia `.env.example` a `.env` y completa los valores reales. Nunca hagas commit de `.env`.

```env
EMAIL_ACCOUNTS=personal,trabajo
EMAIL_PERSONAL_IMAP_HOST=imap.example.com
EMAIL_PERSONAL_IMAP_PORT=993
EMAIL_PERSONAL_IMAP_USER=user@example.com
EMAIL_PERSONAL_IMAP_PASSWORD=...
EMAIL_PERSONAL_SMTP_HOST=smtp.example.com
EMAIL_PERSONAL_SMTP_PORT=587
EMAIL_PERSONAL_SMTP_USER=user@example.com
EMAIL_PERSONAL_SMTP_PASSWORD=...
EMAIL_PERSONAL_FROM=user@example.com
EMAIL_PERSONAL_TLS_MODE=starttls
MCP_MASTER_KEY=...
```

Genera `MCP_MASTER_KEY` con:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Docker

```bash
docker build -t mcp-email .
docker run --rm -i --env-file .env mcp-email
```

## Claude Desktop

```json
{
  "mcpServers": {
    "mcp-email": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/ruta/absoluta/a/comunicaciones/email/.env",
        "mcp-email"
      ]
    }
  }
}
```

## Seguridad

- Usa contrasenas de aplicacion cuando el proveedor lo permita.
- Restringe el `.env` con `chmod 600 .env`.
- El agente puede ver contenido de correo y adjuntos solicitados, pero nunca credenciales IMAP/SMTP.
