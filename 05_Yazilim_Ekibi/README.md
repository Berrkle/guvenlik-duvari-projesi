# 05 — Yazılım Ekibi

## Kadro

| Grup | Sayı |
|---|---:|
| Geliştirici | 120 |
| DevOps / bulut operasyonları | 15 |
| QA / test + teknik destek | 15 |
| Personel (idari) | – (İK/finans hizmetleri İstanbul GM'den) |
| Öğrenci | – |
| Ar-Ge | – |
| **Toplam kullanıcı (yazılım/teknik)** | **150** |

Konum: İstanbul teknopark binası (GM'den ayrı lokasyon). **En kritik varlık:** kaynak kod, CI/CD hattı, üretim (production) ortamına erişim anahtarları.

## Bant genişliği

| Kalem | Değer |
|---|---|
| Hesap | 150 × %90 × 8 Mbps = 1.080 Mbps → × 1,3 = 1.404 Mbps + 500 Mbps (CI/CD → bulut, konteyner imajları) |
| **Gerekli** | **~1.904 Mbps** |
| Birincil hat | 2 Gbps fiber |
| Yedek hat | 1 Gbps, farklı operatör |
| Firewall minimum threat prevention | 2,86 Gbps |

> Sınırda (%5 boşluk). Konteyner imajları için yerel önbellek (registry mirror / Artifactory) kurulup tekrarlı indirmeler azaltılır; 3 ay sonra ölçüm.

### Kampüs içi dağıtım

| Grup | Garanti | Üst limit | Kişi başı |
|---|---:|---:|---|
| CI/CD + Git | %40 | %80 | – |
| Geliştirici | %40 | %90 | 100 Mbps |
| Ses + video | %15 | %30 | – |

## Top 5 güvenlik duvarı önerisi

| Sıra | Model | Threat prevention / protection | Değerlendirme |
|---:|---|---|---|
| **1** | **Palo Alto PA-3410** (HA çift) | 7,5 Gbps; 1,4 M oturum | **Seçildi.** App-ID ile Git/SSH/registry trafiğini uygulama seviyesinde ayırır; dosya engelleme ve DLP; ikinci üretici ile derinlemesine savunma |
| 2 | Fortinet FortiGate 200G | 6 Gbps | Kapasite yeterli; tek üretici olurdu (derinlemesine savunma kaybı) |
| 3 | Check Point Quantum Force 9300 | 10,5 Gbps | En yüksek kapasite; maliyet ve üçüncü bir yönetim aracı |
| 4 | Cisco Secure Firewall 3120 | FW+AVC 21 Gbps (IPS açıkken daha düşük) | Güçlü donanım; yönetim karmaşıklığı |
| 5 | Sophos XGS 138 sınıfı | Datasheet'ten doğrulanmalı | Bu kritiklikte segment için uygulama görünürlüğü daha sınırlı |

## Neden Palo Alto PA-3410?

- **App-ID:** "port 443'e izin ver" yerine "github, npm, pypi, docker-registry uygulamalarına izin ver" diyebiliriz; aynı porttan geçen izinsiz uygulamalar (kişisel bulut depolama, dosya paylaşım siteleri) engellenir.
- **Veri sızıntısı önleme:** Kaynak kod ve anahtar dosyalarının (`.pem`, `.key`, büyük `.zip`/`.tar`) izinsiz hedeflere yüklenmesi dosya engelleme profiliyle durdurulur.
- **SSL derin inceleme kapasitesi:** 7,5 Gbps tehdit önleme, derin inceleme açıkken 2 Gbps hattı rahat taşır.
- **İkinci üretici:** Çevre katmanındaki Fortinet'te bir açık çıksa bile kaynak kodu koruyan katman farklı bir kod tabanıdır.

## VLAN'lar (Yazılım Ekibi'ne özel)

| VLAN | Ad | Ağ | Not |
|---:|---|---|---|
| 10 | MGMT | 10.250.50.0/24 | |
| 20 | DEV | 10.50.20.0/23 | Geliştirici dizüstü/iş istasyonları |
| 25 | DEVOPS | 10.50.25.0/24 | DevOps mühendisleri |
| 30 | QA | 10.50.30.0/24 | Test ekibi, test cihazları |
| 40 | CICD | 10.50.40.0/24 | Build sunucuları, runner'lar, artifact deposu |
| 45 | STAGING | 10.50.45.0/24 | Ön üretim ortamı |
| 50 | VOIP | 10.50.50.0/24 | |
| 60 | BASTION | 10.50.60.0/28 | Üretime tek giriş noktası (PAM + MFA) |
| 70 | MISAFIR | 10.50.70.0/24 | |

## Şubeye özel kurulum notları

1. Dalga 3. Panorama (merkezi Palo Alto yönetimi) İstanbul veri merkezinde kurulur; logları SIEM'e iletir.
2. **Üretim ortamına erişim** yalnızca BASTION üzerinden, PAM (ayrıcalıklı erişim yönetimi) oturum kaydı ve MFA ile. DEV/QA'dan üretime doğrudan yol yok.
3. Bulut (AWS/Azure) erişimi: CI/CD runner'ları ile bulut VPC/VNet arasında site-to-site IPsec; konsol erişimi SSO + MFA.
4. **User-ID:** Kurallar IP'ye değil AD gruplarına yazılır (`YZL-Gelistirici`, `YZL-DevOps`). İşten ayrılan kişi AD'den çıkınca erişimi otomatik biter.
5. Kural seti: `kural_seti.md` · Örnek konfigürasyon: `ornek_config_panos.txt`.
