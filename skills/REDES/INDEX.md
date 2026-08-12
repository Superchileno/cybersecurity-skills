# REDES — Subskills de redes e infraestructura

Área: descubrimiento de hosts/red, escaneo de puertos, servicios, técnicas de
fingerprint y evasión. Fuente completa: `skills/_src/recon-skills/recon/*`,
`skills/_src/recon-skills/infra/*`, `skills/_src/mukul-anthropic/*`.

## Subskills destiladas

| Subskill | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-SUBDOMINIOS.md` | Enumeración pasiva/activa de subdominios | `recon/subdomain-enumeration`, `recon/subdomain-takeover-hunt` |
| `SKILL-PUERTOS.md` | Escaneo de puertos/servicios a escala y clasificación | `recon/port-mass-scan`, `recon/port-service-discovery` |
| `SKILL-VHOST.md` | Enumeración de virtual hosts | `recon/vhost-enumeration` |
| `SKILL-FINGERPRINT.md` | TLS fingerprint, HTTP/2 impersonation, camuflaje | `recon/tls-fingerprint-impersonation`, `recon/http2-header-impersonation` |
| `SKILL-ORIGEN-IP.md` | Descubrir IP real tras CDN/WAF (origin ip) | `recon/origin-ip-discovery` |
| `SKILL-CT-LOGS.md` | Analizar Certificate Transparency logs (subdominios pasivos, phishing) | `mukul-anthropic/analyzing-tls-certificate-transparency-logs` |
| `SKILL-BGP-HIJACK.md` | Evaluar hijacking BGP y mitigación RPKI | `mukul-anthropic/exploiting-bgp-hijacking-vulnerabilities`, `implementing-bgp-security-with-rpki` |
| `SKILL-SSL-TLS.md` | Auditar configuración TLS (testssl, cifrados, certs) | `mukul-anthropic/performing-ssl-tls-security-assessment` |
| `SKILL-SHODAN.md` | Reputación/enriquecimiento de IP con Shodan | `mukul-anthropic/performing-ip-reputation-analysis-with-shodan` |

## Enrutado al _src (para detalle)

- ASN/mapas de infra: `recon/asn-infrastructure-mapping`, `meta/sector-recon-methodology`
- Email security/SPF/DMARC: `recon/email-security`
- Cache poisoning: `recon/cache-attack`
- IoT/SCADA/Hikvision: `recon/iot-camera-recon`, `recon/scada-hikvision-isapi`

## Recuerda (guardrails)

- Escaneo activo solo dentro de alcance autorizado (AGENTS.md).
- Respetar límite de velocidad (200ms/request por host por defecto).
- No escanear terceros sin contrato.