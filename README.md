# MitM Lab: ARP & DNS Spoofing — Documentación Técnica

## 1. Aviso legal y ética profesional
Este documento describe un laboratorio controlado con fines educativos y defensivos. La información incluida está destinada únicamente para:

- Evaluación de vulnerabilidades en entornos controlados.
- Análisis de mitigaciones y prácticas de seguridad.
- Formación en detección de ataques de suplantación ARP y DNS.

**Importante:** El uso de técnicas de interceptación o manipulación de tráfico en entornos no autorizados es ilegal y queda fuera del alcance de este documento.

## 2. Objetivo del laboratorio
El laboratorio tiene como finalidad:

- Comprender los riesgos asociados con suplantación ARP (ARP spoofing/poisoning) en redes de capa 2.
- Analizar el impacto de la manipulación de resolución DNS (DNS spoofing/hijacking).
- Implementar controles para prevenir, detectar y mitigar estos ataques.

**Nota:** Este documento se enfoca en aspectos defensivos y de análisis; no incluye procedimientos ofensivos.

## 3. Alcance
- **Entorno:** Laboratorio virtual con hosts aislados (PNetLab, EVE-NG, GNS3).
- **Capas afectadas:** L2 (ARP), L3/L4 (UDP/53), y aplicación (DNS).
- **Resultados esperados:** Identificación de indicadores de compromiso (IoC) y validación de mitigaciones.

## 4. Topología del laboratorio

### 4.1 Componentes
- **Host víctima (Target/Cliente):** Genera consultas DNS.
- **Gateway:** Router de salida de VLAN.
- **Servidor DNS:** Resolvedor interno o externo, según diseño.
- **Host de pruebas (nodo de validación):** Nodo de laboratorio para simular comportamiento malicioso y validar controles.

### 4.2 Interfaces, VLANs y direccionamiento
| Nodo | Interfaz | VLAN | IP | Rol |
|------|----------|------|----|-----|
| Victim (Target) | eth1 | 10 | 12.0.10.20/24 | Cliente |
| Gateway | ethX | 10 | 12.0.10.1/24 | Gateway |
| Nodo de pruebas | ethZ | 10 | 12.0.10.10/24 | Nodo de validación |

> Sustituir los valores según el entorno de laboratorio real.

## 5. Parámetros del escenario
- **NIC de captura/monitoreo:** Interfaz conectada a la VLAN del cliente.
- **IP de redirección de prueba:** 12.0.10.10/24.
- **DNS Resolver:** **N/A** si no existe, o indicar IP del resolver interno.

## 6. Requisitos del laboratorio

### 6.1 Requisitos de red
- VLAN aislada, sin conexión a redes productivas.
- Disponibilidad de SPAN o port-mirroring para observación de tráfico.
- DNS controlado mediante resolvedor interno o sinkhole de laboratorio.

### 6.2 Requisitos de monitoreo
- **Captura de tráfico:** Wireshark o tcpdump.
- **Logs relevantes:**
  - Switch: DAI, DHCP snooping, port security.
  - Firewall/Router: conntrack, DNS logs.
  - DNS resolver: consultas/respuestas, TTLs, respuestas NXDOMAIN.

## 7. Evidencias requeridas
Se deben incluir capturas de pantalla con datos redactados:

- Tabla ARP antes y después (host víctima y gateway).
- Tráfico DNS (consulta y respuesta) en Wireshark.
- Alertas y logs de mitigación (DAI/DHCP snooping) o IDS (Suricata/Snort).
- Validación de resolución DNS (dig/nslookup) mostrando comportamiento correcto tras mitigación.

Estructura de archivos sugerida:

- `docs/screenshots/01_arp_table_before.png`
- `docs/screenshots/02_arp_table_after.png`
- `docs/screenshots/03_dns_query_response.png`
- `docs/screenshots/04_mitigation_logs.png`

## 8. Indicadores de compromiso (IoC)

### 8.1 ARP Spoofing
- Cambios frecuentes en entradas ARP (IP del gateway con MAC distinta).
- Paquetes ARP “gratuitos” repetitivos.
- Incremento de ARP replies sin solicitudes previas.

### 8.2 DNS Spoofing/Hijacking
- TTLs inusuales o inconsistentes.
- Direcciones IP inesperadas para dominios conocidos.
- Respuestas “authoritative” anómalas.
- Divergencia entre resolver esperado y respuestas observadas.

## 9. Medidas de mitigación recomendadas

### 9.1 Capa 2 (ARP)
- Dynamic ARP Inspection (DAI) en switches gestionables.
- DHCP Snooping con tabla de bindings para validar ARP.
- Port Security (máximo de MAC por puerto, sticky MAC).
- Segmentación de VLAN y reducción del dominio de broadcast.
- Configuración de ARP estático en dispositivos críticos.

### 9.2 Capa 3/Aplicación (DNS)
- Forzar uso de DNS interno y bloquear UDP/53 no autorizado.
- Implementar DNSSEC en el resolvedor.
- Uso de DoT/DoH gestionado para proteger integridad/confidencialidad entre cliente y resolver.
- “DNS sinkhole” para dominios maliciosos.

### 9.3 Observabilidad y respuesta
- IDS/IPS (Suricata/Snort) con reglas para anomalías ARP y DNS spoofing.
- Alertas por cambios de MAC del gateway.
- Procedimiento de respuesta: aislar puerto, limpiar tablas ARP y rotar credenciales afectadas.

## 10. Limitaciones
- Reproducibilidad depende de la virtualización y capacidad del entorno de laboratorio.
- Algunos entornos virtuales no emulan completamente DAI o DHCP snooping.