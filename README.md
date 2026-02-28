# MitM Lab (ARP & DNS) — Documentación técnica (entorno controlado)

## Aviso legal y ético
Este repositorio está orientado **exclusivamente** a fines educativos y defensivos, en **entornos controlados** y con **autorización explícita**. El uso no autorizado de técnicas de interceptación, suplantación o manipulación de tráfico es ilegal.

## Objetivo
Documentar un laboratorio para **comprender riesgos** asociados a suplantación ARP (L2) y manipulación de resolución DNS, y para **aplicar controles de prevención/detección**.

> Esta documentación no proporciona instrucciones operativas para realizar ataques en redes reales.

## Alcance
- Red de laboratorio aislada (PNetLab/EVE-NG/GNS3 u otro).
- Componentes típicos: host cliente, gateway/switch, resolvedor DNS, nodo de pruebas.
- Enfoque: observabilidad, evidencias y mitigación.

## Topología del laboratorio
### Componentes
- **Victim/Cliente**: genera consultas DNS.
- **Gateway**: puerta de enlace de la VLAN.
- **DNS Resolver**: servidor DNS permitido.
- **Nodo de pruebas**: host de validación dentro del lab.

### VLANs, interfaces y direccionamiento (completar)
| Nodo | Interfaz | VLAN | IP/Mask | Rol |
|------|----------|------|---------|-----|
| Cliente | (completar) | (completar) | (completar) | Cliente |
| Gateway | (completar) | (completar) | (completar) | Gateway |
| DNS Resolver | (completar) | (completar) | (completar) | DNS |
| Nodo de pruebas | (completar) | (completar) | (completar) | Validación |

## Parámetros del escenario (completar)
- NIC de observación/captura: `(completar)`
- Dominio(s) de prueba: `(completar)`
- IP(s) de prueba/redirección: `(completar)`

## Requisitos
### Requisitos de red
- VLAN aislada sin conectividad a redes productivas.
- (Opcional) SPAN/port-mirroring para observación.

### Requisitos de monitoreo
- Wireshark o tcpdump.
- Logs del switch (si aplica): DAI/DHCP Snooping.
- Logs del resolver DNS.

## Evidencias (capturas de pantalla)
Guardar evidencias en: `docs/screenshots/`

Capturas sugeridas:
1. Tabla ARP antes/después.
2. Tráfico DNS (consulta y respuesta) en Wireshark.
3. Logs/alertas de controles (DAI/DHCP Snooping/IDS).
4. Pruebas de resolución (dig/nslookup) validando mitigación.

## Indicadores y detección
### ARP
- Cambios frecuentes en la entrada ARP del gateway.
- Respuestas ARP no solicitadas repetitivas.

### DNS
- Respuestas con IP inesperada para dominios conocidos.
- TTLs inconsistentes/anómalos.

## Medidas de mitigación
### Capa 2
- Dynamic ARP Inspection (DAI).
- DHCP Snooping y tabla de bindings.
- Port Security (límite/sticky MAC).
- Segmentación y reducción de broadcast.

### DNS
- Restringir UDP/53 a resolvers autorizados.
- Validación DNSSEC en el resolver.
- Monitoreo y alertas en el resolver (IPs/TTLs anómalos).

### Respuesta
- Aislar puerto sospechoso.
- Limpiar cachés/entradas ARP cuando aplique.
- Recolectar PCAP y logs.

## Estructura del repositorio (propuesta)
```
README.md
/docs
  /screenshots
/tools
  (script_python_pendiente.py)
```

## Script Python (pendiente)
Se reservará un archivo para el script en:
- `tools/mitm_lab_tool.py` (pendiente de añadir)

> Nota: El repositorio debe mantener el enfoque educativo/defensivo y no incluir guías operativas para uso indebido.

## Licencia
(completar)