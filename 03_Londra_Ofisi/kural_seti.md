# Londra Ofisi — Kural Seti (FortiGate 90G)

**İlkeler:** Varsayılan reddet · En az yetki · Yerel çıkış (local breakout) · UK GDPR uyumu.
Profil kısaltmaları: **STD** = AV + IPS + web filtre + uygulama kontrolü + DNS filtre · **DPI** = SSL derin inceleme · **CERT** = sertifika incelemesi

| # | Kural adı | Kaynak | Hedef | Servis / uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 1 | Tehdit-IP-Engel | TI listeleri (giriş) / any (çıkış) | any (giriş) / TI listeleri (çıkış) | any | REDDET | – | Tümü |
| 2 | MGMT-FW-Uzaktan | IST_IT_JUMP_HOST (yalnızca VPN_IST üzerinden) | FW yönetim IP'leri | HTTPS, SSH | İZİN | – | Tümü |
| 3 | Izleme | IST Zabbix / FortiAnalyzer / SIEM (VPN) | Londra ağ cihazları | SNMPv3, Syslog | İZİN | – | Tümü |
| 4 | DNS-Yerel | LON tüm iç ağlar | LON_DNS (DC) | DNS | İZİN | DNS filtre | Tümü |
| 5 | DNS-Dogrudan-Engel | LON istemci VLAN'ları | internet | DNS, DoT, DoH | REDDET | – | Tümü |
| 6 | Hub-AD-ERP | LON_PERSONEL | IST_DC, IST_ERP (VPN_IST) | Kerberos, LDAP/LDAPS, HTTPS | İZİN | IPS | Tümü |
| 7 | Hub-Dosya | LON_PERSONEL | IST_DOSYA (VPN_IST) | SMB | İZİN | IPS + AV | Tümü |
| 8 | Hub-Diger-Engel | LON tüm ağlar | Diğer şube ağları | any | REDDET | – | Tümü |
| 9 | M365-SaaS-Yerel-Cikis | LON_PERSONEL | Microsoft 365, onaylı SaaS (ISDB) | HTTPS | İZİN | CERT | Tümü |
| 10 | Riskli-Uygulama-Engel | LON tüm iç ağlar | internet | P2P, Tor, anonim proxy, izinsiz uzaktan erişim, onaysız bulut depolama | REDDET | Uygulama kontrolü | Tümü |
| 11 | SMB-RDP-SMTP-Disa-Engel | LON tüm iç ağlar | internet | SMB, RDP, SMTP (25) | REDDET | – | Tümü |
| 12 | Personel-Internet | LON_PERSONEL, LON_IT | internet | HTTP, HTTPS | İZİN | STD + DPI (sağlık, bankacılık, kişisel e-posta muaf — GDPR) | Tümü |
| 13 | VoIP-Teams | LON_VOIP | Teams Phone / SIP operatörü | SIP, RTP, Teams medya portları | İZİN | IPS | Tümü |
| 14 | Yazici | LON_PERSONEL | LON_YAZICI | IPP | İZİN | – | Tümü |
| 15 | Misafir-Internet | LON_MISAFIR | internet | HTTP, HTTPS | İZİN (kişi başı 5 Mbps, kabul edilebilir kullanım sayfası) | Web filtre + IPS | Tümü |
| 16 | Misafir-Ic-Engel | LON_MISAFIR | RFC1918 | any | REDDET | – | Tümü |
| 999 | Tumunu-Reddet | any | any | any | REDDET | – | Tümü |

## GDPR notları

- Misafir ağında toplanan loglar 90 gün sıcak, 1 yıl arşivde tutulur; daha uzun saklama için hukuki dayanak gerekir.
- Logları görüntüleme yetkisi: Londra IT + SOC; HR veya yöneticiler logları doğrudan göremez, yalnızca resmi talep ve DPO onayı ile.
