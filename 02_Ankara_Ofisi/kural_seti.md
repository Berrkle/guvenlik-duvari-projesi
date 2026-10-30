# Ankara Ofisi — Kural Seti (FortiGate 120G)

**İlkeler:** Varsayılan reddet · En az yetki · Özel kural genelin üstünde · Her kural loglanır.
Profil kısaltmaları: **STD** = AV + IPS + web filtre + uygulama kontrolü + DNS filtre · **DPI** = SSL derin inceleme · **CERT** = sertifika incelemesi

| # | Kural adı | Kaynak | Hedef | Servis / uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 1 | Tehdit-IP-Engel | TI listeleri (giriş) / any (çıkış) | any (giriş) / TI listeleri (çıkış) | any | REDDET | – | Tümü |
| 2 | MGMT-FW | IST_IT_JUMP_HOST (VPN üzerinden), ANK_IT_JUMP | FW yönetim IP'leri | HTTPS, SSH | İZİN | – | Tümü |
| 3 | Izleme | IST Zabbix / FortiAnalyzer / SIEM | Ankara ağ cihazları | SNMPv3, Syslog | İZİN | – | Tümü |
| 4 | DNS-Yerel-DC | ANK tüm iç ağlar | ANK_RODC (salt okunur DC) | DNS, Kerberos, LDAP/LDAPS | İZİN | IPS | Tümü |
| 5 | DNS-Dogrudan-Engel | ANK istemci VLAN'ları | internet | DNS, DoT, DoH sunucuları | REDDET | – | Tümü |
| 6 | Hub-AD-ERP-Dosya | ANK_PERSONEL, ANK_KAMU | IST_DC, IST_ERP, IST_DOSYA (VPN_IST) | Kerberos, LDAP/LDAPS, HTTPS, SMB | İZİN | IPS + AV | Tümü |
| 7 | ArGe-Dogrudan-Engel | ANK tüm ağlar | ARG ağları (10.60.0.0/16) | any | REDDET | – | Tümü |
| 8 | Kamu-Portallari | ANK_KAMU | Kamu portalı FQDN grubu (EKAP, KEP sağlayıcı, e-imza OCSP/CRL) | HTTPS, OCSP | İZİN | STD + CERT (DPI yok: imza zincirini bozmamak için) | Tümü |
| 9 | Kamu-Diger-Internet-Engel | ANK_KAMU | internet | any | REDDET | – | Tümü |
| 10 | Riskli-Uygulama-Engel | ANK tüm iç ağlar | internet | P2P, Tor, anonim proxy, izinsiz uzaktan erişim | REDDET | Uygulama kontrolü | Tümü |
| 11 | SMB-RDP-SMTP-Disa-Engel | ANK tüm iç ağlar | internet | SMB, RDP, SMTP (25) | REDDET | – | Tümü |
| 12 | M365-Dogrudan | ANK_PERSONEL | Microsoft 365 (ISDB) | HTTPS | İZİN (yerel çıkış) | CERT | Tümü |
| 13 | Personel-Internet | ANK_PERSONEL, ANK_IT | internet | HTTP, HTTPS | İZİN | STD + DPI (KVKK muafiyetleri) | Tümü |
| 14 | VoIP | ANK_VOIP | IST_SANTRAL (VPN), SIP_OPERATOR | SIP, RTP | İZİN | IPS | Tümü |
| 15 | Yazici | ANK_PERSONEL | ANK_YAZDIRMA_SUNUCU | IPP, SMB | İZİN | – | Tümü |
| 16 | Misafir-Internet | ANK_MISAFIR | internet | HTTP, HTTPS | İZİN (captive portal, 5 Mbps/kişi) | Web filtre + IPS | Tümü (5651) |
| 17 | Misafir-Ic-Engel | ANK_MISAFIR | RFC1918 | any | REDDET | – | Tümü |
| 18 | DR-Hub-Tunelleri | LON, AKD, YZL, ARG ağları (yedek tüneller) | IST_DC_YEDEK (Ankara'daki DR kopyaları) | Kural 6 ile aynı servisler | İZİN (yalnızca DR modunda etkin) | IPS | Tümü |
| 999 | Tumunu-Reddet | any | any | any | REDDET | – | Tümü |
