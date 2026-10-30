"""Bant genisligi tahmin araci.
Formul: Gerekli = (sum(kullanici * eszamanlilik * Mbps)) * buyume + servis_payi
Hat: gereksinimi karsilayan bir sonraki standart hat kademesi.
Firewall: Threat Protection (enterprise mix) >= 1.5 x gereksinim.
"""
import csv

KADEMELER = [100, 200, 500, 1000, 2000, 5000, 10000, 20000]
BUYUME = 1.3

subeler = {
    "Istanbul Genel Merkez": dict(gruplar=[("Personel+IT", 325, 0.75, 4)], servis=500),
    "Ankara Ofisi":          dict(gruplar=[("Personel+IT", 150, 0.75, 3)], servis=50),
    "Londra Ofisi":          dict(gruplar=[("Personel+IT", 80, 0.75, 3)], servis=50),
    "Akademik Sube":         dict(gruplar=[("Ogrenci", 10000, 0.35, 1.5),
                                           ("Akademik+Idari+IT", 1040, 0.70, 3)], servis=1000),
    "Yazilim Ekibi":         dict(gruplar=[("Gelistirici+DevOps+QA", 150, 0.90, 8)], servis=500),
    "Ar-Ge Ekibi":           dict(gruplar=[("Arastirmaci+Teknik", 70, 0.90, 10)], servis=100),
}

satirlar = []
for ad, s in subeler.items():
    ham = sum(n * e * m for _, n, e, m in s["gruplar"])
    gerek = ham * BUYUME + s["servis"]
    hat = next((k for k in KADEMELER if k >= gerek), None)
    fw_min = gerek * 1.5
    satirlar.append([ad, sum(g[1] for g in s["gruplar"]), round(ham), round(gerek), hat, round(fw_min)])
    print(f"{ad:24s} kullanici={satirlar[-1][1]:6d} ham={ham:8.1f} gerekli={gerek:8.1f} Mbps hat={hat} FW_TP_min={fw_min/1000:.2f} Gbps")

with open("ozet_bant_genisligi.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Birim", "Kullanici", "Ham_Mbps", "Gerekli_Mbps", "Secilen_Hat_Mbps", "Min_FW_ThreatProt_Mbps"])
    w.writerows(satirlar)
