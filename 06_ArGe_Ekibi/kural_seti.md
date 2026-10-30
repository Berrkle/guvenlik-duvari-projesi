# Ar-Ge Ekibi — Kural Seti (Palo Alto PA-1420)

**İlkeler:** Varsayılan reddet — internete çıkış dahil · İzin listesi (allowlist) yaklaşımı · İzole laboratuvar hiçbir ağa bağlı değil · Tüm veri giriş/çıkışı tek kontrollü kapıdan (TRANSFER) · Kurallar AD gruplarına yazılır.
Profil grubu **ARG-Max** = Antivirüs + Anti-Spyware (strict) + Vulnerability Protection (strict) + URL Filtering + File Blocking (strict) + WildFire + DNS Security + Enterprise DLP (varsa).

## A. Altyapı

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 1 | Tehdit-EDL-Engel | any / TI EDL | TI EDL / any | any | REDDET | – | Tümü |
| 2 | MGMT-FW | IST_IT_JUMP (Panorama dahil) | FW yönetim | ssl, ssh | İZİN | – | Tümü |
| 3 | AD-DNS | ARASTIRMA, IT, VERI_GPU | IST_DC (VPN) | kerberos, ldap, dns | İZİN | ARG-Max | Tümü |
| 4 | DNS-Dogrudan-Engel | Tüm iç zone'lar | internet | dns, dns-over-https, dns-over-tls | REDDET | – | Tümü |

## B. İzole laboratuvar

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 10 | Lab-Transfer-Giris | LAB_IZOLE (grup: ARG-Lab-Sorumlu) | ARG_TRANSFER | sftp (onaylı oturumda) | İZİN (takvim: mesai, dört göz onayı) | ARG-Max | Tümü |
| 11 | Lab-Her-Sey-Engel | LAB_IZOLE | any | any | REDDET | – | Tümü |
| 12 | Diger-Lab-Engel | any | LAB_IZOLE | any | REDDET | – | Tümü |

## C. Araştırma ve veri

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 20 | Arastirma-GPU-Veri | ARASTIRMA (grup: ARG-Arastirmaci) | VERI_GPU | ssh, jupyter, ssl, ms-ds-smb | İZİN | ARG-Max | Tümü |
| 21 | Arastirma-Transfer | ARASTIRMA | ARG_TRANSFER | ssl, sftp | İZİN | ARG-Max | Tümü |
| 22 | Transfer-Bulut-GPU | ARG_TRANSFER | Bulut GPU ortamı (IPsec tüneli) | ssl, ssh, sftp | İZİN | ARG-Max | Tümü |
| 23 | Transfer-Onayli-Disi | ARG_TRANSFER | internet — URL kategorisi `ARG_Veri_Ortak_Allow` (proje ortağı üniversite/kurum veri portalları) | ssl | İZİN | ARG-Max + SSL decrypt + DLP | Tümü |
| 24 | VeriGPU-Internet-Engel | VERI_GPU | internet | any | REDDET (güncellemeler iç depo üzerinden) | – | Tümü |
| 25 | VeriGPU-Ic-Depo | VERI_GPU | IST_GUNCELLEME_DEPOSU (VPN) | ssl | İZİN | ARG-Max | Tümü |

## D. İnternet (izin listesi)

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 30 | M365-Teams | ARASTIRMA, IT | Microsoft 365 | ms-office365, ms-teams | İZİN (tenant restriction: yalnızca şirket kiracısı) | ARG-Max (SSL decrypt hariç) | Tümü |
| 31 | Akademik-Kaynaklar | ARASTIRMA | URL kategorisi `ARG_Akademik_Allow` (IEEE, ACM, arXiv, Scopus, Web of Science, standart kuruluşları, patent veritabanları) | ssl, web-browsing | İZİN | ARG-Max + SSL decrypt | Tümü |
| 32 | Arama-Motorlari | ARASTIRMA | search-engines kategorisi | ssl, web-browsing | İZİN (yükleme yok, yalnızca okuma) | ARG-Max + SSL decrypt + dosya yükleme engeli | Tümü |
| 33 | Kisisel-Bulut-ve-Paylasim-Engel | Tüm zone'lar | internet | dropbox, google-drive, mega, wetransfer, pastebin, kişisel e-posta | REDDET | – | Tümü |
| 34 | YZ-Sohbet-Uygulamalari | ARASTIRMA | Onaylı kurumsal YZ hizmeti (şirket hesabı) | ssl | İZİN (yalnız kurumsal kiracı); diğer genel YZ sohbet siteleri REDDET | ARG-Max + DLP | Tümü |
| 35 | Tunelleme-Engel | Tüm zone'lar | internet | tor, ngrok, ssh (izinsiz), izinsiz VPN uygulamaları | REDDET | – | Tümü |
| 36 | Arastirma-Diger-Internet-Engel | ARASTIRMA | internet | any | REDDET (izin listesi dışı her şey) | – | Tümü |

## E. Misafir ve son kural

| # | Kural adı | Kaynak | Hedef | Uygulama | Aksiyon | Profil | Log |
|---:|---|---|---|---|---|---|---|
| 40 | Misafir-Internet | MISAFIR | internet | ssl, web-browsing | İZİN (5 Mbps) | URL filtre + Anti-Spyware | Tümü (5651) |
| 41 | Misafir-Ic-Engel | MISAFIR | Tüm iç zone'lar | any | REDDET | – | Tümü |
| 999 | Tumunu-Reddet | any | any | any | REDDET | – | Tümü |

## Veri sızıntısı (DLP) ve dosya engelleme

| Kural | Ayrıntı |
|---|---|
| Yükleme engeli | CAD (dwg, step, iges), kaynak kod arşivleri, model ağırlıkları (pt, onnx, safetensors), şifreli arşivler → izinli hedefler dışında **engelle** |
| İçerik eşleşmesi | "GİZLİ — AR-GE" etiketi, proje kod adları, patent başvuru numarası kalıpları → **engelle + SOC uyarısı** |
| Hacim eşiği | Kullanıcı başına saatte 2 GB üzeri dış yükleme → uyarı (SIEM kuralı, bkz. `00_Genel/04_Izleme_ve_Operasyon.md`) |
