# 06 — Ar-Ge Ekibi

## Kadro

| Grup | Sayı |
|---|---:|
| Araştırmacı (Ar-Ge) | 55 |
| Laboratuvar sorumlusu (Ar-Ge) | 5 |
| Teknik destek / IT | 10 |
| Personel (idari) | – (İstanbul GM'den hizmet) |
| Öğrenci | – (stajyerler misafir değil, ayrı "Ar-Ge Stajyer" AD grubuyla) |
| **Toplam kullanıcı** | **70** (60 Ar-Ge + 10 teknik) |

Konum: Ankara teknokent binası. **En kritik varlık:** henüz patenti alınmamış tasarımlar, prototip verileri, araştırma veri setleri, eğitilmiş modeller. Şirketin en sıkı güvenlik politikası buradadır.

## Bant genişliği

| Kalem | Değer |
|---|---|
| Hesap | 70 × %90 × 10 Mbps = 630 Mbps → × 1,3 = 819 Mbps + 100 Mbps (GPU bulut, veri seti aktarımı) |
| **Gerekli** | **~919 Mbps** |
| Birincil hat | 1 Gbps fiber |
| Yedek hat | 500 Mbps, farklı operatör |
| Firewall minimum threat prevention | 1,38 Gbps |

### İç dağıtım

| Grup | Garanti | Üst limit | Kişi başı |
|---|---:|---:|---|
| Veri / GPU aktarımı (veri transfer sunucusu üzerinden) | %40 | %80 | – |
| Araştırmacı | %40 | %90 | 100 Mbps |
| Ses + video | %15 | %30 | – |
| İzole laboratuvar | 0 | 0 | İnternete kapalı |

## Top 5 güvenlik duvarı önerisi

| Sıra | Model | Threat prevention / protection | Değerlendirme |
|---:|---|---|---|
| **1** | **Palo Alto PA-1420** (HA çift) | ~6,0–6,2 Gbps; ~1,2–1,4 M oturum | **Seçildi.** Gereksinimin ~6,5 katı → tam SSL inceleme + DLP + sandbox hepsi açıkken bile rahat; Yazılım Ekibi ile aynı Panorama |
| 2 | Fortinet FortiGate 120G | 2,8 Gbps | Kapasite yeterli; tek üretici olurdu |
| 3 | Check Point Quantum Force 9100 | 6,5 Gbps | Güçlü tehdit önleme; maliyet ve ayrı yönetim |
| 4 | Cisco Secure Firewall 1240 | FW+AVC 18 Gbps (IPS açıkken daha düşük) | Kompakt; DLP için ek ürün gerekir |
| 5 | Sophos XGS 118 | 3,25 Gbps | Uygun maliyet; fikri mülkiyet koruması için uygulama görünürlüğü daha sınırlı |

## Neden Palo Alto PA-1420?

- 70 kişi için büyük görünebilir; ama Ar-Ge'de **tüm güvenlik özellikleri aynı anda açık** (derin SSL inceleme, WildFire sandbox, dosya engelleme, DLP, DNS güvenliği). Bunlar kapasiteyi en çok düşüren özelliklerdir.
- Yazılım Ekibi ile aynı üretici → aynı Panorama, aynı profil grupları, ekip tek eğitimle iki birimi yönetir.
- PA-1410 (4,5 Gbps) de yeterdi; 1420 büyüyen GPU/veri aktarımı ve daha fazla oturum kapasitesi için seçildi.

## VLAN'lar (Ar-Ge'ye özel)

| VLAN | Ad | Ağ | Not |
|---:|---|---|---|
| 10 | MGMT | 10.250.60.0/24 | |
| 20 | ARASTIRMA | 10.60.20.0/24 | Araştırmacı iş istasyonları (kurumsal, şifreli disk) |
| 30 | IT | 10.60.30.0/24 | |
| 40 | VERI_GPU | 10.60.40.0/24 | Yerel GPU sunucuları, veri deposu |
| 45 | TRANSFER | 10.60.45.0/28 | Veri transfer sunucusu (içeri/dışarı tek kapı, kontrollü) |
| 100 | LAB_IZOLE | 10.60.100.0/24 | Prototip ve test cihazları — **internete ve diğer ağlara kapalı** |
| 50 | VOIP | 10.60.50.0/24 | |
| 70 | MISAFIR | 10.60.70.0/24 | Ziyaretçi ve proje ortakları; Ar-Ge ağlarına sıfır erişim |

## Şubeye özel kurulum notları

1. Dalga 4. Yazılım Ekibi ile aynı Panorama cihaz grubuna eklenir; farklı olan yalnız kural seti.
2. **Varsayılan internet erişimi kapalı:** Araştırmacılar internete yalnızca izin listesindeki kategori/sitelere (akademik yayınlar, standart kuruluşları, onaylı SaaS) çıkar. Yeni site talebi ticket ile.
3. **İzole laboratuvar:** Hiçbir ağa rota yok. Laboratuvara veri yalnızca TRANSFER sunucusu üzerinden, AV taramasından geçirilerek ve iki kişi onayıyla (dört göz ilkesi) girer/çıkar.
4. **Ankara Ofisi ile doğrudan bağlantı yoktur** (aynı şehirde olsalar bile). İhtiyaç olursa İstanbul hub üzerinden ve iki güvenlik duvarından geçerek.
5. Kural seti: `kural_seti.md` · Örnek konfigürasyon: `ornek_config_panos.txt`.
