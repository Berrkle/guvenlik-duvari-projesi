# Akademik Şube — Kural Seti (FortiGate 900G)

**İlkeler:** Varsayılan reddet · Öğrenci ağı güvenilmez kabul edilir · Öğrenciler iç sistemlere yalnızca DMZ/yayınlanan servisler üzerinden erişir · 5651 kaydı her öğrenci/misafir kuralında açık.
Profil kısaltmaları: **STD** = AV + IPS + web filtre + uygulama kontrolü + DNS filtre · **DPI** = SSL derin inceleme · **CERT** = sertifika incelemesi · **OGR** = öğrenci profili (CERT + web filtre 5651 kategorileri + IPS + uygulama kontrolü)

## A. Altyapı ve yönetim

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 1 | Tehdit-IP-Engel | TI listeleri (giriş) / any (çıkış) | any / TI listeleri | any | REDDET | – | Tümü |
| 2 | MGMT-FW | AKD_IT_JUMP, IST_IT_JUMP (VPN) | FW yönetim IP'leri | HTTPS, SSH | İZİN | – | Tümü |
| 3 | Izleme | IST Zabbix / FortiAnalyzer / SIEM | Akademik ağ cihazları | SNMPv3, Syslog | İZİN | – | Tümü |
| 4 | RADIUS-NAC | Kablosuz denetleyici, switch'ler | AKD_RADIUS_NAC | RADIUS (1812/1813) | İZİN | – | Tümü |
| 5 | eduroam-Federasyon | AKD_RADIUS_NAC | eduroam ulusal RADIUS sunucuları | RADIUS (1812/1813), RadSec (2083) | İZİN | – | Tümü |
| 6 | DHCP-DNS-NTP | Tüm iç ağlar | AKD_DHCP, AKD_DNS, AKD_NTP | DHCP, DNS, NTP | İZİN | DNS filtre | Tümü (5651 DHCP kaydı) |
| 7 | DNS-Dogrudan-Engel | OGRENCI, MISAFIR, EDUROAM, LAB | internet | DNS, DoT, bilinen DoH | REDDET | – | Tümü |

## B. Öğrenci ağı

| # | Kural adı | Kaynak | Hedef | Servis / uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 10 | Ogrenci-Kampus-Servisleri | AKD_OGRENCI | AKD_DMZ (LMS, OBS ön yüzü, e-kütüphane proxy) | HTTPS | İZİN | IPS | Tümü |
| 11 | Ogrenci-Yazdirma | AKD_OGRENCI | AKD_YAZDIRMA (ücretli baskı sunucusu) | HTTPS, IPP | İZİN | – | Tümü |
| 12 | Ogrenci-Ic-Ag-Engel | AKD_OGRENCI | AKD_IDARI, AKD_AKADEMISYEN, AKD_SUNUCU, AKD_SINAV, AKD_LAB, MGMT, VPN | any | REDDET | – | Tümü |
| 13 | Ogrenci-Ogrenci-Engel | AKD_OGRENCI | AKD_OGRENCI | any | REDDET (kablosuzda istemci izolasyonu ile birlikte) | – | Özet |
| 14 | Ogrenci-Riskli-Uygulama | AKD_OGRENCI | internet | BitTorrent/P2P, Tor, VPN/proxy anonimleştiriciler, kripto madenciliği havuzları | REDDET | Uygulama kontrolü | Tümü |
| 15 | Ogrenci-Port-Engel | AKD_OGRENCI | internet | SMTP (25), SMB, RDP, Telnet, SNMP | REDDET | – | Tümü |
| 16 | Ogrenci-Internet | AKD_OGRENCI | internet | HTTP, HTTPS, QUIC (UDP 443 — CERT incelemesi yeterli olduğu için izinli) | İZİN (kişi başı 20/5 Mbps, 300 oturum) | OGR | Tümü (5651) |
| 17 | Ogrenci-Diger-Engel | AKD_OGRENCI | internet | any | REDDET | – | Tümü |

