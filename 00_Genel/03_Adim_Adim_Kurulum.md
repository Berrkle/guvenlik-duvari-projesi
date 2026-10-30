# 03 — Tüm Şubelere Adım Adım Güvenlik Duvarı Kurulumu

Bu prosedür her birimde aynı sırayla uygulanır. Şubeye özel farklar ilgili klasörün `README.md` dosyasındaki "Şubeye özel kurulum notları" bölümündedir.

## Devreye alma sırası (neden bu sıra?)

| Dalga | Birim | Gerekçe |
|---:|---|---|
| 1 | İstanbul GM | Hub; diğer şubelerin VPN'i ve merkezi log/yönetim buraya bağlanır |
| 2 | Ankara | İkincil hub (felaket kurtarma) |
| 3 | Yazılım Ekibi | Kaynak kod en kritik varlık |
| 4 | Ar-Ge | Fikri mülkiyet |
| 5 | Londra | Uzak lokasyon, uzaktan kurulum + yerel el desteği |
| 6 | Akademik Şube | En büyük ve en riskli değişiklik; dönem arası tatilde yapılır |

---

## Faz A — Hazırlık

**Adım 1. Envanter ve gereksinim toplama**
- Mevcut ağ şeması, IP blokları, sunucu listesi, dışa açık servisler.
- Uygulama envanteri: hangi kullanıcı grubu hangi uygulamayı kullanıyor? (İK, finans, ERP sahipleriyle görüşme.)
- Mevcut firewall varsa kural dökümü; son 90 günde hiç eşleşmeyen kurallar tespit edilir (yeni cihaza taşınmaz).

**Adım 2. Tasarım onayı**
- IP/VLAN planı, zone tanımları, kural seti taslağı, HA ve hat yapısı dokümante edilir.
- Değişiklik Danışma Kurulu (CAB) onayı alınır. Geri dönüş (rollback) planı yazılır.

**Adım 3. Tedarik ve lisans**
- Cihaz çifti (HA), güvenlik abonelikleri (IPS, AV, web filtre, uygulama kontrolü, sandbox), destek sözleşmesi.
- Merkezi yönetim ve log lisansları (FortiManager/FortiAnalyzer, Panorama).

## Faz B — Fiziksel kurulum

**Adım 4. Kabin, enerji, kablolama**
- İki cihaz ayrı güç kaynaklarına (A/B beslemesi, UPS) bağlanır.
- HA kalp atışı (heartbeat) için iki ayrı kablo, cihazlar arası doğrudan.
- WAN hatları farklı fiziksel portlara, LAN tarafı çekirdek anahtara LACP ile.

**Adım 5. İlk erişim ve sertleştirme (hardening)**
- Üreticinin önerdiği güncel kararlı firmware yüklenir (en yeni değil, en kararlı ve güvenlik yaması içeren).
- Varsayılan yönetici hesabı yeniden adlandırılır/devre dışı bırakılır; kişiye özel yönetici hesapları, MFA, RADIUS/TACACS+ ile kimlik doğrulama.
- Yönetim arayüzü yalnızca MGMT VLAN'dan; internet tarafındaki arayüzlerde HTTPS/SSH yönetimi kapalı.
- Güçlü şifreleme (TLS 1.2+), oturum zaman aşımı 10 dk, başarısız giriş kilitleme.
- NTP (iç zaman sunucuları), DNS, SNMPv3 (v1/v2c kapalı), syslog.
- Konfigürasyon yedeği otomatik ve şifreli.

## Faz C — Mantıksal yapılandırma

**Adım 6. Arayüzler, VLAN'lar, zone'lar**
- `01_Sirket_Yapisi_ve_Topoloji.md` dosyasındaki VLAN şablonuna göre alt arayüzler oluşturulur ve zone'lara atanır.

**Adım 7. WAN ve SD-WAN**
- İki hat SD-WAN üyesi yapılır. Sağlık kontrolü (ping/HTTP ile performans SLA): gecikme, jitter, paket kaybı.
- Ses/video en düşük gecikmeli hatta, toplu veri en ucuz/en boş hatta yönlendirilir.

**Adım 8. Nesneler (objects)**
- Adres nesneleri ve grupları anlamlı adlarla (`IST_PERSONEL_NET`, `AKD_OGRENCI_NET`), servis nesneleri, zaman takvimleri (mesai, sınav saatleri), FQDN ve harici tehdit listeleri.

