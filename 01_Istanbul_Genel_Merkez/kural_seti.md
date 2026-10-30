# İstanbul Genel Merkez — Kural Seti (FortiGate 200G)

**İlkeler:** Varsayılan reddet · En az yetki · Özel kural genelin üstünde · Her kural loglanır · Her kuralın sahibi ve gözden geçirme tarihi var.

Profil kısaltmaları: **STD** = AV + IPS + web filtre + uygulama kontrolü + DNS filtre · **DPI** = SSL derin inceleme · **CERT** = yalnızca sertifika incelemesi

## A. Yönetim ve altyapı

| # | Kural adı | Kaynak | Hedef | Servis / uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 1 | Tehdit-IP-Engel-Giris | TI listeleri (FortiGuard IoC + harici blok listesi) | any | any | REDDET | – | Tümü |
| 2 | Tehdit-IP-Engel-Cikis | any | TI listeleri | any | REDDET | – | Tümü |
| 3 | MGMT-FW-Yonetim | IT_JUMP_HOST (10.250.10.10) | FW yönetim IP'leri | HTTPS, SSH | İZİN | – | Tümü |
| 4 | MGMT-Ag-Cihazlari | IT_JUMP_HOST | MGMT VLAN | HTTPS, SSH, SNMPv3 | İZİN | IPS | Tümü |
| 5 | Izleme-SNMP-Syslog | Zabbix, FortiAnalyzer, SIEM | Ağ cihazları | SNMPv3 (UDP 161), Syslog (TCP 514/6514) | İZİN | – | Tümü |
| 6 | DNS-Ic-Sunucular | Tüm iç ağlar | IST_DNS_SUNUCU | DNS (53) | İZİN | DNS filtre | Tümü |
| 7 | DNS-Disa-Yalniz-Sunucu | IST_DNS_SUNUCU | İzinli DNS çözücüleri | DNS, DoT (853) | İZİN | DNS filtre | Tümü |
| 8 | DNS-Dogrudan-Engel | Tüm istemci VLAN'ları | any (internet) | DNS, DoT, bilinen DoH sunucuları | REDDET | – | Tümü |
| 9 | NTP | Tüm iç ağlar | IST_DC (NTP) | NTP (123) | İZİN | – | Kapalı |

## B. Şubeler arası (VPN hub)

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 10 | Subeler-AD-DNS | ANK, LON, AKD_PERSONEL, YZL, ARG ağları | IST_DC | Kerberos (88), LDAP (389), LDAPS (636), DNS, SMB (445, yalnızca DC) | İZİN | IPS | Tümü |
| 11 | Subeler-ERP | ANK, LON, AKD_IDARI, YZL, ARG ağları | IST_ERP | HTTPS (443) | İZİN | STD | Tümü |
| 12 | Subeler-Dosya | ANK, LON, ARG ağları | IST_DOSYA | SMB (445) | İZİN | IPS + AV | Tümü |
| 13 | Subeler-Arasi-Dogrudan-Engel | Şube ağları | Diğer şube ağları | any | REDDET | – | Tümü |
| 14 | Yedekleme-Gece | Şube dosya/sunucu ağları | IST_YEDEK | Yedekleme ajan portu | İZİN (takvim: 01:00–06:00) | IPS | Tümü |

