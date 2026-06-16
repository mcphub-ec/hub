# Seguridad: Rotación de Credenciales

> [!CAUTION]
> **ACCIÓN REQUERIDA DEL USUARIO** — Este issue se cierra como **deferred**
> porque la rotación de credenciales es una acción manual que el operador
> del repositorio debe ejecutar. No puede automatizarse desde un script.

## Inventario de Secretos Detectados (auditoría 2026-06-16)

Los siguientes archivos `.env` contienen secretos reales en **disco** (NO en
git, gracias al `.gitignore` correcto, pero **sin cifrar en reposo**):

| Archivo | Secretos | Acción |
|---|---|---|
| `contabilidad/sri/.env` | `CERTIFICATE_PASSWORD` | **Rotar la contraseña del `.p12`** en el banco emisor del certificado. |
| `contabilidad/sri/certs/firma.p12` | Llave privada RSA | **Revocar el certificado** y emitir uno nuevo. |
| `contabilidad/contifico/.env` | `CONTIFICO_API_KEY`, `CONTIFICO_POS_TOKEN` | Rotar ambos tokens en el portal de Contífico. |
| `contabilidad/invoka/.env` | `INVOKA_API_KEY` | Rotar en el panel de Invoka. |
| `contabilidad/factuplan/.env` | `FACTUPLAN_API_KEY` | Rotar en el panel de Factuplan. |
| `contabilidad/facturasoft/.env` | `FACTURASOFT_BEARER_TOKEN` | Rotar en Abitmedia. |
| `contabilidad/perseo/.env` | (vacío) | OK. |
| `pagos/payphone/.env` | `PAYPHONE_TOKEN` (280+ chars) | Rotar en panel Payphone. |
| `pagos/kushki/.env` | placeholders | OK. |
| `pagos/datafast/.env` | `DATAFAST_BEARER_TOKEN` | Rotar con ACI/Datafast. |
| `pagos/pagomedios/.env` | `PAGOMEDIOS_BEARER_TOKEN` | Rotar en Abitmedia. |
| `comunicaciones/email/.env` | 6 cuentas IMAP/SMTP (~12 secrets) | Cambiar contraseñas de los 6 buzones; revocar app passwords de Gmail/Outlook. |

## Procedimiento Recomendado

### 1. Generar nuevos secretos
- **Certificado SRI**: Solicitar revocación + emisión en el banco autorizador.
  Típicamente toma 24-48h hábiles.
- **API tokens**: Cada proveedor tiene un panel admin → API → Regenerar.
- **Email**: Gmail/Outlook tienen "App passwords" (2FA). Revocar y re-generar.
- **MCP_MASTER_KEY** (Fernet): ejecutar `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`.

### 2. Distribuir sin commitear
- **NO escribir los nuevos secretos en `.env` local y commitearlo**.
- Usar una de estas opciones:
  - **Docker secrets** (`docker secret create mcp_payphone_token ...`)
  - **HashiCorp Vault** (consultar `vault kv put secret/mcp/payphone token=...`)
  - **AWS SSM Parameter Store** (`aws ssm put-parameter --name /mcp/payphone/token --value '...' --type SecureString`)
  - **Bitwarden CLI** + `bw get password <id>` en el entrypoint
- Si `.env` es la única opción, asegúrate de que `.env` está en `.gitignore` (✅ ya está)
  y de aplicar `chmod 600 .env` después de escribir.

### 3. Verificar que los nuevos secretos funcionan
- Para cada servicio, ejecutar el smoke test correspondiente.
- Confirmar que el `git log` NUNCA tuvo un `.env` con secretos:
  ```bash
  git log --all --full-history --diff-filter=A --name-only | grep -E '\.env$|\.p12$'
  ```
  (Resultado esperado: solo `.env.example` y templates).

### 4. Documentar la rotación
- Anotar en el calendario: rotar cada 90 días como buena práctica.
- Considerar automatizar con `cron` + script que notifique al equipo.

## Estado de Implementación
- [x] `.gitignore` correcto en los 11 sub-repos (verificado)
- [x] `chmod 600` en `.env` (recomendado en `.env.example`)
- [x] **Filtro de logging** que redacta tokens, RUCs, cédulas (vía `mcp_common/logging_filter.py`)
- [ ] **Secret manager en producción** — pendiente de decisión de arquitectura
- [ ] **Rotación programada** — pendiente de implementación

## Referencias
- bd issue original: `mcphub-hm5` (P0)
- bd issue relacionado: `mcphub-i78` (P1)
- Auditoría completa: `AUDIT-2026-06-16.md` (en el hub repo)
