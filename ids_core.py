import threading
import logging
import time
import random

try:
    from scapy.all import sniff, IP, TCP
    _SCAPY_AVAILABLE = True
except Exception:
    _SCAPY_AVAILABLE = False

# İç durum
attempted_connections = {}  # IP -> set(ports)
alerts = []  # Liste halinde uyarılar
_lock = threading.Lock()
_sniff_thread = None
_mock_mode = False


def detect_port_scan(source_ip, destination_port, scan_threshold):
    """Port taraması kuralını kontrol eder ve uyarı listesine ekler."""
    with _lock:
        s = attempted_connections.setdefault(source_ip, set())
        s.add(destination_port)

        if len(s) >= scan_threshold:
            alert = {
                "timestamp": time.time(),
                "source_ip": source_ip,
                "ports": sorted(list(s)),
                "count": len(s),
            }
            alerts.append(alert)
            logging.warning("!!! YÜKSEK RİSK UYARISI: PORT TARAMASI TESPİT EDİLDİ !!!")
            logging.warning(f"Kaynak IP: {source_ip} - {len(s)} farklı port denemesi.")

            # Aynı IP için tekrar eden spam uyarılarını azaltmak için temizle
            attempted_connections[source_ip] = set()


def packet_callback(packet, scan_threshold=5):
    """sniff tarafından çağrılan callback; yalnızca IP/TCP SYN paketlerini işler."""
    if not _SCAPY_AVAILABLE:
        return

    if IP in packet and TCP in packet:
        # Flags bazen Scapy'de farklı tiplerde gelebilir, string karşılaştırması güvenli
        if 'S' in str(packet[TCP].flags):
            source_ip = packet[IP].src
            destination_port = packet[TCP].dport
            detect_port_scan(source_ip, destination_port, scan_threshold)

        logging.info(f"Connection attempt: {packet[IP].src}:{packet[TCP].sport} -> {packet[IP].dst}:{packet[TCP].dport}")


def _sniff_worker(scan_threshold, iface):
    try:
        if not _SCAPY_AVAILABLE:
            logging.warning("Scapy yüklenemedi; Mock moda geçildi (sahte veriler).")
            _mock_sniff_worker(scan_threshold)
            return

        try:
            sniff(prn=lambda pkt: packet_callback(pkt, scan_threshold=scan_threshold), store=0, iface=iface)
        except RuntimeError as e:
            if "winpcap" in str(e).lower() or "npcap" in str(e).lower():
                logging.warning(f"Npcap/WinPcap yüklü değil: {e}")
                logging.warning("Mock moda geçildi (sahte veriler).")
                _mock_sniff_worker(scan_threshold)
            else:
                logging.error(f"Sniff hatası: {e}")
                raise
    except Exception as e:
        logging.error(f"_sniff_worker'da beklenmeyen hata: {e}")
        logging.exception("Stack trace:")


def _mock_sniff_worker(scan_threshold):
    """Scapy olmadığında sahte paketler ve uyarılar üretir."""
    global _mock_mode
    _mock_mode = True
    logging.info(f"Mock sniffing başlatılıyor (eşik: {scan_threshold})...")
    
    fake_ips = [f"192.168.1.{random.randint(100, 200)}" for _ in range(3)]
    
    while _mock_mode:
        # Rastgele bir IP ve port seçin
        source_ip = random.choice(fake_ips)
        destination_port = random.randint(1, 65535)
        
        # Tespit fonksiyonunu çağır
        detect_port_scan(source_ip, destination_port, scan_threshold)
        logging.debug(f"Mock paket: {source_ip}:* -> *:{destination_port}")
        
        # Biraz bekleme (gerçekçi görünmesi için)
        time.sleep(random.uniform(0.1, 0.5))



def start_sniffing(scan_threshold=5, iface=None):
    """Arka planda sniffing başlatır (daemon thread). Tekrarlı çağrılarda mevcut thread'ı korur."""
    global _sniff_thread
    if _sniff_thread and _sniff_thread.is_alive():
        logging.info("Sniffing zaten çalışıyor.")
        return

    try:
        _sniff_thread = threading.Thread(target=_sniff_worker, args=(scan_threshold, iface), daemon=True)
        _sniff_thread.start()
        logging.info("Sniffing başlatıldı.")
    except Exception as e:
        logging.error(f"Sniffing başlatılamadı: {e}")


def get_alerts():
    with _lock:
        # timestamp'ları okunabilir forma çevirebiliriz
        return [
            {
                "timestamp": a["timestamp"],
                "time_human": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(a["timestamp"])),
                "source_ip": a["source_ip"],
                "ports": a["ports"],
                "count": a["count"],
            }
            for a in alerts
        ]


def get_stats():
    with _lock:
        return {"tracked_ips": len(attempted_connections), "alerts": len(alerts), "scapy_available": _SCAPY_AVAILABLE, "mock_mode": _mock_mode}

