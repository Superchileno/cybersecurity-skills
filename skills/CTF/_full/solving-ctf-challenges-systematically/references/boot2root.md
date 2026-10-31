# Boot2Root en CTF — despliegue, red y escalada

Notas de los boot2root resueltos: «Señal Fantasma» (XimaTV/CentinelaOTA), «Fresia»
(Kimün) y «Apocalipsis — Archivo Communio».

## 1. Desplegar la VM cuando el hipervisor "no está"

| Problema | Solución aplicada |
|---|---|
| No hay VirtualBox | `tar -xf reto.ova` → disco VMDK + `.ovf`; crear `.vmx` a mano |
| `streamOptimized` no arranca | `vmware-vdiskmanager -t 0 disco.vmdk` (monolítico) |
| `virtualHW.version 19` no soportado | Bajar a `18` en el `.vmx` |
| Sin hipervisor en absoluto | `qemu-img convert` a raw + `losetup -P` + montaje read-only |

Montaje offline read-only (forense sin arrancar la VM):

```bash
qemu-img convert -O raw disco.vmdk disco.raw
losetup -Pf --show disco.raw
mount -o ro /dev/loop0p1 /mnt/vm
```

## 2. Red: la causa más común de "no responde"

El OVA declara la NIC con el nombre del hipervisor de origen (`enp0s3` en
VirtualBox). Al cambiar de hipervisor el nombre cambia (`ens33`) y **netplan no
aplica**, por lo que la VM queda sin IP.

```yaml
# /etc/netplan/99-ctf-any.yaml  (dentro de la VM, vía montaje)
network:
  version: 2
  ethernets:
    all-en:
      match: { name: "en*" }
      dhcp4: true
```

Reempaquetar y arrancar. Conservar el disco original (`*-disk1.vmdk.orig`).

## 3. Alcanzar la VM desde WSL2

WSL2 en modo NAT no ve las redes del hipervisor (VMnet8/Host-Only). Opciones:

- **Relay TCP en espacio de usuario** (no requiere admin):
  `solucion/relay_tcp.py` escucha en `127.0.0.1:8080` y reenvía a la IP de la VM.
- **Pivote SOCKS5**: un proceso en el host expone `127.0.0.1:1080`; desde WSL se usa
  `proxychains4` para nmap/curl.
- `netsh interface portproxy` funciona pero **exige administrador**.

## 4. Escalada típica en boot2root de CTF

| Vector | Ejemplo real | Señal |
|---|---|---|
| Backup público con hash | `/old/backup_2019.sql` con bcrypt → crackeo → admin | `robots.txt`, `/backup`, `/old` |
| Script de backup con clave en claro | `mysqldump -u root -p'Clave'` en `backup_db.sh` | buscar `-p'` en home |
| `sudo NOPASSWD` sobre script escribible | `(root) NOPASSWD: /opt/.../respaldo.sh` con 777 | `sudo -l` + `ls -l` |
| `sudo eval` sobre variable controlada | `eval "sha256sum .../$PKG"` → `x;cat /root/root.txt` | leer el script, no solo listarlo |
| `.git` expuesto con backdoor | commit que añade `_arve_uc_init` a un plugin | `git log -p` en el webroot |
| Credenciales reutilizadas | `conf.php` con la misma clave del panel | comparar configs |
| Upload sin validación de extensión | `ota.php` guarda `.php` en `/ota/` | probar multipart |

## 5. Cuentas y flags

- `user.txt` suele requerir RCE web de baja privilegio; `root.txt` requiere escalada.
- Si la flag no está en `/root/root.txt`, buscar en `/home/<user>/`, `/tmp`,
  `/var/backups` y variables de entorno del servicio.
- Validar la flag **en la plataforma**, no solo por formato.

## 6. Autorización

Los boot2root de CTF se ejecutan sobre instancias provistas por el evento. Nunca
contra infraestructura de terceros ni IPs fuera del rango del reto.
