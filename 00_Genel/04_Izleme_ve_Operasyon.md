# 04 — İzleme (Monitoring) ve Operasyon Modeli

Profesyonel dünyada güvenlik duvarını izlemek iki ayağa dayanır: **sistematik taraf** (araçlar, otomasyon, uyarılar) ve **insani taraf** (ekipler, roller, süreçler). Araçlar veriyi toplar; kararı ve müdahaleyi insanlar verir. Biri olmadan diğeri işe yaramaz: insansız araç, okunmayan binlerce uyarı demektir; araçsız insan ise kör kalır.

---

## 1. Sistematik taraf

### 1.1 Mimari

```
[FortiGate'ler] ──► FortiManager (konfigürasyon, politika, firmware)
       │
       └────────► FortiAnalyzer (log, rapor) ─┐
[Palo Alto'lar] ──► Panorama (yönetim + log) ──┼──► SIEM (korelasyon, uyarı) ──► SOAR / Ticket ──► SOC analisti
[Switch/AP/Sunucu] ─ syslog/SNMP ──────────────┘          │
[NetFlow/IPFIX] ──► Akış analizi (ntopng/PRTG) ───────────┘
[SNMPv3] ──► Zabbix ──► Grafana panoları ──► NOC ekranı
```

### 1.2 Katmanlar ve önerilen araçlar

| Katman | Ne izlenir? | Kurumsal araç | Açık kaynak / öğrenci projesi alternatifi |
|---|---|---|---|
| Merkezi yönetim | Konfigürasyon sapması, politika paketleri, firmware | FortiManager, Panorama | Ansible + Git (konfigürasyon yedekleri) |
| Log ve rapor | Trafik, tehdit, VPN, yönetici işlemleri | FortiAnalyzer, Panorama / Strata Logging Service | Graylog |
| SIEM | Olay korelasyonu, uyarı üretimi | Splunk Enterprise Security, Microsoft Sentinel, IBM QRadar | Wazuh (+ OpenSearch) |
| SOAR | Otomatik müdahale (IP engelle, kullanıcıyı karantinaya al) | FortiSOAR, Cortex XSOAR, Splunk SOAR | Shuffle, TheHive + Cortex |
| Performans / sağlık | CPU, bellek, oturum sayısı, HA durumu, hat kullanımı | PRTG, SolarWinds | Zabbix + Grafana, LibreNMS |
| Akış analizi | Uygulama/kullanıcı bazlı bant tüketimi | Kentik, Plixer Scrutinizer | ntopng, ElastiFlow |
| Konfigürasyon denetimi | Gölgelenen/kullanılmayan kurallar, uyum | Tufin, AlgoSec, FireMon | Kural kullanım raporları + manuel inceleme |
| Zafiyet | Dış IP'lerde açık port ve servis | Tenable, Qualys | OpenVAS/Greenbone, nmap |

**Bu proje için seçim:** FortiManager + FortiAnalyzer + Panorama (üretici araçları) → **Wazuh SIEM** (ücretsiz, sunumda canlı gösterilebilir) → Zabbix + Grafana (sağlık panoları). Kurumsal ölçekte bütçe varsa Wazuh yerine Splunk ES veya Microsoft Sentinel.

### 1.3 Uyarı eşikleri

| Olay | Eşik | Önem | İlk müdahale |
|---|---|---|---|
| Firewall CPU | > %80, 5 dk | Orta | NOC: en çok oturum açan kaynakları incele |
| Oturum tablosu | > %80 kapasite | Yüksek | DDoS / tarama şüphesi, SOC'a aktar |
| WAN hat kullanımı | > %85, 15 dk | Orta | QoS kontrolü, kapasite kaydı aç |
| HA failover | Her olay | Yüksek | Nedenini bul; donanım/arayüz arızası mı? |
| VPN tüneli düştü | > 2 dk | Yüksek | Operatör/hat kontrolü, yedek tünel aktif mi? |
| IPS kritik imza | Her olay | Kritik | SOC L1 doğrular, gerekirse cihazı izole et |
| Botnet C2 / kötü amaçlı DNS | Her olay | Kritik | Cihazı karantina VLAN'ına al (SOAR otomatik) |
| Yönetici girişi başarısız | ≥ 5 deneme / 10 dk | Yüksek | Hesabı kilitle, kaynak IP'yi incele |
| Mesai dışı konfigürasyon değişikliği | Onaylı değişiklik kaydı yoksa | Kritik | Değişikliği geri al, hesabı askıya al, olay müdahalesi başlat |
| Ar-Ge/Yazılım'dan büyük dışa veri aktarımı | > 2 GB / saat, izin listesi dışı | Yüksek | DLP incelemesi, kullanıcı yöneticisine bilgi |
| Log akışı durdu | > 10 dk log yok | Yüksek | Log kesintisi saldırı işareti olabilir; cihazı kontrol et |

