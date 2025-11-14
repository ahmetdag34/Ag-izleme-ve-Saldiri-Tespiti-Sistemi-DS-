from scapy.all import sniff, IP, TCP
import argparse
import logging

# Kural Tespiti İçin Global Değişkenler
attempted_connections = {}  # IP: {Port} yapısını tutacak


def parse_args():
    parser = argparse.ArgumentParser(description="Basit IDS - Port taraması tespiti")
    parser.add_argument("--threshold", "-t", type=int, default=5,
                        help="Bir IP'den kabul edilecek farklı port deneme eşiği (varsayılan: 5)")
    parser.add_argument("--interface", "-i", type=str, default=None,
                        help="Dinlenecek ağ arayüzü (varsayılan: tüm arayüzler)")
    return parser.parse_args()


def detect_port_scan(source_ip, destination_port, scan_threshold):
    """Port taraması kuralını kontrol eder."""
    global attempted_connections

    if source_ip not in attempted_connections:
        attempted_connections[source_ip] = set()

    attempted_connections[source_ip].add(destination_port)

    # Eğer aynı kaynaktan gelen farklı hedef port sayısı eşiği aşarsa
    if len(attempted_connections[source_ip]) >= scan_threshold:
        logging.warning("#######################################################")
        logging.warning("!!! YÜKSEK RİSK UYARISI: PORT TARAMASI TESPİT EDİLDİ !!!")
        logging.warning(f"!!! Kaynak IP: {source_ip} - {scan_threshold} farklı port denemesi. !!!")
        logging.warning("#######################################################")

        # Tespit edildikten sonra aynı kaynaktan tekrar eden spam uyarılarını azaltmak için temizleyelim
        attempted_connections[source_ip] = set()


def packet_callback(packet, scan_threshold=None):
    """Her yakalanan paket için çağrılan fonksiyon."""

    # Sadece TCP ve IP paketlerini işleyelim
    if IP in packet and TCP in packet:
        # Sadece SYN bayrağı olan paketleri kontrol edelim (Yeni bağlantı denemeleri)
        # flags bazen Scapy'de FlagsValue tipinde gelir, güvenli karşılaştırma için string olarak kontrol edelim
        if 'S' in str(packet[TCP].flags):  # 'S' = SYN bayrağı
            source_ip = packet[IP].src
            destination_port = packet[TCP].dport

            # Port taraması kontrolünü yap
            detect_port_scan(source_ip, destination_port, scan_threshold)

        logging.info(f"[*] Bağlantı Denemesi: {packet[IP].src}:{packet[TCP].sport} -> {packet[IP].dst}:{packet[TCP].dport}")


def main():
    args = parse_args()

    # Logging yapılandırması (zaman damgası ile)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    logging.info("Ağ dinleniyor ve Port Taraması Tespiti aktif...")
    logging.info(f"Eşik (threshold): {args.threshold}")

    # sniff çağrısında packet_callback'a scan_threshold değerini geçmek için lambda kullanıyoruz
    sniff(prn=lambda pkt: packet_callback(pkt, scan_threshold=args.threshold), store=0, iface=args.interface)


if __name__ == '__main__':
    main()