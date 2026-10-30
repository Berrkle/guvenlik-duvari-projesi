# 04 — Akademik Şube

## Kadro

| Grup | Sayı |
|---|---:|
| **Öğrenci** | **10.000** |
| Akademisyen (hoca) | 600 |
| İdari personel | 400 |
| IT / teknik | 40 |
| Yazılım | – |
| Ar-Ge | – (akademik araştırma laboratuvarları VLAN 120'de) |
| **Toplam kullanıcı** | **11.040** |
| Tahmini cihaz | ~25.000 (öğrenci başı ~2 cihaz + kampüs cihazları) |

Bu birim şirketin **en büyük ve en riskli** ağıdır: kontrol edilemeyen kişisel cihazlar (BYOD), yüksek eşzamanlı oturum sayısı, sınav dönemlerinde ani yük, 5651 kapsamında toplu kullanım sağlayıcı yükümlülükleri.

## Bant genişliği

| Kalem | Değer |
|---|---|
| Öğrenci | 10.000 × %35 × 1,5 Mbps = 5.250 Mbps |
| Akademik + idari + IT | 1.040 × %70 × 3 Mbps = 2.184 Mbps |
| Ham toplam | 7.434 Mbps → × 1,3 = 9.664 Mbps |
| Servis payı (LMS, sınav sistemi, web sitesi, e-kütüphane) | 1.000 Mbps |
| **Gerekli** | **~10,7 Gbps** |
| Hat | **2 × 10 Gbps**, iki farklı operatör, aktif-aktif SD-WAN (toplam 20 Gbps) |
| Firewall minimum threat protection | 16 Gbps |

**Hat koparsa:** Kalan 10 Gbps'te QoS devreye girer: sunucular ve akademik/idari personel korunur, öğrenci üst limiti %60'a çekilir.

### Kampüs içi dağıtım (QoS)

| Grup | Garanti | Üst limit | Kişi başı |
|---|---:|---:|---|
| Sunucular (LMS, sınav, web) | %15 | %40 | – |
| Akademisyen | %20 | %60 | 50 Mbps |
| İdari personel | %15 | %50 | 30 Mbps |
| Öğrenci | %40 | %80 | 20 Mbps indirme / 5 Mbps yükleme, en fazla 300 eşzamanlı oturum |
| Laboratuvar | %5 | %20 | – |
| Misafir / eduroam misafir | – | %5 | 5 Mbps |

Sınav saatlerinde: sınav VLAN'ı + LMS en yüksek öncelik, öğrenci üst limiti %60.

## Top 5 güvenlik duvarı önerisi

| Sıra | Model | Threat protection / threat prevention | Eşzamanlı oturum | Değerlendirme |
|---:|---|---|---:|---|
| **1** | **Fortinet FortiGate 900G** (HA çift) | 20–30 Gbps (datasheet revizyonuna göre); SSL inceleme ~16,7 Gbps | 16 M | **Seçildi.** 25 GbE portlar, NP7 hızlandırma; tasarımda temkinli 20 Gbps esas alındı |
| 2 | Palo Alto PA-5410 | ~22–35 Gbps (kaynağa göre) | ~5 M | Kampüs kenarı için güçlü; oturum kapasitesi 25.000 cihaz için daha dar, maliyet yüksek |
| 3 | Check Point Quantum Force 19100 | 28,8–35 Gbps | – | Yüksek kapasite, 2U modüler; maliyet yüksek |
| 4 | Cisco Secure Firewall 4215 | FW+AVC 65 Gbps (IPS açıkken daha düşük); 40 M oturum | 40 M | Çok yüksek oturum kapasitesi; yönetim karmaşık |
| 5 | Sophos XGS 8500 | 34 Gbps (2023 açıklaması; yeni metodolojiyle daha yüksek) | 58 M | Kampüs kenarı için tasarlanmış; büyük ölçekte referans daha az |

**Büyüme adımı:** Öğrenci sayısı 15.000'i aşarsa FortiGate 3000F (33 Gbps threat protection, 70 M oturum) sınıfına geçilir.

## Neden FortiGate 900G?

- Öğrenci trafiğinde SSL derin inceleme yapılmadığı için (gizlilik + performans) 20 Gbps tehdit koruması, 10,7 Gbps ihtiyacı ~1,9 kat karşılar.
- 16 M eşzamanlı oturum: 25.000 cihaz × ~300 oturum = 7,5 M → yaklaşık 2 kat pay.
- Diğer şubelerle aynı yönetim; FortiAnalyzer 5651 raporlaması için hazır şablonlar.

## VLAN'lar (Akademik Şube'ye özel)

| VLAN | Ad | Ağ | Not |
|---:|---|---|---|
| 10 | MGMT | 10.250.40.0/24 | |
| 20 | IDARI | 10.40.20.0/22 | İdari personel |
| 30 | IT | 10.40.30.0/24 | |
| 40 | SUNUCU | 10.40.40.0/22 | LMS, öğrenci bilgi sistemi, sınav, kütüphane |
| 80 | DMZ | 10.40.80.0/24 | Web sitesi, LMS ön yüzü, e-kütüphane proxy |
| 100 | OGRENCI | 10.100.0.0/16 | Bina başına /20; kablosuzda istemci izolasyonu açık |
| 110 | AKADEMISYEN | 10.40.110.0/22 | 802.1X, kurumsal cihaz |
| 120 | LAB | 10.40.120.0/22 | Bilgisayar ve araştırma laboratuvarları |
| 130 | SINAV | 10.40.130.0/24 | Sınav salonu bilgisayarları; yalnızca sınav sunucusu |
| 140 | KUTUPHANE | 10.40.140.0/24 | Kütüphane kiosk bilgisayarları |
| 150 | EDUROAM | 10.101.0.0/18 | Diğer üniversitelerden gelen eduroam kullanıcıları |
| 70 | MISAFIR | 10.40.70.0/23 | Etkinlik misafirleri, captive portal |
| 99 | KARANTINA | 10.40.99.0/24 | NAC'ın attığı riskli cihazlar |

## Şubeye özel kurulum notları

1. **Zamanlama:** Dalga 6, yarıyıl tatilinde. Önce idari ve akademik VLAN'lar, bir hafta sonra öğrenci ağı.
2. **5651:** DHCP IP dağıtım kayıtları ve erişim kayıtları 2 yıl saklanır (yönetmelik madde 4); kayıtlar değiştirilemez arşive alınır ve günlük hash/zaman damgası ile bütünlüğü korunur. Suç teşkil eden içeriğe erişimi önleyici web filtre kategorileri zorunludur.
3. **Kimlik:** Öğrenci kablosuzu 802.1X (öğrenci numarası + şifre, RADIUS); FortiGate'te FSSO/RADIUS ile kullanıcı tabanlı loglama — IP değil kişi görünür.
4. **NAC:** Ağa bağlanan cihazlar kontrol edilir; tehdit görülen cihaz otomatik karantina VLAN'ına alınır (`00_Genel/04_Izleme_ve_Operasyon.md` senaryosu).
5. **Sınav sistemi:** Sınav VLAN'ı sınav saatlerinde yalnızca sınav sunucusuna erişir; internet tamamen kapalı. Takvim nesnesi sınav programından üretilir.
6. **SSL inceleme:** Öğrenci trafiğinde yalnızca sertifika incelemesi (SNI tabanlı kategori filtreleme). Derin inceleme personel ve akademisyen kurumsal cihazlarında.
7. Kural seti: `kural_seti.md` · Örnek konfigürasyon: `ornek_config_fortios.conf`.
