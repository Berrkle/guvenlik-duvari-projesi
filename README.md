# Güvenlik Duvarı Projesi — NovaTek Holding (hayali şirket)

Bu klasör, çok şubeli hayali bir şirket için **bant genişliği tanımlama**, **adım adım güvenlik duvarı kurulumu**, **şube bazlı top 5 güvenlik duvarı önerisi**, **kural setleri** ve **izleme (monitoring) modeli** içerir.

> Ürün performans değerleri üreticilerin datasheet'lerinden (Ekim 2026 itibarıyla erişilebilen sürümler) alınmıştır. Değerler test metodolojisine ve yazılım sürümüne göre değişebilir; satın almadan önce güncel datasheet ile doğrulanmalıdır.

## Klasör yapısı

```
Guvenlik_Duvari_Projesi/
├── README.md                          ← bu dosya (genel özet)
├── 00_Genel/
│   ├── 01_Sirket_Yapisi_ve_Topoloji.md   kadro, IP/VLAN planı, bölgeler (zone), topoloji
│   ├── 02_Bant_Genisligi.md              hesap yöntemi, hat seçimi, QoS politikası
│   ├── 03_Adim_Adim_Kurulum.md           tüm şubeler için 16 adımlı kurulum prosedürü
│   ├── 04_Izleme_ve_Operasyon.md         sistematik + insan tarafı izleme, SOC/NOC
│   ├── 05_Neden_Tercih_Etmedik.md        (opsiyonel) elenen ürünler ve gerekçeleri
│   ├── bant_genisligi_hesapla.py         hesap aracı (çalıştırılabilir)
│   └── ozet_bant_genisligi.csv           hesap çıktısı
├── 01_Istanbul_Genel_Merkez/   README.md · kural_seti.md · ornek_config_fortios.conf
├── 02_Ankara_Ofisi/            README.md · kural_seti.md · ornek_config_fortios.conf
├── 03_Londra_Ofisi/            README.md · kural_seti.md · ornek_config_fortios.conf
├── 04_Akademik_Sube/           README.md · kural_seti.md · ornek_config_fortios.conf
├── 05_Yazilim_Ekibi/           README.md · kural_seti.md · ornek_config_panos.txt
└── 06_ArGe_Ekibi/              README.md · kural_seti.md · ornek_config_panos.txt
```

## Şirket özeti

| Birim | Konum | Personel | Öğrenci | Yazılım/Teknik | Ar-Ge | Toplam kullanıcı |
|---|---|---:|---:|---:|---:|---:|
| İstanbul Genel Merkez (+ veri merkezi) | İstanbul | 300 | – | 25 | – | 325 |
| Ankara Ofisi | Ankara | 140 | – | 10 | – | 150 |
| Londra Ofisi | Londra | 75 | – | 5 | – | 80 |
| Akademik Şube | İstanbul (kampüs) | 1.000 (600 akademisyen + 400 idari) | 10.000 | 40 | – | 11.040 |
| Yazılım Ekibi | İstanbul (teknopark binası) | – | – | 150 | – | 150 |
| Ar-Ge Ekibi | Ankara (teknokent binası) | – | – | 10 | 60 | 70 |
| **Toplam** | | **1.515** | **10.000** | **240** | **60** | **11.815** |

## Bant genişliği ve seçilen güvenlik duvarı (özet)

