# 05 — (Opsiyonel) Neden Bu Güvenlik Duvarlarını Tercih Etmedik?

Seçim kriterlerimiz: (1) tüm güvenlik özellikleri açıkken yeterli performans, (2) merkezi yönetim ve SD-WAN, (3) Türkiye ve UK'de yerel destek/iş ortağı ağı, (4) 10.000+ kullanıcıyı kaldıracak ölçek, (5) toplam sahip olma maliyeti, (6) tedarik zinciri ve mevzuat riski.

## Ana listede olup #1 seçilmeyenler

| Ürün | Güçlü yanı | #1 olmama nedeni |
|---|---|---|
| **Check Point Quantum** | Olgun yönetim (SmartConsole), güçlü tehdit önleme, bankacılık sektöründe yaygın | Aynı performans sınıfında lisans + donanım maliyeti genellikle daha yüksek; SD-WAN'da Fortinet kadar entegre değil. Her şubede #3 olarak duruyor. |
| **Cisco Secure Firewall (FTD)** | Cisco anahtar/kablosuz altyapısıyla entegrasyon, güçlü Talos istihbaratı | Yönetim katmanı (FMC/cloud) birden fazla araç arasında dağınık; datasheet'te öne çıkan değerler genellikle IPS kapalı (FW+AVC) ölçüm, gerçek tehdit önleme kapasitesi daha düşük. |
| **Sophos XGS** | KOBİ'ler için kolay yönetim, uç nokta (endpoint) ürünleriyle senkronize güvenlik | Büyük kampüs ve çok şubeli kurumsal ölçekte referans sayısı daha az; üst segment model seçeneği sınırlı. |

## Ana listeye hiç girmeyenler

| Ürün | Neden elendi? |
|---|---|
| **pfSense / OPNsense** (açık kaynak) | Laboratuvar, küçük ofis ve eğitim için çok iyi; ancak 10.000 öğrencili kampüste kurumsal SLA'lı destek, merkezi çoklu cihaz yönetimi ve ticari tehdit istihbaratı beslemeleri yok. Arıza anında sorumluluk tamamen iç ekipte. *Öğrenci projesinde kural setlerini denemek için kullanılabilir.* |
| **MikroTik** | Uygun fiyatlı ve esnek bir yönlendirici; ancak tam bir yeni nesil güvenlik duvarı (uygulama tanıma, IPS, sandbox, SSL inceleme) değil. Kurumsal çevre güvenliği için yetersiz. |
| **Juniper SRX** | Teknik olarak güçlü, özellikle servis sağlayıcı ortamlarında. Şirketin 2025'te HPE bünyesine geçmesiyle entegrasyon sürecinde ürün yol haritasının netleşmesi beklendi; Türkiye'de güvenlik duvarı odaklı iş ortağı ve uzman sayısı Fortinet/Palo Alto'ya göre az. |
| **WatchGuard / SonicWall** | KOBİ ve şube segmentinde güçlü; kampüs çekirdeği (20 Gbps tehdit önleme) sınıfında seçenekleri ve referansları sınırlı. Bulut yönetim servislerinde geçmişte yaşanan güvenlik olayları da tedarikçi risk değerlendirmesinde dikkate alındı. |
| **Huawei USG** | Fiyat/performans iyi; ancak Londra ofisi için UK'deki tedarik zinciri güvenliği tartışmaları ve müşteri/denetçi algısı nedeniyle risk; tek üretici standardı hedeflendiği için Türkiye şubelerinde de tercih edilmedi. |
| **Sadece bulut tabanlı güvenlik (SASE: Zscaler, Netskope vb.)** | Uzaktan çalışanlar için güçlü bir tamamlayıcı; ancak kampüs içi segmentasyonu, laboratuvar izolasyonunu ve 5651 kapsamındaki yerel log yükümlülüğünü tek başına karşılamaz. İleride uzaktan erişim için ek katman olarak değerlendirilebilir. |

## Neden tek üretici değil, iki üretici?

- **Lehine:** Çevre (Fortinet) ve kritik iç segment (Palo Alto) farklı üreticiden olunca, bir üreticide çıkan sıfırıncı gün açığı iki katmanı birden geçemez.
- **Aleyhine:** İki yönetim aracı, iki eğitim seti, iki lisans sözleşmesi. Bu maliyet yalnızca kaynak kod ve fikri mülkiyetin bulunduğu iki segmentte kabul edildi; geri kalan her yerde tek üretici (Fortinet) standardı korundu.
