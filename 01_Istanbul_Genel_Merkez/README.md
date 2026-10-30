# 01 — İstanbul Genel Merkez

## Kadro

| Grup | Sayı |
|---|---:|
| Personel (yönetim, finans, İK, hukuk, satış) | 300 |
| IT / teknik | 25 |
| Öğrenci | – |
| Yazılım | – (ayrı birim: `05_Yazilim_Ekibi`) |
| Ar-Ge | – (ayrı birim: `06_ArGe_Ekibi`) |
| **Toplam kullanıcı** | **325** |

Ek rol: Şirket veri merkezi (Active Directory, DNS, ERP, dosya sunucusu, yedekleme, merkezi log) ve tüm şubelerin **VPN hub**'ı.

## Bant genişliği

| Kalem | Değer |
|---|---|
| Hesap | 325 × %75 × 4 Mbps = 975 Mbps → × 1,3 = 1.268 Mbps + 500 Mbps (VPN hub + veri merkezi) |
| **Gerekli** | **~1.768 Mbps** |
| Birincil hat | 2 Gbps Metro Ethernet fiber |
| Yedek hat | 1 Gbps fiber, farklı operatör ve farklı bina girişi |
| Firewall minimum threat protection | 2,65 Gbps |

## Top 5 güvenlik duvarı önerisi

| Sıra | Model | Threat protection / threat prevention | Değerlendirme |
|---:|---|---|---|
| **1** | **Fortinet FortiGate 200G** (HA çift) | 6 Gbps; 11 M eşzamanlı oturum | **Seçildi.** Gereksinimin ~3,4 katı kapasite, yerleşik SD-WAN hub, FortiManager/FortiAnalyzer ile tüm şubeler tek ekrandan |
| 2 | Palo Alto PA-1420 | ~6,0–6,2 Gbps | App-ID ile en iyi uygulama görünürlüğü; maliyeti daha yüksek, SD-WAN için ek lisans |
| 3 | Check Point Quantum Force 9100 | 6,5 Gbps | Güçlü tehdit önleme ve yönetim; benzer kapasitede daha pahalı |
| 4 | Cisco Secure Firewall 3110 | FW+AVC 17 Gbps (IPS açıkken daha düşük) | Cisco altyapısı olan kurumlar için mantıklı; yönetim araçları dağınık |
| 5 | Sophos XGS 3300 / 4300 sınıfı | Güncel datasheet'ten doğrulanmalı | Yönetimi kolay; bu ölçek ve hub rolü için referansı daha az |

## Neden FortiGate 200G?

- Hub rolü: 5 şubenin IPsec tünellerini sonlandıracak; FortiGate'in donanım hızlandırmalı IPsec'i bu rol için uygun.
- Tüm Fortinet şubelerini yöneten FortiManager ve FortiAnalyzer burada barınır.
- 6 Gbps tehdit koruması, SSL derin inceleme açıldığında bile 2 Gbps hattı rahat taşır.

## VLAN'lar

`00_Genel/01_Sirket_Yapisi_ve_Topoloji.md` ortak şablonu (10, 20, 30, 40, 50, 60, 70, 80, 99) birebir uygulanır. Blok: 10.10.0.0/16.

## Şubeye özel kurulum notları

1. İlk devreye alınan birimdir (dalga 1). FortiManager ve FortiAnalyzer, firewall'dan **önce** kurulur ki ilk günden log toplansın.
2. Veri merkezi sunucuları ayrı bir iç segmentte (VLAN 40) tutulur; personel ↔ sunucu trafiği de firewall'dan geçer (iç segmentasyon).
3. Hub tünelleri: her şube için ayrı IPsec arayüzü (`VPN_ANK`, `VPN_LON`, `VPN_AKD`, `VPN_YZL`, `VPN_ARG`).
4. DMZ'de reverse proxy/WAF arkasında yalnızca kurumsal web sitesi ve tedarikçi portalı yayınlanır.
5. Kural seti: `kural_seti.md` · Örnek konfigürasyon: `ornek_config_fortios.conf`.
