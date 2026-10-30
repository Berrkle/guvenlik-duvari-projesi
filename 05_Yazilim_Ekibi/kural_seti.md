# Yazılım Ekibi — Kural Seti (Palo Alto PA-3410)

**İlkeler:** Varsayılan reddet · Kurallar AD gruplarına (User-ID) ve uygulamalara (App-ID) yazılır, port numarasına değil · `application-default` servis (uygulama yalnızca standart portunda) · Geliştirme ve üretim tamamen ayrı.
Profil grubu **YZL-Strict** = Antivirüs + Anti-Spyware + Vulnerability Protection + URL Filtering + File Blocking + WildFire (sandbox) + DNS Security.

## A. Altyapı

| # | Kural adı | Kaynak (zone / kullanıcı) | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 1 | Tehdit-EDL-Engel | any / TI harici dinamik listeleri (EDL) | TI EDL / any | any | REDDET | – | Tümü |
| 2 | MGMT-FW | IST_IT_JUMP (Panorama dahil) | FW yönetim | ssl, ssh | İZİN | – | Tümü |
| 3 | AD-DNS | Tüm iç zone'lar | IST_DC (VPN) | kerberos, ldap, dns, ms-ds-smb (DC) | İZİN | YZL-Strict | Tümü |
| 4 | DNS-Dogrudan-Engel | DEV, DEVOPS, QA | internet | dns, dns-over-https, dns-over-tls | REDDET | – | Tümü |

## B. Geliştirme akışı

| # | Kural adı | Kaynak | Hedef | Uygulama / URL | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 10 | Git-SaaS | DEV, DEVOPS, CICD (grup: YZL-Gelistirici, YZL-DevOps) | internet — URL kategorisi `YZL_Git_Allow` (github.com, gitlab.com vb. şirket organizasyonları) | git, ssh (yalnız bu hedeflere), ssl | İZİN | YZL-Strict + SSL decrypt | Tümü |
| 11 | Paket-Depolari | DEV, CICD | URL kategorisi `YZL_Paket_Allow` (npm, PyPI, Maven Central, NuGet, Docker Hub) veya yerel Artifactory | ssl, web-browsing | İZİN | YZL-Strict + SSL decrypt | Tümü |
| 12 | Ic-Artifact-Deposu | DEV, QA, CICD | YZL_ARTIFACTORY | ssl | İZİN | YZL-Strict | Tümü |
| 13 | CICD-Bulut | CICD | Bulut VPC/VNet (IPsec tüneli) | ssl, ssh, kubernetes API | İZİN | YZL-Strict | Tümü |
| 14 | QA-Staging | QA, DEV | STAGING | ssl, web-browsing, ssh (grup: YZL-QA) | İZİN | YZL-Strict | Tümü |
| 15 | Dev-Prod-Dogrudan-Engel | DEV, QA, CICD | Üretim ağları (bulut prod + IST prod) | any | REDDET | – | Tümü |
| 16 | Bastion-Giris | DEVOPS (grup: YZL-Prod-Yetkili, MFA) | BASTION | ssl (PAM web), ssh | İZİN | YZL-Strict | Tümü |
| 17 | Bastion-Prod | BASTION | Üretim ağları | ssh, rdp, ssl | İZİN (oturum kaydı PAM'de) | YZL-Strict | Tümü |

## C. Veri sızıntısı önleme

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 20 | Kisisel-Bulut-Depolama-Engel | Tüm kullanıcı zone'ları | internet | dropbox, google-drive (kişisel), mega, wetransfer, pastebin vb. | REDDET | – | Tümü |
| 21 | Kurumsal-OneDrive | DEV, DEVOPS, QA | internet | ms-onedrive (şirket kiracısı, tenant restriction ile) | İZİN | YZL-Strict | Tümü |
| 22 | SSH-Bilinmeyen-Hedef-Engel | DEV, DEVOPS | internet | ssh, scp, sftp | REDDET (kural 10 ve 13 dışındaki tüm SSH) | – | Tümü |
| 23 | Tunelleme-Engel | Tüm zone'lar | internet | tor, ngrok, ssh-tunnel, dns tünelleme, izinsiz VPN uygulamaları | REDDET | – | Tümü |

## D. Genel internet

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 30 | M365-Teams | DEV, DEVOPS, QA | Microsoft 365 | ms-office365, ms-teams | İZİN | YZL-Strict (SSL decrypt hariç, Microsoft önerisi) | Tümü |
| 31 | Gelistirici-Web | DEV, DEVOPS, QA | internet | ssl, web-browsing (dokümantasyon, Stack Overflow vb.) | İZİN | YZL-Strict + SSL decrypt (KVKK muafiyetleri) | Tümü |
| 32 | CICD-Diger-Internet-Engel | CICD | internet | any | REDDET (yalnız kural 10–13) | – | Tümü |
| 33 | Misafir-Internet | MISAFIR | internet | ssl, web-browsing | İZİN (5 Mbps) | URL filtre + Anti-Spyware | Tümü (5651) |
| 34 | Misafir-Ic-Engel | MISAFIR | Tüm iç zone'lar | any | REDDET | – | Tümü |

## E. Son kural

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Log |
|---:|---|---|---|---|---|---|
| 999 | Tumunu-Reddet | any | any | any | REDDET | Tümü (PAN-OS varsayılan interzone-default kuralı ayrıca override edilerek loglanır) |

## Dosya engelleme profili (YZL-FileBlock)

| Yön | Dosya türü | Aksiyon |
|---|---|---|
| İndirme | exe, dll, msi, scr, bat, ps1 (izinli paket depoları hariç) | uyar (continue) + WildFire |
| Yükleme | pem, key, p12, pfx, kdbx, büyük arşivler (zip/tar/7z) | izinli hedefler dışında **engelle** |
| Her iki yön | Şifreli arşivler (incelenemeyen) | engelle |
