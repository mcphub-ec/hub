# Changelog

Todos los cambios notables a este proyecto se documentan aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Security (Auditoría 2026-06-16)
- **Added**: `mcp_common/` shared library in 4 payment servers (payphone, kushki, datafast, pagomedios)
  - `mcp_common.security.validate_safe_url`: anti-SSRF helper (blocks private IPs, loopback, metadata endpoints, non-HTTPS)
  - `mcp_common.security.validate_amount`: enforces per-transaction max (default 10,000 USD, env: `MCP_MAX_AMOUNT_USD`)
  - `mcp_common.logging_filter.SensitiveDataFilter`: redacts tokens, RUCs, cédulas, cards from logs
- **payphone**: add `token` parameter to all tools (multi-account support), max amount cap, SSRF check on `responseUrl`/`notifyUrl`, `reverse_transaction` pre-checks `Approved` state
- **kushki**: `KUSHKI_ENVIRONMENT` default changed from `sandbox` to `production` (fail-closed); validate `periodicity` whitelist
- **datafast**: `pago_recurrente_oneclick` validates `shopper_result_url` against SSRF; `reversar_reembolsar_pago` validates amount
- **pagomedios**: `crear_link_pago` validates `notify_url` against SSRF; `reversar_cobro` pre-checks same-day window using Ecuador timezone (UTC-5)
- **email**: HMAC action tokens now include `expires_at` (TTL default 300s, env: `EMAIL_ACTION_TOKEN_TTL`); IMAP/SMTP explicit timeouts (env: `EMAIL_NETWORK_TIMEOUT`); HTML sanitization via `nh3` (Rust-backed) with regex fallback; `_send_message` accepts `bcc_recipients` separately and logs only counts; `email_save_draft` extracts UID via RFC 4315 APPENDUID with Message-ID and last-UID fallbacks; outbound recipient validation via `email-validator`
- **SRI signing-service (Java)**: requires `X-Signing-Key` header on `/sign` and `/certificate/info`; CORS restricted via `SIGNING_ALLOWED_ORIGINS` env (default empty = strictest); signing-service only exposed on internal Docker network, NOT to host; `docker-compose.yml` healthcheck uses correct `/api/v1/signature/health` path; `sri/docker.yml` standardized to use `secrets.GITHUB_TOKEN` (matches other 10 repos)
- **All 11 servers**: `host="0.0.0.0"` replaced with `host=os.getenv("MCP_HOST", "0.0.0.0")`; B104 removed from `.bandit` skips; Dockerfile HEALTHCHECK reads `MCP_PORT` env (default 8000)
- **SRI**: dead `import logger` block removed from contifico, invoka, factuplan, facturasoft; `certs/` and `*.p12` added to `.gitignore`; cert permissions set to 600
- **email**: `contacts.json` and `contacts*.json` added to `.gitignore` (PII protection)
- **hub root**: `.beads/` and `git_sync_log.txt` removed from git tracking; `commit_all.sh` and `commit_and_push_fixes.sh` neutralized (now exit with deprecation notice)

### Documentation
- Added `agent-docs.md` to all 11 sub-repos (sri, invoka, factuplan, facturasoft, datafast, pagomedios were missing)
- Added `SECRET_ROTATION.md` (in hub root) with step-by-step procedure for rotating credentials
- Updated `email/README.md` to document new contact tools and security features
- Updated `README.md` hub root: replaced broken `gemini.google.com/agent-cheatsheet.md` link with relative `./agent-cheatsheet.md`; added Comunicaciones category to architecture diagram
- `CLAUDE.md` reduced to a one-liner pointing to `AGENTS.md` (was duplicating beads integration)

### Infrastructure
- `mcp_common/` library created at hub root (template for shared code)
- `.pre-commit-config.yaml`: detect-secrets hook commented out (was broken due to missing baseline); document how to re-enable
- `.github/ISSUE_TEMPLATE/bug_report.md`: fixed malformed YAML frontmatter

## [Pre-audit] - 2026-04-25 to 2026-05-28

Initial development of all 11 MCP servers. See git history for individual commits.