**Adım 9. Güvenlik politikaları (kural seti)**
- Önce en altta **"tümünü reddet ve logla"** kuralı yazılır.
- Kurallar yukarıdan aşağıya: yönetim → altyapı (DNS, NTP) → sunuculara erişim → internet erişimi → misafir.
- Özel kurallar genel kuralların üstünde; her kuralda açıklama, sahip, oluşturma ve gözden geçirme tarihi.
- Şube kural setleri: her klasördeki `kural_seti.md`.

**Adım 10. Güvenlik profilleri**
- IPS: kritik ve yüksek imzalarda engelle, orta seviyede izle.
- Antivirüs + sandbox (bilinmeyen dosyalar için).
- Web filtre: kötü amaçlı, phishing, kumar, yetişkin içerik, proxy/anonimleştirici kategorileri engellenir.
- Uygulama kontrolü: P2P/torrent, uzaktan erişim araçları (izinsiz), şifreli tünelleme araçları engellenir.
- DNS filtreleme: botnet C2 ve yeni kaydedilmiş alan adları engellenir.

**Adım 11. SSL/TLS inceleme**
- Kurumsal CA sertifikası MDM/Group Policy ile cihazlara dağıtılır.
- Personel trafiğinde derin inceleme; bankacılık, sağlık ve kişisel veri kategorileri KVKK gereği hariç tutulur.
- Öğrenci trafiğinde yalnızca sertifika incelemesi (SNI tabanlı), derin inceleme yok (gizlilik + performans).

**Adım 12. NAT ve yayınlanan servisler**
- Çıkış için kaynak NAT (SD-WAN arayüzü).
- Dışa açık servisler yalnızca DMZ'deki reverse proxy/WAF üzerinden (hedef NAT / VIP); iç sunucu asla doğrudan yayınlanmaz.

**Adım 13. VPN**
- Şubeden hub'a IPsec IKEv2, AES-256-GCM, PFS (DH grup 20 veya üzeri), sertifika tabanlı kimlik doğrulama.
- Uzaktan erişim: IPsec/IKEv2 istemci VPN veya ZTNA; her durumda MFA ve cihaz uyumluluk kontrolü.

**Adım 14. Yüksek erişilebilirlik (HA)**
- Aktif-pasif, oturum senkronizasyonu açık, izlenen arayüzler (WAN ve LAN uplink) tanımlı.
- Failover testi: aktif cihazın gücü kesilir; ses görüşmesi ve dosya kopyalama kesintisiz devam etmeli.

## Faz D — Doğrulama ve canlıya geçiş

**Adım 15. Test ve pilot**
- Kural testleri: her kural için "izin verilmeli" ve "engellenmeli" senaryosu (ör. öğrenci VLAN'ından ERP'ye erişim engellenmeli).
- Zafiyet taraması (dış IP'lere), port taraması (nmap) ile beklenmeyen açık port kontrolü.
- EICAR test dosyası ile AV, test URL'leri ile web filtre doğrulaması.
- Pilot grup (her departmandan 5–10 kişi) ile 1 hafta.

**Adım 16. Canlıya geçiş, dokümantasyon, devir**
- Bakım penceresinde geçiş; geri dönüş için eski cihaz 2 hafta hazır bekler.
- Loglar FortiAnalyzer/Panorama ve SIEM'e akıyor mu kontrol edilir.
- As-built doküman, kural seti, yedek konfigürasyon, şifre kasası kaydı.
- İlk 30 gün yoğun izleme; 30. günde kural optimizasyonu (kullanılmayan/gölgelenen kurallar).

---

## Kontrol listesi (her birim için doldurulur)

| # | Kontrol | Tamam |
|---:|---|:-:|
| 1 | Firmware güncel ve kararlı sürüm | ☐ |
| 2 | Varsayılan yönetici hesabı kapalı, MFA aktif | ☐ |
| 3 | Yönetim yalnızca MGMT VLAN'dan | ☐ |
| 4 | En alttaki "tümünü reddet + logla" kuralı mevcut | ☐ |
| 5 | Her kuralda açıklama, sahip, gözden geçirme tarihi | ☐ |
| 6 | IPS/AV/web filtre/uygulama kontrolü profilleri bağlı | ☐ |
| 7 | SSL inceleme istisnaları (KVKK) tanımlı | ☐ |
| 8 | HA failover testi başarılı | ☐ |
| 9 | Loglar merkezi sisteme ve SIEM'e akıyor | ☐ |
| 10 | Konfigürasyon yedeği alındı ve şifreli saklanıyor | ☐ |
| 11 | Dış zafiyet taraması temiz | ☐ |
| 12 | As-built dokümantasyon teslim edildi | ☐ |