## C. Akademisyen, idari personel, laboratuvar

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 20 | Akademisyen-Sunucular | AKD_AKADEMISYEN | AKD_SUNUCU (LMS yönetim, not girişi, sınav hazırlık) | HTTPS, SMB (bölüm paylaşımları) | İZİN | IPS + AV | Tümü |
| 21 | Idari-OBS-ERP | AKD_IDARI | AKD_SUNUCU (öğrenci bilgi sistemi), IST_ERP (VPN) | HTTPS | İZİN | STD | Tümü |
| 22 | Idari-AD | AKD_IDARI, AKD_AKADEMISYEN | AKD_DC | Kerberos, LDAP/LDAPS, SMB (DC) | İZİN | IPS | Tümü |
| 23 | Akademisyen-Internet | AKD_AKADEMISYEN | internet | HTTP, HTTPS, SSH (araştırma sunucularına), Git | İZİN (kişi başı 50 Mbps) | STD + DPI (KVKK muafiyetleri) | Tümü |
| 24 | Idari-Internet | AKD_IDARI | internet | HTTP, HTTPS | İZİN (kişi başı 30 Mbps) | STD + DPI | Tümü |
| 25 | Lab-Lisans-Guncelleme | AKD_LAB | Yazılım lisans sunucuları, güncelleme FQDN'leri, AKD_DMZ | HTTPS, lisans portları (FlexLM vb.) | İZİN | STD | Tümü |
| 26 | Lab-Internet-Ders-Saatleri | AKD_LAB | internet | HTTP, HTTPS | İZİN (takvim: ders saatleri) | STD + CERT | Tümü |
| 27 | Lab-Diger-Engel | AKD_LAB | any | any | REDDET | – | Tümü |

## D. Sınav ağı

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 30 | Sinav-Sunucu | AKD_SINAV | AKD_SINAV_SUNUCU | HTTPS | İZİN (takvim: Sınav_Saatleri) | IPS | Tümü |
| 31 | Sinav-Bakim | AKD_IT | AKD_SINAV | SSH, RDP, yönetim ajanı | İZİN (takvim: sınav dışı) | IPS | Tümü |
| 32 | Sinav-Her-Sey-Engel | AKD_SINAV | any | any | REDDET | – | Tümü |

## E. Misafir ve eduroam

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 40 | eduroam-Internet | AKD_EDUROAM | internet | HTTP, HTTPS, IPsec/IKE (kendi kurumlarına VPN) | İZİN (kişi başı 10 Mbps) | OGR | Tümü (5651) |
| 41 | Misafir-Internet | AKD_MISAFIR | internet | HTTP, HTTPS | İZİN (SMS doğrulamalı captive portal, 5 Mbps) | OGR | Tümü (5651) |
| 42 | Misafir-eduroam-Ic-Engel | AKD_MISAFIR, AKD_EDUROAM | RFC1918 | any | REDDET | – | Tümü |
| 43 | Karantina | AKD_KARANTINA | AKD_NAC_PORTAL, AV güncelleme FQDN'leri | HTTPS | İZİN | IPS | Tümü |
| 44 | Karantina-Diger-Engel | AKD_KARANTINA | any | any | REDDET | – | Tümü |

## F. Dışarıdan içeriye

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 50 | Web-LMS-Yayini | internet | VIP → AKD_DMZ WAF/reverse proxy | HTTPS | İZİN | IPS + WAF | Tümü |
| 51 | DMZ-Arka-Uc | AKD_DMZ_PROXY | AKD_LMS, AKD_OBS uygulama sunucuları | HTTPS (8443) | İZİN | IPS | Tümü |
| 52 | DMZ-Ic-Engel | AKD_DMZ | Diğer tüm iç ağlar | any | REDDET | – | Tümü |

## G. Son kural

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Log |
|---:|---|---|---|---|---|---|
| 999 | Tumunu-Reddet | any | any | any | REDDET | Tümü |

## Öğrenci web filtre profili (OGR) — engellenen kategoriler

Kötü amaçlı yazılım/phishing, botnet, yetişkin içerik, kumar/bahis, uyuşturucu, şiddet/nefret, anonim proxy/VPN hizmetleri, yasa dışı içerik, yeni kaydedilmiş alan adları (ilk 7 gün), cryptojacking. Eğitim, araştırma, haber, sosyal medya izinli; video akış izinli ama düşük öncelik sınıfında.
