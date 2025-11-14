# Basit IDS - Web Arayüzü

Bu proje, `simple_ids.py` üzerinde basit bir port taraması tespiti mantığını kullanan küçük bir web arayüzü demo'su içerir.

Dosyalar
- `simple_ids.py` - Komut satırı ile çalıştırılabilen orijinal basit IDS (ayrık olarak bırakıldı).
- `ids_core.py` - Web arayüzü tarafından paylaşılacak çekirdek tespit mantığı ve arka plan sniff başlatma.
- `web_app.py` - Flask tabanlı web arayüzü.
- `templates/index.html` - Basit HTML şablonu.
- `requirements.txt` - Gerekli paketler (`flask`, `scapy`).

Çalıştırma

1. Sanal ortam oluşturun (opsiyonel ama önerilir):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Web sunucusunu başlatın:

```powershell
python .\web_app.py
```

3. Tarayıcıda `http://localhost:5000` adresine gidin. Arayüzden sniffing'i başlatabilirsiniz.

Notlar ve uyarılar
- Windows'ta ağ trafiğini ham şekilde yakalamak için yönetici (Admin) hakları gerekebilir.
- `scapy` bazı Windows kurulumlarında ek bağımlılıklar veya WinPcap/Npcap gerektirir.
- Bu demo eğitim amaçlıdır; üretimde kullanmadan önce güvenlik, yetkilendirme ve sağlamlık ekleyin.
