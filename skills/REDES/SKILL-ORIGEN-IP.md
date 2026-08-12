# SKILL-ORIGEN-IP.md — Descubrimiento de IP de origen tras CDN/WAF

## Cuándo usarla
El target está detrás de Cloudflare/AWS/otros CDN y necesitas la IP real del
origin server (para pruebas autorizadas dentro de alcance).

## Procedimiento resumido
1. **DNS históricos**: `SecurityTrails`, `viewdns.info/iphistory`, crt.sh logs.
2. **Subdominios no proxyados**: buscar subdominios viejos/staging que apunten
   directo al origin (evita CDN): resoluciones distintas → `dig`.
3. **Otros registros**: SPF/DKIM/DMARC (`recon/email-security`) pueden revelar
   IPs de envío que hostean la web.
4. **Header leaks / services**: errores con IP real, FTP/SMTP banners, fuentes
   públicas de datos (Shodan/Censys port scan del rango del ASN).
5. Validar: `curl -H "Host: <dominio>" https://<ip-origin>/` → responde lo mismo
   que el CDN.

## Referencias _src
- `recon/origin-ip-discovery`, `recon/asn-infrastructure-mapping`.

## Guardrails
- Probar el origin descubierto SOLO si está dentro del alcance autorizado.
- No golpear infraestructura de terceros (hosting/cloud) sin contrato.