## C. İç segmentasyon (personel → veri merkezi)

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 15 | Personel-AD | IST_PERSONEL | IST_DC | Kerberos, LDAP/LDAPS, DNS, SMB (DC) | İZİN | IPS | Tümü |
| 16 | Personel-ERP | IST_PERSONEL | IST_ERP | HTTPS | İZİN | STD | Tümü |
| 17 | Personel-Dosya | IST_PERSONEL | IST_DOSYA | SMB | İZİN | IPS + AV | Tümü |
| 18 | Personel-Yazdirma | IST_PERSONEL | IST_YAZDIRMA_SUNUCU | IPP (631), SMB | İZİN | – | Tümü |
| 19 | YazdirmaSunucu-Yazicilar | IST_YAZDIRMA_SUNUCU | IST_YAZICI_IOT | IPP, RAW (9100) | İZİN | – | Tümü |
| 20 | IT-Sunucu-Yonetim | IST_IT | IST_SUNUCU | RDP (3389), SSH, WinRM (5986) | İZİN (MFA'lı PAM üzerinden) | IPS | Tümü |
| 21 | Personel-Sunucu-Diger-Engel | IST_PERSONEL | IST_SUNUCU | any | REDDET | – | Tümü |
| 22 | VoIP-Santral | IST_VOIP | IST_SANTRAL, SIP_OPERATOR | SIP (5060/5061), RTP aralığı | İZİN | IPS | Tümü |

## D. İnternet çıkışı

| # | Kural adı | Kaynak | Hedef | Servis / uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 23 | Riskli-Uygulama-Engel | Tüm iç ağlar | internet | P2P/torrent, Tor, izinsiz uzaktan erişim (AnyDesk/TeamViewer izinli grup hariç), anonim proxy | REDDET | Uygulama kontrolü | Tümü |
| 24 | SMB-RDP-Disa-Engel | Tüm iç ağlar | internet | SMB, NetBIOS, RDP | REDDET | – | Tümü |
| 25 | SMTP-Dogrudan-Engel | Tüm iç ağlar (mail relay hariç) | internet | SMTP (25) | REDDET | – | Tümü |
| 26 | M365-Dogrudan | IST_PERSONEL, IST_IT | Microsoft 365 (ISDB nesnesi) | HTTPS | İZİN | CERT (M365 önerisi gereği DPI hariç) | Tümü |
| 27 | Personel-Internet | IST_PERSONEL, IST_IT | internet | HTTP, HTTPS (QUIC engelli → TLS'e düşer) | İZİN | STD + DPI (bankacılık/sağlık hariç) | Tümü |
| 28 | Sunucu-Guncelleme | IST_SUNUCU | Güncelleme FQDN'leri (Windows Update, Linux depoları) | HTTPS | İZİN | STD | Tümü |
| 29 | Sunucu-Internet-Engel | IST_SUNUCU | internet | any | REDDET | – | Tümü |
| 30 | IoT-Bulut | IST_YAZICI_IOT | Üretici bulut FQDN'leri | HTTPS | İZİN | IPS | Tümü |
| 31 | Misafir-Internet | IST_MISAFIR | internet | HTTP, HTTPS, DNS (FW üzerinden) | İZİN (captive portal, kişi başı 5 Mbps) | Web filtre + IPS | Tümü (5651) |
| 32 | Misafir-Ic-Engel | IST_MISAFIR | RFC1918 tüm iç ağlar | any | REDDET | – | Tümü |

## E. Dışarıdan içeriye (yayınlanan servisler)

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 33 | Web-Sitesi | internet (coğrafi kısıtlama yok) | VIP → DMZ reverse proxy/WAF | HTTPS | İZİN | IPS + WAF | Tümü |
| 34 | Tedarikci-Portali | internet | VIP → DMZ portal | HTTPS | İZİN | IPS + WAF | Tümü |
| 35 | DMZ-Uygulama | IST_DMZ_PROXY | IST_UYGULAMA_SUNUCU | HTTPS (8443) | İZİN | IPS | Tümü |
| 36 | DMZ-Ic-Engel | IST_DMZ | Tüm iç ağlar | any | REDDET | – | Tümü |
| 37 | Uzaktan-Erisim-VPN | internet | FW IPsec arayüzü | IKE (500, 4500) | İZİN (sertifika + MFA) | – | Tümü |

## F. Son kural

| # | Kural adı | Kaynak | Hedef | Servis | Aksiyon | Log |
|---:|---|---|---|---|---|---|
| 999 | Tumunu-Reddet | any | any | any | REDDET | Tümü |

## Gözden geçirme

| Alan | Değer |
|---|---|
| Kural seti sahibi | Ağ Güvenliği Ekibi |
| Onaylayan | CISO |
| Sertifikasyon periyodu | 3 ay |
| Son gözden geçirme | (doldurulacak) |
