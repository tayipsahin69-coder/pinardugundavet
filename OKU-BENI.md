# pinardugundavet.com

Statik site. Her sayfa `uret.py` tarafından üretilir.

## Kural

`.html` dosyalarını elle düzenleme; `python uret.py` her çalıştığında üzerlerine yazar.
İçerik (adres, telefon, menüler, kına paketi, galeri, SSS) `uret.py` içindeki sabitlerde.

```
python uret.py
```

## Sayfalar

```
/                      ana sayfa
/salon/                salon ve 16 fotoğraflık galeri
/kina-organizasyonu/   16 kalemlik kına paketi
/menuler/              2 yemekli + 3 pastalı menü
/hizmetler/            24 hizmet, 6 grupta
/iletisim/             telefon, adres, harita
/kvkk/                 aydınlatma metni
```

Eski WordPress adresleri yeni sayfalara yönlendirilir (Google'daki eski
bağlantılar ölmesin diye):

| Eski | Yeni |
|---|---|
| /kurumsal/ | / |
| /fotograflar/ | /salon/ |
| /360-sanal-tur/ | /salon/ |
| /kina-organizasyon/ | /kina-organizasyonu/ |
| /bize-ulasin/ | /iletisim/ |

## Görseller

`assets/img/` içinde her fotoğrafın iki boyutu var: `-900.webp` ve `-1800.webp`.
Kaynak: eski sitedeki 2019 profesyonel çekimi (6000×4000). Yeni fotoğraf eklemek
için aynı adlandırmayla iki boyut üret ve `GALERI` listesine ekle.

---

# GitHub + alan adı aktarımı

## 1. GitHub deposu

Yerel depo hazır, ilk commit atıldı. GitHub'da boş bir depo aç
(README ekleme, boş kalsın), sonra:

```
git remote add origin git@github.com:<kullanici>/pinardugundavet.git
git push -u origin main
```

## 2. GitHub Pages'i aç

Depo → **Settings → Pages**

- Source: **Deploy from a branch**
- Branch: **main**, klasör: **/ (root)** → Save
- Custom domain kutusunda `pinardugundavet.com` görünmeli (depodaki `CNAME`
  dosyasından gelir). Görünmüyorsa yaz, Save.

## 3. DNS — Hostçini panelinde

> **ÖNEMLİ: Nameserver'ı DEĞİŞTİRME.** DNS şu an Hostçini'de
> (`ns1.hostcini.com`, `ns67.dnscini.com`) ve e-posta kayıtları orada.
> Nameserver değişirse info@pinardugundavet.com çalışmayı bırakabilir.
> Sadece aşağıdaki iki kaydı değiştir, gerisine dokunma.

**Değiştirilecek:**

| Kayıt | Tür | Eski değer | Yeni değer |
|---|---|---|---|
| `@` (kök) | A | 77.223.134.134 | **4 ayrı A kaydı:** 185.199.108.153 · 185.199.109.153 · 185.199.110.153 · 185.199.111.153 |
| `www` | A → **CNAME** | 77.223.134.134 | `<kullanici>.github.io` |

Kökteki tek A kaydını silip yerine dört ayrı A kaydı ekle. `www` için A kaydını
sil, aynı adla CNAME ekle.

**DOKUNMA:**

| Kayıt | Tür | Değer | Neden |
|---|---|---|---|
| `mail` | A | 77.223.134.134 | e-posta sunucusu |
| `@` | MX | mgkurumsal.dnscini.com | e-posta |
| `@` | MX | mail.pinardugundavet.com | e-posta |
| `@` | TXT | v=spf1 mx a include:_spf.dnscini.com -all | e-posta doğrulama |

## 4. HTTPS

DNS yayıldıktan sonra (birkaç dakika ile birkaç saat) GitHub sertifikayı
kendisi üretir. Settings → Pages → **Enforce HTTPS** kutusunu işaretle.
Kutu gri görünüyorsa sertifika henüz hazır değildir; biraz bekle.

## 5. Eski hosting paketi

**E-posta eski sitenin sunucusunda duruyor:** `mail.pinardugundavet.com`
ile web sitesi aynı IP'de (77.223.134.134). Hostçini paketini iptal etmeden önce
info@ kutusunun nerede barındığını Hostçini'ye sor. Paket kapanırsa e-posta da
gidebilir. İkinci MX (`mgkurumsal.dnscini.com`) ayrı bir kurumsal posta servisi;
asıl kutunun orada olup olmadığını teyit et.

## 6. Doğrulama

DNS yayıldıktan sonra:

```
nslookup pinardugundavet.com        # 185.199.10x.153 dönmeli
nslookup www.pinardugundavet.com    # <kullanici>.github.io'ya gitmeli
nslookup -type=MX pinardugundavet.com   # iki MX kaydı AYNEN durmalı
```

Bir de kendine info@pinardugundavet.com'a deneme e-postası at, geldiğini gör.

## 7. Google

- Search Console'a alan adını ekle, `sitemap.xml` gönder.
- Google İşletme Profili'ndeki web sitesi alanı `https://pinardugundavet.com`
  olmalı; adres ve telefon sitedekiyle birebir aynı yazılmalı.