### 1.4 Panolar

- **NOC panosu:** Hat kullanımları, HA durumu, CPU/oturum, VPN tünelleri — tüm birimler tek ekranda, yeşil/sarı/kırmızı.
- **SOC panosu:** Son 24 saat tehditler, en çok engellenen kaynaklar, en çok tetiklenen IPS imzaları, coğrafi dağılım.
- **Yönetim panosu (aylık):** Engellenen saldırı sayısı, ortalama tespit ve müdahale süreleri, kapasite trendi, kural sayısı ve temizlik oranı.

### 1.5 Log saklama

| Log türü | Sıcak (hızlı arama) | Arşiv | Dayanak |
|---|---|---|---|
| Akademik Şube öğrenci/misafir erişim kayıtları + DHCP IP dağıtım kayıtları | 90 gün | **2 yıl**, değiştirilemez arşiv + hash/zaman damgası | 5651 / İnternet Toplu Kullanım Sağlayıcıları Yönetmeliği |
| Diğer birimler trafik logları | 90 gün | 1 yıl | Kurum politikası, ISO 27001 |
| Tehdit ve yönetici işlem logları | 180 gün | 2 yıl | Olay incelemesi |
| Londra logları | 90 gün | 1 yıl, UK'de veya onaylı bölgede | UK GDPR |

---

## 2. İnsani taraf

### 2.1 Ekipler ve roller

| Ekip / rol | Sorumluluk | Bu şirkette |
|---|---|---|
| **NOC** (Network Operations Center) | Erişilebilirlik ve performans: hat, cihaz sağlığı, kapasite | 6 kişi, 7/24 vardiya (3 vardiya × 2 kişi) |
| **SOC L1** (Analist) | Uyarıları ilk değerlendirme, yanlış alarm ayıklama, eskalasyon | 6 kişi, 7/24 vardiya |
| **SOC L2** (Olay müdahale) | Doğrulanmış olayları inceleme, sınırlama (containment) | 3 kişi, mesai + nöbet |
| **SOC L3** (Tehdit avcısı / uzman) | İleri analiz, adli inceleme, yeni tespit kuralları | 2 kişi |
| **Firewall / ağ güvenliği mühendisi** | Kural değişikliklerini uygulama, optimizasyon | 3 kişi |
| **CISO / Bilgi güvenliği yöneticisi** | Politika, risk kabulü, üst yönetime raporlama | 1 kişi |
| **Kural sahipleri** (departman yöneticileri) | Kendi kurallarının gerekliliğini 3 ayda bir onaylama | Her departmandan 1 kişi |

**Alternatif (bütçe kısıtlıysa):** Gece ve hafta sonu SOC L1 hizmeti bir MSSP'den (yönetilen güvenlik hizmet sağlayıcısı) alınır; şirket içi ekip 8/5 çalışır ve nöbet tutar.

### 2.2 Süreçler

