import ids_core
import time
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s [%(levelname)s] %(message)s')

print("=== IDS Core Mock Mode Test ===\n")
print("Sniffing başlatılıyor (threshold=3, eşik)...")
ids_core.start_sniffing(scan_threshold=3)

print("Mock sniff 10 saniye çalışıyor...\n")
time.sleep(10)

print("\n=== Sonuçlar ===")
alerts = ids_core.get_alerts()
print(f"Toplam uyarı: {len(alerts)}")

if alerts:
    for i, alert in enumerate(alerts, 1):
        port_list = ", ".join(str(p) for p in alert["ports"][:3])
        if len(alert["ports"]) > 3:
            port_list += "..."
        print(f"  {i}. IP: {alert['source_ip']} | Ports: {port_list} | Sayım: {alert['count']}")

stats = ids_core.get_stats()
print(f"\nİstatistikler:")
print(f"  - İzlenen IP'ler: {stats['tracked_ips']}")
print(f"  - Toplam uyarı: {stats['alerts']}")
print(f"  - Scapy yüklü: {stats['scapy_available']}")
print(f"  - Mock mode: {stats['mock_mode']}")
