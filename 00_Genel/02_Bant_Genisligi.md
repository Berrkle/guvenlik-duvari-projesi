# 02 — Bant Genişliği Tanımlama

Bant genişliği iki ayrı seviyede tanımlanır:

1. **Dış hat (WAN) kapasitesi:** Her birime ne kadarlık internet hattı alınacak?
2. **İç dağıtım (QoS / trafik şekillendirme):** Bu hattın içinde kim ne kadar garanti ve en fazla ne kadar kullanacak?

## 1. Hesaplama yöntemi

```
Ham ihtiyaç    = Σ ( kullanıcı sayısı × eşzamanlılık oranı × kullanıcı başı ortalama Mbps )
Gerekli        = Ham ihtiyaç × 1,3 (büyüme payı, 3 yıl)  +  servis payı (sunucu, VPN, bulut)
Hat seçimi     = gerekliyi karşılayan bir sonraki standart kademe (100/200/500/1000/2000/5000/10000 Mbps)
Firewall boyutu= Threat Protection (enterprise mix) kapasitesi ≥ 1,5 × gerekli
```

Neden *threat protection* değeri? Datasheet'in en üstündeki "firewall throughput" yalnızca durum denetimli paket iletimidir. IPS, antivirüs, uygulama kontrolü ve loglama açıldığında gerçek kapasite çok daha düşüktür. Örneğin FortiGate 200G'nin firewall throughput değeri 39 Gbps iken threat protection değeri 6 Gbps'tir. Boyutlandırma her zaman tüm güvenlik özellikleri açıkken ölçülen değerle yapılır; SSL derin inceleme açılınca bu değer daha da düşer, 1,5 katsayısı bunun için konmuştur.

## 2. Varsayımlar

| Birim | Kullanıcı | Eşzamanlılık | Kişi başı ort. | Servis payı | Gerekçe |
|---|---:|---:|---:|---:|---|
| İstanbul GM | 325 | %75 | 4 Mbps | 500 Mbps | Veri merkezi + tüm şubelerin VPN hub'ı |
| Ankara | 150 | %75 | 3 Mbps | 50 Mbps | Ofis işleri, video konferans |
| Londra | 80 | %75 | 3 Mbps | 50 Mbps | Ofis işleri, M365 |
| Akademik — öğrenci | 10.000 | %35 | 1,5 Mbps | – | Aynı anda kampüste ve çevrimiçi olan öğrenci oranı |
| Akademik — akademik/idari/IT | 1.040 | %70 | 3 Mbps | 1.000 Mbps | LMS, sınav sistemi, e-kütüphane, web |
| Yazılım | 150 | %90 | 8 Mbps | 500 Mbps | Git, konteyner imajları, paket indirmeleri, CI/CD bulut trafiği |
| Ar-Ge | 70 | %90 | 10 Mbps | 100 Mbps | Büyük veri setleri, GPU bulut erişimi |

## 3. Sonuçlar (`bant_genisligi_hesapla.py` çıktısı)

| Birim | Ham | Gerekli | Seçilen hat | Yedek hat | FW min. threat prot. |
|---|---:|---:|---|---|---:|
| İstanbul GM | 975 Mbps | **1.768 Mbps** | 2 Gbps fiber (Metro Ethernet) | 1 Gbps, farklı operatör | 2,65 Gbps |
| Ankara | 338 Mbps | **489 Mbps** | 500 Mbps fiber | 200 Mbps, farklı operatör | 0,73 Gbps |
| Londra | 180 Mbps | **284 Mbps** | 500 Mbps leased line | 200 Mbps FTTP | 0,43 Gbps |
| Akademik Şube | 7.434 Mbps | **10.664 Mbps** | 2 × 10 Gbps, iki operatör, aktif-aktif | (aktif-aktif yapı kendi yedeği) | 16 Gbps |
| Yazılım | 1.080 Mbps | **1.904 Mbps** | 2 Gbps fiber | 1 Gbps, farklı operatör | 2,86 Gbps |
| Ar-Ge | 630 Mbps | **919 Mbps** | 1 Gbps fiber | 500 Mbps, farklı operatör | 1,38 Gbps |

