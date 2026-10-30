# 02 — Ankara Ofisi

## Kadro

| Grup | Sayı |
|---|---:|
| Personel (kamu ilişkileri, ihale, bölge satış, idari) | 140 |
| IT / teknik | 10 |
| Öğrenci | – |
| Yazılım | – |
| Ar-Ge | – (aynı şehirde ayrı birim: `06_ArGe_Ekibi`) |
| **Toplam kullanıcı** | **150** |

Ek rol: İstanbul GM devre dışı kalırsa **ikincil VPN hub** (felaket kurtarma). Kamu kurumlarıyla e-imza / KEP / ihale portalı trafiği yoğun.

## Bant genişliği

| Kalem | Değer |
|---|---|
| Hesap | 150 × %75 × 3 Mbps = 338 Mbps → × 1,3 = 439 Mbps + 50 Mbps servis payı |
| **Gerekli** | **~489 Mbps** |
| Birincil hat | 500 Mbps fiber |
| Yedek hat | 200 Mbps, farklı operatör |
| Firewall minimum threat protection | 0,73 Gbps |

> Birincil hat sınırda (%2 boşluk). İlk 3 ay ölçülür; sürekli %80 üzeri kullanımda 1 Gbps'e yükseltilir.

## Top 5 güvenlik duvarı önerisi

| Sıra | Model | Threat protection / threat prevention | Değerlendirme |
|---:|---|---|---|
| **1** | **Fortinet FortiGate 120G** (HA çift) | 2,8 Gbps; 3 M eşzamanlı oturum | **Seçildi.** Gereksinimin ~5,7 katı; 1U rack, çift güç kaynağı; İstanbul ile aynı yönetim |
| 2 | Palo Alto PA-1410 | 4,5 Gbps | Daha yüksek kapasite; maliyet ve ikinci yönetim aracı gerektirir |
| 3 | Check Point Quantum 3920 | 3,2 Gbps | Şube sınıfında güçlü; lisans maliyeti yüksek |
| 4 | Cisco Secure Firewall 1230 | FW+AVC 13 Gbps (IPS açıkken daha düşük) | Kompakt ve uygun; tehdit önleme değeri ayrıca doğrulanmalı |
| 5 | Sophos XGS 118 | 3,25 Gbps | Kolay yönetim; masaüstü form faktör, HA için ek kurulum |

## Neden FortiGate 120G?

- Gereksinimi rahatça karşılar ve ikincil hub rolünde 5 tüneli kaldırabilir.
- FortiGate 90G de kapasite olarak yeterdi; ancak ikincil hub rolü ve rack montaj/çift güç kaynağı ihtiyacı nedeniyle 120G seçildi.

## VLAN'lar

Ortak şablon (10–99), blok 10.20.0.0/16. Ek VLAN: **25 — KAMU_ENTEGRASYON** (e-imza/KEP istemcileri ve ihale işlemleri yapan sabit iş istasyonları).

## Şubeye özel kurulum notları

1. Dalga 2'de, İstanbul hub çalıştıktan sonra kurulur.
2. Ar-Ge birimine (aynı şehir) doğrudan tünel **yoktur**; Ar-Ge trafiği her zaman İstanbul hub'ı üzerinden ve Ar-Ge'nin kendi Palo Alto'sundan geçer.
3. İkincil hub için Londra, Akademik, Yazılım ve Ar-Ge'den gelen yedek tüneller tanımlanır ama SD-WAN kuralıyla yalnızca İstanbul tüneli düştüğünde trafik taşır.
4. Kural seti: `kural_seti.md` · Örnek konfigürasyon: `ornek_config_fortios.conf`.