| Birim | Hesaplanan ihtiyaç | Seçilen internet hattı | Seçilen güvenlik duvarı (#1) | Threat Prot. kapasitesi |
|---|---:|---|---|---:|
| İstanbul GM | ~1,77 Gbps | 2 Gbps + 1 Gbps yedek | FortiGate 200G (HA çift) | 6 Gbps |
| Ankara | ~489 Mbps | 500 Mbps + 200 Mbps yedek | FortiGate 120G (HA çift) | 2,8 Gbps |
| Londra | ~284 Mbps | 500 Mbps leased line + 200 Mbps FTTP yedek | FortiGate 90G (HA çift) | 2,2 Gbps |
| Akademik Şube | ~10,7 Gbps | 2 × 10 Gbps (iki farklı operatör, aktif-aktif) | FortiGate 900G (HA çift) | 20–30 Gbps* |
| Yazılım Ekibi | ~1,9 Gbps | 2 Gbps + 1 Gbps yedek | Palo Alto PA-3410 (HA çift) | 7,5 Gbps |
| Ar-Ge | ~919 Mbps | 1 Gbps + 500 Mbps yedek | Palo Alto PA-1420 (HA çift) | ~6 Gbps |

\* FortiGate 900G için kaynaklar datasheet revizyonuna göre 20 Gbps ve 30 Gbps değerleri veriyor; tasarımda temkinli olarak 20 Gbps esas alınmıştır.

## Mimari kararın özeti

- **Çevre (perimeter) + SD-WAN katmanı: Fortinet.** Tüm şubelerde FortiGate → tek FortiManager ile merkezi yönetim, yerleşik SD-WAN, Türkiye'de güçlü iş ortağı/destek ağı, fiyat/performans.
- **Kritik iç segmentler (Yazılım, Ar-Ge): Palo Alto.** Kaynak kod ve fikri mülkiyet bu segmentlerde. İkinci bir üretici kullanarak *derinlemesine savunma* (defense-in-depth) sağlanır: bir üreticide çıkan kritik açık iki katmanı birden düşürmez. App-ID ve DLP/dosya engelleme yetenekleri bu kullanım için güçlü.
- **Topoloji:** İstanbul GM hub, diğer şubeler spoke. Şubeler arası IPsec (IKEv2, AES-256-GCM) tüneller; Akademik Şube internete doğrudan çıkar (local breakout).
- **Varsayılan politika:** Her yerde *default deny* (açıkça izin verilmeyen her şey yasak), en az yetki, her kuralın sahibi ve gözden geçirme tarihi var.
- **İzleme:** FortiAnalyzer + Panorama → merkezi SIEM (Wazuh / kurumsal alternatif Splunk veya Microsoft Sentinel) → SOC. Ayrıntılar `00_Genel/04_Izleme_ve_Operasyon.md` içinde.

## Okuma sırası (sunum için önerilen)

1. `00_Genel/01_Sirket_Yapisi_ve_Topoloji.md`
2. `00_Genel/02_Bant_Genisligi.md`
3. Her şube klasöründeki `README.md` (top 5 + seçim gerekçesi)
4. Her şube klasöründeki `kural_seti.md`
5. `00_Genel/03_Adim_Adim_Kurulum.md`
6. `00_Genel/04_Izleme_ve_Operasyon.md`
7. (Opsiyonel) `00_Genel/05_Neden_Tercih_Etmedik.md`

## Kaynaklar (datasheet ve mevzuat)

- Fortinet FortiGate 90G/120G/200G karşılaştırması — datacenter360.ca (Fortinet datasheet ve Product Matrix, Mayıs 2026 verisi)
- FortiGate 900G — datacenter360.ca ve networktigers.com (datasheet değerleri)
- Palo Alto PA-1400/3400/5400 — paloguard.com model karşılaştırma tablosu, paloaltonetworks.com
- Check Point Quantum Force 9100/9300/19100 — checkpoint.com datasheet'leri ve cihaz karşılaştırma tablosu
- Cisco Secure Firewall 1200/3100/4200 — cisco.com datasheet'leri
- Sophos XGS — sophos.com ürün sayfaları ve 2023 XGS 7500/8500 duyurusu
- 5651 sayılı Kanun ve İnternet Toplu Kullanım Sağlayıcıları Hakkında Yönetmelik — mevzuat.gov.tr (erişim kayıtlarını 2 yıl saklama yükümlülüğü)
