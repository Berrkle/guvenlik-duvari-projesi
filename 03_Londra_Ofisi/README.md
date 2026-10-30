# 03 — Londra Ofisi

## Kadro

| Grup | Sayı |
|---|---:|
| Personel (UK/AB operasyonları, iş geliştirme, finans) | 75 |
| IT / teknik | 5 |
| Öğrenci | – |
| Yazılım | – |
| Ar-Ge | – |
| **Toplam kullanıcı** | **80** |

Özel durum: **UK GDPR** kapsamında kişisel veri işleniyor. Yerel IT ekibi küçük olduğu için yönetim büyük ölçüde İstanbul'dan uzaktan yapılır; sahada "akıllı el" (remote hands) desteği alınır.

## Bant genişliği

| Kalem | Değer |
|---|---|
| Hesap | 80 × %75 × 3 Mbps = 180 Mbps → × 1,3 = 234 Mbps + 50 Mbps servis payı |
| **Gerekli** | **~284 Mbps** |
| Birincil hat | 500 Mbps leased line (simetrik, SLA'lı) |
| Yedek hat | 200 Mbps FTTP, farklı operatör |
| Firewall minimum threat protection | 0,43 Gbps |

Not: UK'de iş hatları genellikle 100/200/500/1000 Mbps kademelerinde satılır; 284 Mbps'i karşılayan ilk kademe 500 Mbps'tir. Ek kapasite, Türkiye ile video konferans yoğunluğunu rahatlatır.

## Top 5 güvenlik duvarı önerisi

| Sıra | Model | Threat protection / threat prevention | Değerlendirme |
|---:|---|---|---|
| **1** | **Fortinet FortiGate 90G** (HA çift) | 2,2 Gbps; 3 M eşzamanlı oturum | **Seçildi.** Gereksinimin ~7,7 katı; masaüstü form faktör, sıfır dokunuşla kurulum (FortiManager'dan uzaktan provizyon) |
| 2 | Palo Alto PA-1410 | 4,5 Gbps | Kapasite fazlası; bu ölçek için maliyeti yüksek |
| 3 | Check Point Quantum 3920 | 3,2 Gbps | Güçlü; maliyet ve ayrı yönetim |
| 4 | Cisco Secure Firewall 1220 | FW+AVC 9 Gbps (IPS açıkken daha düşük) | Kompakt; UK'de Cisco destek ağı güçlü |
| 5 | Sophos XGS 108 | 2,5 Gbps | Sophos'un UK merkezli olması yerel destek avantajı; tek üretici standardından sapma |

## Neden FortiGate 90G?

- Sahada az IT personeli var: cihaz kutudan çıkınca FortiManager'a bağlanıp şablon konfigürasyonu otomatik çeker (zero-touch provisioning).
- İstanbul'la aynı politika paketleri; Londra'ya özel yalnızca GDPR ve yerel çıkış kuralları eklenir.

## VLAN'lar

Ortak şablon (10–99), blok 10.30.0.0/16.

## Şubeye özel kurulum notları

1. Dalga 5'te kurulur. Cihazlar İstanbul'da ön-konfigüre edilip kargo ile gönderilir veya zero-touch ile provizyon edilir.
2. **Yerel internet çıkışı (local breakout):** M365, SaaS ve genel web Londra'dan doğrudan çıkar; yalnızca şirket iç uygulamaları (ERP, AD) İstanbul tüneline gider. Böylece gecikme düşer ve kişisel veri gereksiz yere ülke dışına taşınmaz.
3. **GDPR:** Londra logları FortiAnalyzer'da ayrı bir yönetim alanında (ADOM) tutulur; erişim yalnızca yetkili kişilere. SSL derin incelemede sağlık, bankacılık ve kişisel e-posta kategorileri muaf.
4. Yerel zaman dilimi ve UK yasal tatil takvimine göre bakım pencereleri.
5. Kural seti: `kural_seti.md` · Örnek konfigürasyon: `ornek_config_fortios.conf`.