Notlar:
- Akademik Şube ihtiyacı tek bir 10 Gbps hattı aşıyor (~10,7 Gbps). İki 10 Gbps hat aktif-aktif çalışır; biri koparsa kalan 10 Gbps, QoS sayesinde öğrenci trafiği kısılarak kritik servisleri taşır.
- Yazılım Ekibi hattı (%5 boşluk) ve Ankara hattı (%2 boşluk) sınırda. Devreye alındıktan sonraki ilk 3 ay NetFlow ölçümleri izlenir; %80 sürekli kullanım aşılırsa bir üst kademeye geçilir.
- Şubeler arası VPN trafiği bu hatların içindedir; İstanbul'un servis payı bunun için yüksek tutulmuştur.

## 4. İç dağıtım: QoS politikası

### 4.1 Trafik sınıfları (tüm birimlerde ortak)

| Öncelik | Sınıf | Örnek uygulamalar | DSCP |
|---:|---|---|---|
| 1 | Ses | SIP/RTP, Teams/Zoom ses | EF (46) |
| 2 | Etkileşimli video | Teams/Zoom/Meet video | AF41 (34) |
| 3 | İş kritik | ERP, AD, LMS, sınav sistemi, Git | AF31 (26) |
| 4 | Genel iş | Web, e-posta, SaaS | AF21 (18) |
| 5 | Toplu veri | Yedekleme, güncellemeler, büyük indirmeler | AF11 (10) |
| 6 | Düşük öncelik (scavenger) | Video akış, sosyal medya, misafir | CS1 (8) |

### 4.2 Birim bazlı garanti / üst limitler

| Birim | Grup | Garanti | Üst limit | Kişi başı limit |
|---|---|---:|---:|---|
| İstanbul GM | Ses + video | %20 | %40 | – |
| | Veri merkezi / VPN hub | %25 | %60 | – |
| | Personel | %35 | %90 | – |
| | Misafir | – | %5 | 5 Mbps |
| Ankara / Londra | Ses + video | %25 | %50 | – |
| | Personel | %60 | %95 | – |
| | Misafir | – | %5 | 5 Mbps |
| Akademik Şube | Sunucular (LMS, sınav, web) | %15 | %40 | – |
| | Akademisyen | %20 | %60 | 50 Mbps |
| | İdari personel | %15 | %50 | 30 Mbps |
| | Öğrenci | %40 | %80 | 20 Mbps indirme / 5 Mbps yükleme |
| | Laboratuvar | %5 | %20 | – |
| | Misafir / eduroam misafir | – | %5 | 5 Mbps |
| Yazılım | CI/CD + Git | %40 | %80 | – |
| | Geliştirici | %40 | %90 | 100 Mbps |
| | Ses + video | %15 | %30 | – |
| Ar-Ge | Veri/GPU aktarımı | %40 | %80 | – |
| | Araştırmacı | %40 | %90 | 100 Mbps |

Kurallar:
- **Sınav saatlerinde** (takvim nesnesi) Akademik Şube'de sınav VLAN'ı ve LMS en yüksek önceliğe çıkar, öğrenci üst limiti %60'a iner.
- **Yedekleme** gece 01:00–06:00 arasına zamanlanır; gündüz toplu veri sınıfı %10 ile sınırlıdır.
- Toplam garanti hiçbir birimde %100'ü aşmaz.

## 5. Ölçüm ve doğrulama

- Devreye almadan önce: her hatta `iperf3` ile kapasite testi, operatör SLA'sının doğrulanması.
- Devreye aldıktan sonra: NetFlow/IPFIX ile uygulama bazlı tüketim, 95. yüzdelik (95th percentile) kullanım raporu.
- Eşik: bir hat 15 dakika boyunca %85'in üzerinde kalırsa NOC'a uyarı; ayda 5 günden fazla tekrarlanırsa kapasite artışı talebi.