1. **Değişiklik yönetimi (Change Management):** Kural ekleme/silme talebi ticket ile açılır → güvenlik mühendisi risk değerlendirir → CAB onaylar → bakım penceresinde uygulanır → talep sahibi test eder → kayıt kapanır. Acil değişiklikler sonradan CAB'e raporlanır.
2. **Kural yeniden sertifikasyonu:** 3 ayda bir her kural sahibine "bu kural hâlâ gerekli mi?" sorusu. Cevapsız veya 90 gün eşleşmesi olmayan kurallar devre dışı bırakılır, 30 gün sonra silinir.
3. **Olay müdahalesi (Incident Response):** Hazırlık → Tespit/Analiz → Sınırlama → Temizleme → Kurtarma → Ders çıkarma. Her olay türü için yazılı oyun kitabı (playbook): fidye yazılımı, veri sızıntısı, DDoS, hesap ele geçirme.
4. **Yama yönetimi:** Kritik firewall zafiyetleri (özellikle internetten erişilen VPN/yönetim arayüzlerini etkileyenler) 72 saat içinde, diğerleri aylık bakım penceresinde.
5. **Tatbikat:** 6 ayda bir masa başı tatbikat (tabletop), yılda bir dış sızma testi.
6. **Farkındalık:** Personele yıllık phishing eğitimi ve simülasyonu; öğrencilere dönem başında kabul edilebilir kullanım politikası.

### 2.3 RACI (örnek: yeni kural talebi)

| Aktivite | Talep sahibi | FW mühendisi | CAB | CISO | SOC |
|---|:-:|:-:|:-:|:-:|:-:|
| Talep açma | **R** | I | – | – | – |
| Risk değerlendirme | C | **R** | I | A | C |
| Onay | I | C | **R** | A | – |
| Uygulama | I | **R/A** | I | – | I |
| İzleme | – | C | – | I | **R** |

R: Yapan · A: Hesap veren · C: Danışılan · I: Bilgilendirilen

### 2.4 Başarı ölçütleri (KPI)

| KPI | Hedef |
|---|---|
| Ortalama tespit süresi (MTTD) | < 15 dk (kritik uyarılar) |
| Ortalama müdahale süresi (MTTR) | < 4 saat (kritik olaylar) |
| Firewall erişilebilirliği | ≥ %99,95 |
| Kural değişikliği tamamlama süresi | Standart talep ≤ 3 iş günü |
| Kullanılmayan kural oranı | < %5 |
| Yanlış alarm oranı | < %30 (ayda bir ayarlanır) |
| Kritik yamaların uygulanması | ≤ 72 saat |

---

## 3. Profesyonel dünyada referans çerçeveler

- **NIST Cybersecurity Framework 2.0:** Yönet (Govern) → Tanımla → Koru → Tespit Et → Müdahale Et → Kurtar. Firewall kuralları "Koru", izleme "Tespit Et" fonksiyonuna girer.
- **ISO/IEC 27001:2022 Ek A:** Ağ güvenliği, ağ hizmetlerinin güvenliği, ağların ayrıştırılması, izleme faaliyetleri ve loglama kontrolleri.
- **CIS Controls v8:** Kontrol 4 (güvenli yapılandırma), Kontrol 8 (log yönetimi), Kontrol 13 (ağ izleme ve savunma).
- **MITRE ATT&CK:** SIEM tespit kuralları saldırı tekniklerine eşlenir; hangi tekniklerin görülebildiği bir kapsama haritasıyla takip edilir.

## 4. Bir günün akışı (sunumda anlatılabilecek senaryo)

1. 03:12 — Akademik Şube öğrenci VLAN'ındaki bir cihaz bilinen bir botnet C2 alan adını sorguluyor.
2. FortiGate DNS filtresi sorguyu engeller, log FortiAnalyzer'a ve Wazuh'a gider.
3. Wazuh korelasyon kuralı: "aynı cihazdan 10 dk içinde 3+ C2 sorgusu" → kritik uyarı.
4. SOAR otomatik olarak cihazın MAC adresini NAC üzerinden karantina VLAN'ına taşır ve ticket açar.
5. Gece vardiyasındaki SOC L1 analisti uyarıyı doğrular, olayı L2'ye eskale eder.
6. Sabah L2 analisti cihaz sahibine (öğrenci) BT yardım masası üzerinden ulaşır, cihaz temizlenir, karantina kaldırılır.
7. Haftalık raporda olay "otomatik sınırlandı, MTTD 2 dk" olarak yer alır.
