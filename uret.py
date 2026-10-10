# -*- coding: utf-8 -*-
"""
pinardugundavet.com sayfa ureticisi.

Kullanim:  python uret.py

Bu dosya sitenin TEK kaynagidir. Uretilen .html dosyalarini elle duzenleme;
bir sonraki calistirmada uzerine yazilir. Icerik degisikligi burada yapilir.

Icerigin tamami eski sitedeki (pinardugundavet.com, 2015) metinlerden ve
Instagram profilinden alindi. Fiyat, calisma saati ve koordinat gibi
kaynakta olmayan bilgi uydurulmadi.
"""

import os
import re
from datetime import date

KOK = os.path.dirname(os.path.abspath(__file__))
SITE = "https://pinardugundavet.com"
BUGUN = date.today().isoformat()

# ---------------------------------------------------------------------------
# ISLETME BILGISI
# ---------------------------------------------------------------------------

SALON = {
    "ad": "Pınar Düğün & Davet",
    "tam_ad": "Pınar Düğün Davet Salonu",
    "kurulus_firma": 2000,          # Has Pınar Yemek
    "kurulus_salon": 2015,          # Pınar Düğün Salonu
    "kapasite": 600,
    "bolunme": "300 kadın, 300 erkek",
    "adres_satir": "Kocasinan Merkez Mah. Mimar Sinan Cad. No:7 Kat:1",
    "adres_bina": "Kazancı İş Merkezi",
    "ilce": "Bahçelievler",
    "il": "İstanbul",
    "tel_sabit": "+902126512769",
    "tel_sabit_yazi": "0212 651 27 69",
    "tel_cep": "+905324477113",
    "tel_cep_yazi": "0532 447 71 13",
    "eposta": "info@pinardugundavet.com",
    "instagram": "https://www.instagram.com/pinardugundavet/",
    "facebook": "https://www.facebook.com/pinardugundavetsalonu/",
}

YIL_TECRUBE = date.today().year - SALON["kurulus_firma"]
HARITA_ADRES = "%s %s, %s/%s" % (SALON["adres_satir"], SALON["adres_bina"],
                                 SALON["ilce"], SALON["il"])
WHATSAPP = ("https://wa.me/%s?text=Merhaba%%2C%%20salonunuz%%20hakk%%C4%%B1nda"
            "%%20bilgi%%20almak%%20istiyorum." % SALON["tel_cep"].lstrip("+"))
HARITA_LINK = ("https://www.google.com/maps/search/?api=1&query="
               "P%C4%B1nar+D%C3%BC%C4%9F%C3%BCn+Davet+Salonu+Kocasinan+Bah%C3%A7elievler")
HARITA_GOMME = ("https://www.google.com/maps?q="
                "P%C4%B1nar+D%C3%BC%C4%9F%C3%BCn+Davet+Salonu+Kocasinan+Bah%C3%A7elievler"
                "+%C4%B0stanbul&output=embed")

# ---------------------------------------------------------------------------
# ICERIK — eski siteden birebir
# ---------------------------------------------------------------------------

ORGANIZASYONLAR = [
    ("Düğün", "Yemekli ya da kokteyl; gelin yolu, nikâh masası ve pist düzeniyle.",
     "gelin-yolu"),
    ("Nişan", "Küçük ya da kalabalık; salon isteğe göre ikiye bölünebilir.",
     "cicekli-sutunlar"),
    ("Kına gecesi", "Kına tahtı, bindallı, davul ve gelin çıkarma dahil hazır paket.",
     "kina-tahti"),
    ("Sünnet", "Sünnet tahtı, sahne ve eğlence düzeniyle.", "sahne-orkestra"),
    ("Doğum günü", "Pastalı menülerle aile ve çocuk kutlamaları.", "kristal-susleme"),
    ("Toplantı ve seminer", "Ses sistemi, sinevizyon ve dev ekranlarla.", "salon-sahne"),
]

# Eski sitenin 24 maddelik listesi; ayni maddeler gruplandi.
HIZMETLER = [
    ("Salon", [
        "Geniş pist alanı ve akustik ses sistemi",
        "Ferah ortam, modern mimari ve konforlu tasarım",
        "Rahat oturma düzeni",
        "Klima ve havalandırma sistemi",
        "Son sistem ışıklandırma ve aydınlatma",
        "Sinevizyon, barkovizyon ve dev ekran televizyonlar",
    ]),
    ("Süsleme", [
        "Gelin yolu ve nikâh masası süsleme",
        "Sandalye ve masa süsleme",
        "Şamdan ve supla",
        "Konfeti",
        "Kına tahtı, cibinlik, yer minderleri ve tabureler",
        "Sünnet tahtı",
    ]),
    ("Fotoğraf ve kayıt", [
        "Full çekim kamera",
        "10 poz 20 fotoğraf aile fotoğrafı",
        "Karşılama fotoğrafı",
    ]),
    ("Servis", [
        "Cam bardak ve porselen tabakta servis",
        "Güler yüzlü, deneyimli personel",
    ]),
    ("Gösteri", [
        "Semazen gösterisi",
        "Davul zurna gösterisi",
        "Kına gecesi organizasyonu",
    ]),
    ("Misafir rahatlığı", [
        "Bebek bakım odası",
        "Mescit alanı",
        "Sigara içme bölümü",
    ]),
]

KINA_PAKETI = [
    "Kına tahtı ve cibinliği", "Gelin bindallısı", "2 kına kızı",
    "Gelin çıkarma ve davul şov", "Karşılama masası", "5 adet arkadaş kaftanı",
    "2 adet konfeti", "Halay mendilleri", "5 adet tef", "Yüz örtüsü ve eldivenleri",
    "Damat kostümü", "12 adet el gülü ve el mumu", "Kına tepsisi ve sepeti",
    "5 adet kına tacı", "Laptop ve geniş müzik arşivi",
    "Kına gecesi organizasyonu ve planlama",
]

# Eski sitede iki ayri "Menu 3" vardi; adlar duzeltildi, icerik ayni.
MENULER = [
    {"ad": "Kırmızı et menüsü", "tur": "Yemekli",
     "kalemler": ["Et kavurma", "Pirinç pilavı", "Su böreği ya da patates püresi",
                  "Söğüş salata", "Meşrubat ya da ayran", "Cevizli baklava",
                  "Roll ekmek", "Bardak su"]},
    {"ad": "Beyaz et menüsü", "tur": "Yemekli",
     "kalemler": ["Tavuk sote", "Pirinç pilavı", "Su böreği ya da patates püresi",
                  "Söğüş salata", "Meşrubat ya da ayran", "Cevizli baklava",
                  "Roll ekmek", "Bardak su"]},
    {"ad": "Pastalı menü", "tur": "Kokteyl",
     "kalemler": ["Yaş pasta", "2 tatlı kurabiye", "2 çubuk kraker", "Sınırsız içecek"],
     "not": "İsteğe bağlı, ücret farkıyla su böreği eklenir."},
    {"ad": "Pastalı lüks menü", "tur": "Kokteyl",
     "kalemler": ["Yaş pasta", "Ekler", "Su böreği", "2 kurabiye", "2 çubuk kraker",
                  "Meşrubat", "Su"]},
    {"ad": "Dondurmalı pasta menüsü", "tur": "Kokteyl",
     "kalemler": ["Dondurmalı pasta", "2 tatlı kurabiye", "2 çubuk kraker",
                  "Sınırsız içecek"],
     "not": "İsteğe bağlı, ücret farkıyla su böreği eklenir."},
]

MENU_EKLER = [
    "İsteğe göre et döner, tavuk döner, karışık ızgara ve ordövr tabağı servis edilir.",
    "Mevsim salata ve çoban salata seçenekleri vardır.",
]

GALERI = [
    ("salon-genel", "Salonun genel görünümü: kristal orta süslemeli masalar ve pist"),
    ("gelin-yolu", "Kırmızı halı gelin yolu ve iki yanında çiçekli beyaz sütunlar"),
    ("nikah-masasi", "Beyaz ve altın detaylı nikâh masası köşesi"),
    ("masa-duzeni", "Yuvarlak masada porselen tabak ve gümüş supla düzeni"),
    ("salon-masalar", "Pembe örtülü masalar ve beyaz sandalyeler"),
    ("semazen", "Pistte semazen gösterisi"),
    ("salon-pist", "Siyah beyaz desenli pist zemini ve masalar"),
    ("kina-tahti", "Kırmızı cibinlikli kına tahtı"),
    ("kristal-susleme", "Kristal küre orta süslemeli masalar"),
    ("sahne-orkestra", "Işıklı çerçeveli sahne ve müzik düzeni"),
    ("cicekli-sutunlar", "Gelin yolunu çevreleyen çiçek sütunları"),
    ("salon-derin", "Salonun arka bölümü ve tavan aydınlatması"),
    ("giris-merdiven", "Çiçekli salon girişi"),
    ("pist-zemin", "Geniş pist alanı"),
    ("salon-isik", "Renkli tavan aydınlatması altında salon"),
    ("menu-tabagi", "Yemekli menü: tavuk sote, pilav, baklava ve salata"),
]

SSS = [
    ("Salon kaç kişilik?",
     "Salonumuz %d kişiliktir. İsteğe göre %s olmak üzere ayrı girişlerle ikiye "
     "bölünebilir." % (SALON["kapasite"], SALON["bolunme"])),
    ("Hangi organizasyonları yapıyorsunuz?",
     "Düğün, nişan, kına, sünnet, doğum günü, özel toplantı ve seminer. Hepsi yemekli "
     "ya da kokteyl olarak düzenlenebilir."),
    ("Kına organizasyonunda neler var?",
     "Kına tahtı ve cibinliği, gelin bindallısı, iki kına kızı, gelin çıkarma ve davul "
     "şov, arkadaş kaftanları, tef, kına tepsisi ve müzik dahil 16 kalemlik hazır bir "
     "paketimiz var."),
    ("Menüleri değiştirebilir miyiz?",
     "Evet. Yemekli ve pastalı menülerimizin yanında isteğe göre et döner, tavuk döner, "
     "karışık ızgara ve ordövr tabağı servis ediyoruz."),
    ("Fiyat ve boş tarih bilgisi nasıl alınır?",
     "Fiyat; tarihe, kişi sayısına ve menüye göre değişiyor. En doğru bilgi için bizi "
     "arayın ya da WhatsApp'tan yazın."),
    ("Salonu önceden görebilir miyiz?",
     "Elbette. Gelmeden önce arayıp gün belirlerseniz salonu ve düzeni yerinde "
     "gösteririz."),
]

# ---------------------------------------------------------------------------
# YARDIMCILAR
# ---------------------------------------------------------------------------

URETILEN = []


def yaz(yol, icerik):
    tam = os.path.join(KOK, yol)
    klasor = os.path.dirname(tam)
    if klasor:
        os.makedirs(klasor, exist_ok=True)
    with open(tam, "w", encoding="utf-8", newline="\n") as f:
        f.write(icerik)
    URETILEN.append(yol)


def kacir(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def duz(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def jk(s):
    return duz(s).replace("\\", "\\\\").replace('"', '\\"')


def resim(ad, alt, boyut="(max-width: 760px) 100vw, 50vw", yukle="lazy", oncelik=False):
    return ('<img src="/assets/img/%s-900.webp" '
            'srcset="/assets/img/%s-900.webp 900w, /assets/img/%s-1800.webp 1800w" '
            'sizes="%s" alt="%s" loading="%s" decoding="async"%s>'
            % (ad, ad, ad, boyut, kacir(alt), yukle,
               ' fetchpriority="high"' if oncelik else ""))


def baklava(sol=False):
    """Salonun siyah-beyaz baklava desenli zemininden gelen ayrac."""
    return ('<div class="baklava%s" aria-hidden="true"><i></i><i></i><i></i></div>'
            % (" baklava--sol" if sol else ""))


MENU = [("/", "Ana sayfa"), ("/salon/", "Salon"), ("/kina-organizasyonu/", "Kına"),
        ("/menuler/", "Menüler"), ("/hizmetler/", "Hizmetler"), ("/iletisim/", "İletişim")]


def ust(aktif):
    ler = "".join('<a href="%s"%s>%s</a>'
                  % (y, ' aria-current="page"' if y == aktif else "", a) for y, a in MENU)
    return """<header class="ust">
  <div class="sar ust__ic">
    <a class="logo" href="/" aria-label="Pınar Düğün &amp; Davet ana sayfa">
      <span class="logo__ad">Pınar</span>
      <span class="logo__alt">Düğün &amp; Davet</span>
    </a>
    <button class="menu-dugme" type="button" aria-expanded="false" aria-controls="ana-menu">
      <span class="menu-dugme__cizgi" aria-hidden="true"></span><span>Menü</span>
    </button>
    <nav class="ust__menu" id="ana-menu" aria-label="Ana menü">%s
      <a class="ust__ara" href="tel:%s">%s</a>
    </nav>
  </div>
</header>""" % (ler, SALON["tel_cep"], SALON["tel_cep_yazi"])


def alt():
    return """<footer class="alt">
  <div class="sar">
    <div class="alt__izgara">
      <div>
        <p class="logo logo--alt"><span class="logo__ad">Pınar</span><span class="logo__alt">Düğün &amp; Davet</span></p>
        <p class="alt__metin">%(yil)d yıldır Bahçelievler'de. %(kap)d kişilik salonumuzda düğün,
          nişan, kına, sünnet ve davetlerinizi ağırlıyoruz.</p>
      </div>
      <div>
        <p class="alt__baslik">Adres</p>
        <p>%(adres)s<br>%(bina)s<br>%(ilce)s / %(il)s</p>
        <p><a href="%(harita)s" target="_blank" rel="noopener">Yol tarifi al</a></p>
      </div>
      <div>
        <p class="alt__baslik">İletişim</p>
        <p><a href="tel:%(tc)s">%(tcy)s</a></p>
        <p><a href="tel:%(ts)s">%(tsy)s</a></p>
        <p><a href="mailto:%(ep)s">%(ep)s</a></p>
      </div>
      <div>
        <p class="alt__baslik">Takip edin</p>
        <p><a href="%(ig)s" target="_blank" rel="noopener">Instagram</a></p>
        <p><a href="%(fb)s" target="_blank" rel="noopener">Facebook</a></p>
      </div>
    </div>
    <div class="alt__satir">
      <span>&copy; <span id="yil">%(bugun)s</span> %(tam)s</span>
      <a href="/kvkk/">KVKK aydınlatma metni</a>
    </div>
  </div>
</footer>
<a class="wp" href="%(wp)s" target="_blank" rel="noopener" aria-label="WhatsApp'tan yazın">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.2a9.8 9.8 0 0 0-8.4 14.9L2.3 21.8l4.8-1.3A9.8 9.8 0 1 0 12 2.2Zm0 17.8a8 8 0 0 1-4.1-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 20Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3Z"/></svg>
  <span>WhatsApp</span>
</a>""" % {
        "yil": YIL_TECRUBE, "kap": SALON["kapasite"], "adres": SALON["adres_satir"],
        "bina": SALON["adres_bina"], "ilce": SALON["ilce"], "il": SALON["il"],
        "harita": HARITA_LINK, "tc": SALON["tel_cep"], "tcy": SALON["tel_cep_yazi"],
        "ts": SALON["tel_sabit"], "tsy": SALON["tel_sabit_yazi"], "ep": SALON["eposta"],
        "ig": SALON["instagram"], "fb": SALON["facebook"], "bugun": BUGUN[:4],
        "tam": SALON["tam_ad"], "wp": WHATSAPP}


def kirinti(parcalar):
    gor, kay = [], []
    for i, (ad, url) in enumerate(parcalar):
        gor.append('<li><a href="%s">%s</a></li>' % (url, ad) if url
                   else '<li aria-current="page">%s</li>' % ad)
        kay.append('{"@type":"ListItem","position":%d,"name":"%s"%s}'
                   % (i + 1, jk(ad), (',"item":"%s%s"' % (SITE, url)) if url else ""))
    return ('<nav aria-label="Neredesiniz"><ol class="kirinti">%s</ol></nav>' % "".join(gor),
            '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}'
            % ",".join(kay))


def cta(baslik="Tarihinizi birlikte planlayalım",
        metin="Fiyat ve boş tarih bilgisi için arayın ya da WhatsApp'tan yazın. "
              "Salonu görmek isterseniz gün belirleyelim."):
    return """
<section class="cta">
  <div class="sar cta__ic">
    %s
    <h2>%s</h2>
    <p>%s</p>
    <div class="eylem eylem--orta">
      <a class="btn" href="%s" target="_blank" rel="noopener">WhatsApp'tan yazın</a>
      <a class="btn btn--cizgi" href="tel:%s">%s</a>
    </div>
  </div>
</section>""" % (baklava(), kacir(baslik), kacir(metin), WHATSAPP,
                 SALON["tel_cep"], SALON["tel_cep_yazi"])


def sss_blok(ciftler):
    govde = "".join('<details class="sss"><summary>%s</summary><p>%s</p></details>'
                    % (kacir(s), kacir(c)) for s, c in ciftler)
    ld = ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}'
          % ",".join('{"@type":"Question","name":"%s","acceptedAnswer":'
                     '{"@type":"Answer","text":"%s"}}' % (jk(s), jk(c)) for s, c in ciftler))
    return govde, ld


def ld_mekan():
    return ('{"@context":"https://schema.org","@type":["EventVenue","LocalBusiness"],'
            '"@id":"%(site)s/#mekan","name":"%(ad)s","alternateName":"%(alt)s",'
            '"url":"%(site)s/","image":"%(site)s/assets/img/og.jpg",'
            '"telephone":"%(tel)s","email":"%(ep)s",'
            '"description":"Bahçelievler Kocasinan\'da %(kap)d kişilik düğün, nişan, kına, '
            'sünnet ve davet salonu.",'
            '"foundingDate":"%(kur)d","maximumAttendeeCapacity":%(kap)d,'
            '"address":{"@type":"PostalAddress","streetAddress":"%(adres)s %(bina)s",'
            '"addressLocality":"%(ilce)s","addressRegion":"%(il)s","addressCountry":"TR"},'
            '"hasMap":"%(harita)s","sameAs":["%(ig)s","%(fb)s"]}'
            % {"site": SITE, "ad": SALON["tam_ad"], "alt": SALON["ad"],
               "tel": SALON["tel_sabit"], "ep": SALON["eposta"], "kap": SALON["kapasite"],
               "kur": SALON["kurulus_salon"], "adres": SALON["adres_satir"],
               "bina": SALON["adres_bina"], "ilce": SALON["ilce"], "il": SALON["il"],
               "harita": HARITA_LINK, "ig": SALON["instagram"], "fb": SALON["facebook"]})


def sayfa(baslik, aciklama, yol, govde, ldler=(), aktif="", onyukle="", robots=""):
    ld = "".join('\n<script type="application/ld+json">%s</script>' % b for b in ldler if b)
    on = ('\n<link rel="preload" as="image" href="/assets/img/%s-900.webp" '
          'imagesrcset="/assets/img/%s-900.webp 900w, /assets/img/%s-1800.webp 1800w" '
          'imagesizes="100vw" fetchpriority="high">'
          % (onyukle, onyukle, onyukle)) if onyukle else ""
    rb = '\n<meta name="robots" content="%s">' % robots if robots else ""
    return """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(baslik)s</title>
<meta name="description" content="%(aciklama)s">
<link rel="canonical" href="%(site)s%(yol)s">%(rb)s
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="Pınar Düğün &amp; Davet">
<meta property="og:url" content="%(site)s%(yol)s">
<meta property="og:title" content="%(baslik)s">
<meta property="og:description" content="%(aciklama)s">
<meta property="og:image" content="%(site)s/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="%(site)s/assets/img/og.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Jost:wght@400;500&display=swap">%(on)s
<link rel="stylesheet" href="/assets/stil.css">%(ld)s
</head>
<body>
<a class="atla" href="#icerik">İçeriğe geç</a>
%(ust)s
<main id="icerik">
%(govde)s
</main>
%(alt)s
<script src="/assets/site.js" defer></script>
</body>
</html>
""" % {"baslik": kacir(baslik), "aciklama": kacir(aciklama), "site": SITE, "yol": yol,
       "rb": rb, "on": on, "ld": ld, "ust": ust(aktif), "govde": govde, "alt": alt()}


# ---------------------------------------------------------------------------
# STIL
# ---------------------------------------------------------------------------

STIL = """:root{
  --beyaz:#FFFFFF;
  --kirik:#FAF7F5;
  --pudra:#F4E3DF;
  --murekkep:#151413;
  --murekkep-2:#4A4643;
  --murekkep-3:#6E6864;
  --cizgi:rgba(21,20,19,.13);
  --cizgi-2:rgba(21,20,19,.07);
  --altin:#8A6A3C;
  --altin-2:#B8935A;
  --olcu:1160px;
  --dar:780px;
  --baslik:'Bodoni Moda','Didot','Bodoni MT',Georgia,serif;
  --govde:'Jost',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
  --gecis:.3s cubic-bezier(.22,.61,.36,1);
}

*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition-duration:.01ms!important}
}
body{
  background:var(--beyaz);color:var(--murekkep);
  font-family:var(--govde);font-size:17px;line-height:1.7;
  -webkit-font-smoothing:antialiased;
}
img{display:block;max-width:100%;height:auto}
:target{scroll-margin-top:96px}

.sar{max-width:var(--olcu);margin:0 auto;padding-inline:22px;width:100%}
.sar--dar{max-width:var(--dar)}

a{color:inherit;text-decoration:none;transition:color var(--gecis)}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--altin);outline-offset:4px;border-radius:2px}

.atla{position:absolute;left:-9999px;top:0;z-index:60;padding:12px 18px;background:var(--murekkep);color:#fff}
.atla:focus{left:10px;top:10px}

/* ---------- baslik dili ---------- */
.ust-yazi{font-size:12px;font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--altin)}
h1,h2,h3{font-family:var(--baslik);font-weight:400;letter-spacing:-.01em;line-height:1.1;text-wrap:balance}
h1{font-size:clamp(42px,7vw,90px);line-height:1.03}
h2{font-size:clamp(32px,4.5vw,54px)}
h3{font-size:clamp(22px,2.4vw,28px)}
h1 em,h2 em{font-style:italic;color:var(--altin)}

/* ---------- baklava motifi (salonun zemininden) ---------- */
.baklava{display:flex;justify-content:center;gap:10px;margin-bottom:22px}
.baklava i{width:9px;height:9px;transform:rotate(45deg);background:var(--murekkep)}
.baklava i:nth-child(2){background:transparent;border:1px solid var(--murekkep)}
.baklava--sol{justify-content:flex-start}

/* ---------- ust ---------- */
.ust{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--cizgi-2)}
.ust__ic{display:flex;align-items:center;justify-content:space-between;gap:18px;padding-block:13px}
.logo{display:flex;flex-direction:column;line-height:1}
.logo__ad{font-family:var(--baslik);font-size:30px;font-style:italic;letter-spacing:-.01em}
.logo__alt{font-size:10.5px;font-weight:500;letter-spacing:.3em;text-transform:uppercase;color:var(--murekkep-3);margin-top:5px}
.ust__menu{display:flex;align-items:center;gap:2px}
.ust__menu a{font-size:14.5px;font-weight:500;letter-spacing:.02em;color:var(--murekkep-2);padding:10px 13px;min-height:44px;display:inline-flex;align-items:center}
.ust__menu a:hover{color:var(--murekkep)}
.ust__menu a[aria-current="page"]{color:var(--murekkep);box-shadow:inset 0 -1px 0 var(--altin-2)}
.ust__menu .ust__ara{margin-left:10px;border:1px solid var(--murekkep);color:var(--murekkep);padding-inline:18px;border-radius:999px;transition:background var(--gecis),color var(--gecis)}
.ust__menu .ust__ara:hover{background:var(--murekkep);color:#fff}

.menu-dugme{display:none;align-items:center;gap:10px;background:none;border:1px solid var(--cizgi);border-radius:999px;padding:0 16px;min-height:44px;font:500 13px var(--govde);letter-spacing:.14em;text-transform:uppercase;color:var(--murekkep);cursor:pointer}
.menu-dugme__cizgi,.menu-dugme__cizgi::before,.menu-dugme__cizgi::after{display:block;width:16px;height:1px;background:currentColor;transition:transform var(--gecis)}
.menu-dugme__cizgi{position:relative}
.menu-dugme__cizgi::before,.menu-dugme__cizgi::after{content:"";position:absolute;left:0}
.menu-dugme__cizgi::before{top:-5px}.menu-dugme__cizgi::after{top:5px}
.menu-dugme[aria-expanded="true"] .menu-dugme__cizgi{background:transparent}
.menu-dugme[aria-expanded="true"] .menu-dugme__cizgi::before{transform:translateY(5px) rotate(45deg)}
.menu-dugme[aria-expanded="true"] .menu-dugme__cizgi::after{transform:translateY(-5px) rotate(-45deg)}
@media (max-width:1000px){
  .menu-dugme{display:inline-flex}
  .ust__ic{flex-wrap:wrap}
  .ust__menu{display:none;order:3;width:100%;flex-direction:column;align-items:stretch;gap:0;padding-top:6px;border-top:1px solid var(--cizgi-2);margin-top:12px}
  .ust__menu.acik{display:flex}
  .ust__menu a{min-height:52px;font-size:16px;border-bottom:1px solid var(--cizgi-2)}
  .ust__menu .ust__ara{margin:14px 0 8px;justify-content:center}
}

/* ---------- butonlar ---------- */
.eylem{display:flex;flex-wrap:wrap;gap:12px;margin-top:34px}
.eylem--orta{justify-content:center}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:14px 30px;border-radius:999px;background:var(--murekkep);color:#fff;border:1px solid var(--murekkep);font-size:14px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;transition:background var(--gecis),color var(--gecis),border-color var(--gecis)}
.btn:hover{background:var(--altin);border-color:var(--altin);color:#fff}
.btn--cizgi{background:transparent;color:var(--murekkep)}
.btn--cizgi:hover{background:var(--murekkep);color:#fff;border-color:var(--murekkep)}
.btn--acik{background:#fff;color:var(--murekkep);border-color:#fff}
.btn--acik:hover{background:var(--pudra);border-color:var(--pudra);color:var(--murekkep)}

/* ---------- kahraman ---------- */
.kahraman{position:relative;min-height:min(86vh,840px);display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:var(--murekkep)}
.kahraman__gorsel{position:absolute;inset:0}
.kahraman__gorsel img{width:100%;height:100%;object-fit:cover;object-position:50% 58%}
.kahraman::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(21,20,19,.62) 0%,rgba(21,20,19,.28) 48%,rgba(21,20,19,0) 76%),linear-gradient(180deg,rgba(21,20,19,.22) 0%,rgba(21,20,19,0) 34%,rgba(21,20,19,.6) 100%)}
@media (max-width:760px){.kahraman::after{background:linear-gradient(180deg,rgba(21,20,19,.3) 0%,rgba(21,20,19,.25) 40%,rgba(21,20,19,.8) 100%)}}
.kahraman__ic{position:relative;z-index:2;padding-block:120px 70px}
.kahraman .ust-yazi{color:var(--pudra)}
.kahraman h1{margin-top:18px;max-width:14ch}
.kahraman h1 em{color:var(--pudra)}
.kahraman__metin{margin-top:22px;font-size:clamp(17px,1.5vw,19px);max-width:46ch;color:rgba(255,255,255,.9)}
.kahraman .btn--cizgi{color:#fff;border-color:rgba(255,255,255,.72)}
.kahraman .btn--cizgi:hover{background:#fff;color:var(--murekkep);border-color:#fff}

/* ---------- olcu seridi ---------- */
.olculer{border-bottom:1px solid var(--cizgi-2)}
.olculer__izgara{display:grid;grid-template-columns:repeat(2,1fr)}
@media (min-width:860px){.olculer__izgara{grid-template-columns:repeat(4,1fr)}}
.olcu{padding:34px 18px;text-align:center}
.olcu+.olcu{border-left:1px solid var(--cizgi-2)}
@media (max-width:859px){
  .olcu:nth-child(3){border-left:0}
  .olcu:nth-child(-n+2){border-bottom:1px solid var(--cizgi-2)}
}
.olcu b{display:block;font-family:var(--baslik);font-size:clamp(34px,4vw,48px);font-weight:400;line-height:1;font-variant-numeric:lining-nums}
.olcu span{display:block;margin-top:10px;font-size:12px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--murekkep-3)}

/* ---------- bolum ---------- */
.bolum{padding-block:104px}
.bolum--ust-yok{padding-top:0}
.bolum--pudra{background:var(--kirik)}
.bolum__ust{text-align:center;max-width:680px;margin:0 auto 58px}
.bolum__ust h2{margin-top:14px}
.bolum__ust p{margin:20px auto 0;color:var(--murekkep-2);max-width:54ch}

/* ---------- hikaye ---------- */
.hikaye{display:grid;gap:52px;align-items:center;grid-template-columns:1fr}
@media (min-width:900px){.hikaye{grid-template-columns:1fr 1fr;gap:84px}}
.hikaye__gorsel{position:relative;isolation:isolate}
.hikaye__gorsel img{width:100%;aspect-ratio:4/5;object-fit:cover}
.hikaye__gorsel::after{content:"";position:absolute;inset:18px -18px -18px 18px;border:1px solid var(--altin-2);z-index:-1}
@media (max-width:899px){.hikaye__gorsel::after{inset:12px -10px -12px 10px}}
.hikaye h2{margin-top:14px}
.hikaye p{margin-top:20px;color:var(--murekkep-2)}

.zaman{list-style:none;margin-top:30px;border-top:1px solid var(--cizgi)}
.zaman li{display:grid;grid-template-columns:78px 1fr;gap:18px;padding-block:16px;border-bottom:1px solid var(--cizgi)}
.zaman b{font-family:var(--baslik);font-size:24px;font-weight:400;line-height:1.15}
.zaman span{color:var(--murekkep-2);font-size:16px;padding-top:2px}

/* ---------- organizasyon kartlari ---------- */
.kartlar{display:grid;gap:22px;grid-template-columns:1fr}
@media (min-width:640px){.kartlar{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1000px){.kartlar{grid-template-columns:repeat(3,1fr)}}
.kart{display:flex;flex-direction:column;background:var(--beyaz)}
.kart__gorsel{overflow:hidden}
.kart__gorsel img{width:100%;aspect-ratio:4/3;object-fit:cover;transition:transform .8s cubic-bezier(.22,.61,.36,1)}
.kart:hover .kart__gorsel img{transform:scale(1.04)}
.kart__ic{padding:24px 24px 30px}
.kart h3{font-size:27px}
.kart p{margin-top:9px;color:var(--murekkep-2);font-size:16px;line-height:1.6}

/* ---------- galeri ---------- */
.galeri{display:grid;gap:10px;grid-template-columns:repeat(2,1fr)}
@media (min-width:860px){.galeri{grid-template-columns:repeat(4,1fr)}}
.galeri a{position:relative;display:block;overflow:hidden;background:var(--kirik)}
.galeri img{width:100%;height:100%;aspect-ratio:1;object-fit:cover;transition:transform .8s cubic-bezier(.22,.61,.36,1)}
.galeri a:hover img{transform:scale(1.05)}
.galeri a:first-child{grid-column:span 2;grid-row:span 2}
.galeri a:first-child img{aspect-ratio:auto}

/* ---------- isik kutusu ---------- */
.kutu{position:fixed;inset:0;z-index:80;background:rgba(21,20,19,.95);display:flex;align-items:center;justify-content:center;padding:64px 16px}
.kutu[hidden]{display:none}
.kutu figure{margin:0;display:flex;flex-direction:column;align-items:center}
.kutu img{max-height:80vh;max-width:min(1400px,100%);object-fit:contain}
.kutu figcaption{margin-top:16px;text-align:center;color:rgba(255,255,255,.82);font-size:14px;max-width:60ch}
.kutu button{position:absolute;background:none;border:1px solid rgba(255,255,255,.35);color:#fff;width:48px;height:48px;border-radius:999px;font-size:22px;line-height:1;cursor:pointer;transition:border-color var(--gecis),background var(--gecis)}
.kutu button:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.kutu__kapat{top:14px;right:14px}
.kutu__onceki{left:14px;top:50%;transform:translateY(-50%)}
.kutu__sonraki{right:14px;top:50%;transform:translateY(-50%)}

/* ---------- liste ---------- */
.hizmet-izgara{display:grid;gap:46px 56px;grid-template-columns:1fr}
@media (min-width:760px){.hizmet-izgara{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1060px){.hizmet-izgara{grid-template-columns:repeat(3,1fr)}}
.hizmet-grup h3{font-size:24px;padding-bottom:14px;border-bottom:1px solid var(--murekkep)}
.liste{list-style:none;margin-top:6px}
.liste li{position:relative;padding:11px 0 11px 22px;border-bottom:1px solid var(--cizgi-2);color:var(--murekkep-2);font-size:16px;line-height:1.5}
.liste li::before{content:"";position:absolute;left:1px;top:19px;width:6px;height:6px;transform:rotate(45deg);background:var(--altin-2)}
.liste--iki{columns:2;column-gap:48px;margin-top:22px}
.liste--iki li{break-inside:avoid}
@media (max-width:680px){.liste--iki{columns:1}}

/* ---------- menuler ---------- */
.menuler{display:grid;gap:22px;grid-template-columns:1fr}
@media (min-width:760px){.menuler{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1080px){.menuler{grid-template-columns:repeat(3,1fr)}}
.menu{background:var(--beyaz);border:1px solid var(--cizgi);padding:38px 30px 32px;text-align:center;display:flex;flex-direction:column}
.menu__tur{font-size:11.5px;font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--altin)}
.menu h3{margin-top:12px;font-size:28px}
.menu ul{list-style:none;margin-top:22px;padding-top:20px;border-top:1px solid var(--cizgi-2)}
.menu li{padding-block:6px;color:var(--murekkep-2);font-size:16px}
.menu__not{margin-top:auto;padding-top:20px;font-size:14px;font-style:italic;color:var(--murekkep-3)}
.ekler{margin-top:44px;text-align:center;color:var(--murekkep-2)}
.ekler p+p{margin-top:6px}

/* ---------- kina vitrini ---------- */
.vitrin{display:grid;gap:52px;grid-template-columns:1fr;align-items:center}
@media (min-width:920px){.vitrin{grid-template-columns:.92fr 1.08fr;gap:76px}}
.vitrin__gorseller{display:grid;gap:12px;grid-template-columns:1.2fr 1fr;grid-template-rows:1fr 1fr}
.vitrin__gorseller img{width:100%;height:100%;object-fit:cover}
.vitrin__gorseller img:first-child{grid-row:span 2;aspect-ratio:3/4}
.vitrin__gorseller img:not(:first-child){aspect-ratio:1}
.vitrin h2{margin-top:14px}
.vitrin p{margin-top:18px;color:var(--murekkep-2)}

/* ---------- sss ---------- */
.sss-liste{border-top:1px solid var(--murekkep)}
.sss{border-bottom:1px solid var(--cizgi)}
.sss summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding-block:24px;min-height:56px;font-family:var(--baslik);font-size:clamp(19px,2vw,23px);line-height:1.3;transition:color var(--gecis)}
.sss summary::-webkit-details-marker{display:none}
.sss summary::after{content:"+";font-family:var(--govde);font-size:26px;font-weight:300;color:var(--altin);flex:none;transition:transform var(--gecis)}
.sss[open] summary::after{transform:rotate(45deg)}
.sss summary:hover{color:var(--altin)}
.sss p{padding-bottom:26px;color:var(--murekkep-2);max-width:62ch}

/* ---------- iletisim ---------- */
.iletisim{display:grid;gap:52px;grid-template-columns:1fr}
@media (min-width:900px){.iletisim{grid-template-columns:1fr 1.15fr;gap:64px}}
.iletisim__blok{padding-block:22px;border-bottom:1px solid var(--cizgi)}
.iletisim__blok:first-child{border-top:1px solid var(--murekkep)}
.iletisim__etiket{font-size:12px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--altin);margin-bottom:6px}
.iletisim__blok a{display:inline-flex;align-items:center;min-height:40px;font-family:var(--baslik);font-size:25px}
.iletisim__blok a:hover{color:var(--altin)}
.iletisim__blok address{font-style:normal;font-size:18px;line-height:1.6}
.harita{width:100%;aspect-ratio:4/3;border:0;background:var(--kirik)}

/* ---------- ic sayfa ---------- */
.kirinti{list-style:none;display:flex;flex-wrap:wrap;gap:4px 10px;font-size:13px;letter-spacing:.06em;color:var(--murekkep-3);padding-top:28px}
.kirinti li{display:inline-flex;align-items:center;min-height:28px}
.kirinti li+li::before{content:"";width:5px;height:5px;transform:rotate(45deg);background:var(--altin-2);margin-right:10px}
.kirinti a:hover{color:var(--murekkep)}
.ic-baslik{padding-block:34px 70px;text-align:center}
.ic-baslik h1{font-size:clamp(40px,6vw,74px);margin-top:16px}
.ic-baslik p:not(.ust-yazi){margin:22px auto 0;color:var(--murekkep-2);max-width:56ch;font-size:18px}
.ic-gorsel{margin-bottom:96px}
.ic-gorsel img{width:100%;height:min(64vh,600px);object-fit:cover}
.yasal p+p{margin-top:16px}
.yasal{color:var(--murekkep-2)}
.yasal a{border-bottom:1px solid var(--cizgi)}

/* ---------- cta ---------- */
.cta{background:var(--pudra);padding-block:96px;text-align:center}
.cta h2{max-width:18ch;margin:0 auto}
.cta p{margin:20px auto 0;max-width:52ch;color:var(--murekkep-2)}

/* ---------- alt ---------- */
.alt{background:var(--murekkep);color:rgba(255,255,255,.74);padding-block:72px 34px;font-size:15.5px}
.alt a{color:#fff;display:inline-flex;align-items:center;min-height:32px;border-bottom:1px solid rgba(255,255,255,.22);transition:border-color var(--gecis)}
.alt a:hover{border-color:#fff}
.alt__izgara{display:grid;gap:40px;grid-template-columns:1fr}
@media (min-width:680px){.alt__izgara{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1000px){.alt__izgara{grid-template-columns:1.5fr 1fr 1fr .8fr}}
.logo--alt .logo__ad{color:#fff}
.logo--alt .logo__alt{color:rgba(255,255,255,.58)}
.alt__metin{margin-top:18px;max-width:34ch;line-height:1.7}
.alt__baslik{font-size:11.5px;font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--altin-2);margin-bottom:10px}
.alt__izgara p+p{margin-top:4px}
.alt__satir{display:flex;flex-wrap:wrap;gap:10px 24px;justify-content:space-between;align-items:center;margin-top:56px;padding-top:24px;border-top:1px solid rgba(255,255,255,.12);font-size:13.5px}

/* ---------- whatsapp ---------- */
.wp{position:fixed;right:18px;bottom:18px;z-index:45;display:inline-flex;align-items:center;gap:10px;min-height:52px;padding:0 20px 0 16px;border-radius:999px;background:#1E7349;color:#fff;font-size:14.5px;font-weight:500;letter-spacing:.04em;box-shadow:0 12px 30px -12px rgba(21,20,19,.55);transition:transform var(--gecis),background var(--gecis)}
.wp:hover{transform:translateY(-2px);background:#185F3C}
.wp svg{width:24px;height:24px}
@media (max-width:560px){.wp span{display:none}.wp{padding:0;width:56px;justify-content:center}}

@media (max-width:640px){
  body{font-size:16px}
  .bolum{padding-block:72px}
  .bolum__ust{margin-bottom:42px}
  .kahraman__ic{padding-block:100px 54px}
  .cta{padding-block:72px}
  .ic-gorsel{margin-bottom:64px}
  .menu{padding:32px 22px 28px}
}
"""

BETIK = """(function () {
  var y = document.getElementById('yil');
  if (y) y.textContent = new Date().getFullYear();

  var d = document.querySelector('.menu-dugme'), m = document.getElementById('ana-menu');
  if (d && m) {
    d.addEventListener('click', function () {
      var a = m.classList.toggle('acik');
      d.setAttribute('aria-expanded', a ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && m.classList.contains('acik')) {
        m.classList.remove('acik'); d.setAttribute('aria-expanded', 'false'); d.focus();
      }
    });
  }

  // ---- isik kutusu ----
  var linkler = [].slice.call(document.querySelectorAll('[data-kutu]'));
  if (!linkler.length) return;
  var kutu = document.createElement('div');
  kutu.className = 'kutu'; kutu.hidden = true;
  kutu.setAttribute('role', 'dialog'); kutu.setAttribute('aria-modal', 'true');
  kutu.setAttribute('aria-label', 'Fotoğraf');
  kutu.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="kutu__kapat" type="button" aria-label="Kapat">&times;</button>' +
    '<button class="kutu__onceki" type="button" aria-label="Önceki fotoğraf">&#8249;</button>' +
    '<button class="kutu__sonraki" type="button" aria-label="Sonraki fotoğraf">&#8250;</button>';
  document.body.appendChild(kutu);
  var img = kutu.querySelector('img'), cap = kutu.querySelector('figcaption');
  var sira = 0, onceki = null;

  function goster(i) {
    sira = (i + linkler.length) % linkler.length;
    var a = linkler[sira], k = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = k ? k.alt : '';
    cap.textContent = k ? k.alt : '';
  }
  function ac(i) {
    onceki = document.activeElement;
    goster(i); kutu.hidden = false; document.body.style.overflow = 'hidden';
    kutu.querySelector('.kutu__kapat').focus();
  }
  function kapat() {
    kutu.hidden = true; document.body.style.overflow = '';
    if (onceki) onceki.focus();
  }
  linkler.forEach(function (a, i) {
    a.addEventListener('click', function (e) { e.preventDefault(); ac(i); });
  });
  kutu.querySelector('.kutu__kapat').addEventListener('click', kapat);
  kutu.querySelector('.kutu__onceki').addEventListener('click', function () { goster(sira - 1); });
  kutu.querySelector('.kutu__sonraki').addEventListener('click', function () { goster(sira + 1); });
  kutu.addEventListener('click', function (e) { if (e.target === kutu) kapat(); });
  document.addEventListener('keydown', function (e) {
    if (kutu.hidden) return;
    if (e.key === 'Escape') kapat();
    if (e.key === 'ArrowLeft') goster(sira - 1);
    if (e.key === 'ArrowRight') goster(sira + 1);
  });
})();
"""


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="64" height="64" rx="12" fill="#151413"/>'
            '<text x="32" y="45" font-family="Georgia,serif" font-style="italic" '
            'font-size="38" fill="#F4E3DF" text-anchor="middle">P</text></svg>\n')


# ---------------------------------------------------------------------------
# PARCALAR
# ---------------------------------------------------------------------------

def galeri_html(liste):
    return '<div class="galeri">%s</div>' % "".join(
        '<a href="/assets/img/%s-1800.webp" data-kutu>%s</a>'
        % (ad, resim(ad, alt, boyut="(max-width: 860px) 50vw, 25vw")) for ad, alt in liste)


def organizasyon_kartlari():
    return '<div class="kartlar">%s</div>' % "".join(
        '<article class="kart"><div class="kart__gorsel">%s</div>'
        '<div class="kart__ic"><h3>%s</h3><p>%s</p></div></article>'
        % (resim(g, b, boyut="(max-width: 640px) 100vw, (max-width: 1000px) 50vw, 33vw"),
           kacir(b), kacir(m)) for b, m, g in ORGANIZASYONLAR)


def menu_kartlari():
    ler = []
    for mn in MENULER:
        ler.append('<article class="menu"><p class="menu__tur">%s</p><h3>%s</h3>'
                   '<ul>%s</ul>%s</article>'
                   % (kacir(mn["tur"]), kacir(mn["ad"]),
                      "".join("<li>%s</li>" % kacir(k) for k in mn["kalemler"]),
                      ('<p class="menu__not">%s</p>' % kacir(mn["not"])) if mn.get("not") else ""))
    return '<div class="menuler">%s</div>' % "".join(ler)


def hizmet_gruplari(gruplar=None):
    return '<div class="hizmet-izgara">%s</div>' % "".join(
        '<div class="hizmet-grup"><h3>%s</h3><ul class="liste">%s</ul></div>'
        % (kacir(g), "".join("<li>%s</li>" % kacir(x) for x in liste))
        for g, liste in HIZMETLER if gruplar is None or g in gruplar)


def kina_gorselleri():
    return ('<div class="vitrin__gorseller">%s%s%s</div>'
            % (resim("kina-tahti", "Kırmızı cibinlikli kına tahtı",
                     boyut="(max-width: 920px) 60vw, 30vw"),
               resim("davul", "Kına gecesi davulu", boyut="(max-width: 920px) 40vw, 20vw"),
               resim("kina-koltuk", "Kına gecesi gelin koltuğu",
                     boyut="(max-width: 920px) 40vw, 20vw")))


def olcu_seridi():
    return """
<section class="olculer" aria-label="Kısaca salon">
  <div class="sar olculer__izgara">
    <div class="olcu"><b>%d</b><span>yıllık tecrübe</span></div>
    <div class="olcu"><b>%d</b><span>kişilik salon</span></div>
    <div class="olcu"><b>2</b><span>ayrı giriş</span></div>
    <div class="olcu"><b>16</b><span>kalem kına paketi</span></div>
  </div>
</section>""" % (YIL_TECRUBE, SALON["kapasite"])


def ic_baslik(ust_yazi, baslik, metin=""):
    return """
<div class="sar">
  <header class="ic-baslik">
    %s
    <p class="ust-yazi">%s</p>
    <h1>%s</h1>
    %s
  </header>
</div>""" % (baklava(), kacir(ust_yazi), baslik, ("<p>%s</p>" % metin) if metin else "")


def bolum_ust(ust_yazi, baslik, metin=""):
    return """<header class="bolum__ust">
      %s
      <p class="ust-yazi">%s</p>
      <h2>%s</h2>
      %s
    </header>""" % (baklava(), kacir(ust_yazi), baslik, ("<p>%s</p>" % metin) if metin else "")


# ---------------------------------------------------------------------------
# SAYFALAR
# ---------------------------------------------------------------------------

def ana_sayfa():
    sss_govde, sss_ld = sss_blok(SSS)
    govde = """
<section class="kahraman">
  <div class="kahraman__gorsel">%(kahraman)s</div>
  <div class="sar kahraman__ic">
    <p class="ust-yazi">Bahçelievler · %(kur)d'ten beri</p>
    <h1>En güzel gününüz <em>burada</em> başlasın.</h1>
    <p class="kahraman__metin">%(kap)d kişilik salonumuzda düğün, nişan, kına, sünnet ve
      davetlerinizi %(yil)d yıllık tecrübeyle ağırlıyoruz.</p>
    <div class="eylem">
      <a class="btn btn--acik" href="%(wp)s" target="_blank" rel="noopener">Tarih sorun</a>
      <a class="btn btn--cizgi" href="/salon/">Salonu görün</a>
    </div>
  </div>
</section>
%(olcu)s

<section class="bolum">
  <div class="sar hikaye">
    <div class="hikaye__gorsel">%(hikaye)s</div>
    <div>
      %(bs)s
      <p class="ust-yazi">Hikâyemiz</p>
      <h2>Bir yemek mutfağından <em>düğün salonuna</em></h2>
      <p>Sektöre ilk adımımızı %(kurf)d yılında Bahçelievler Kocasinan'da Has Pınar Yemek
        olarak attık. %(kur)d'te aynı mahallede %(kap)d kişilik Pınar Düğün Salonu'nu
        açtık.</p>
      <p>Hazırlıkların başladığı ilk günden gecenin sonuna kadar yanınızdayız. Sade ya da
        gösterişli, klasik ya da sıra dışı; size en uygun düzeni birlikte buluruz.</p>
      <ul class="zaman">
        <li><b>%(kurf)d</b><span>Has Pınar Yemek, Bahçelievler Kocasinan</span></li>
        <li><b>%(kur)d</b><span>%(kap)d kişilik Pınar Düğün Salonu açıldı</span></li>
        <li><b>Bugün</b><span>%(yil)d yıllık tecrübe, aynı mahallede</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="bolum bolum--pudra">
  <div class="sar">
    %(org_ust)s
    %(kartlar)s
  </div>
</section>

<section class="bolum">
  <div class="sar vitrin">
    %(kina_gorsel)s
    <div>
      %(bs)s
      <p class="ust-yazi">Kına organizasyonu</p>
      <h2>Kına geceniz <em>hazır</em>, siz sadece gelin</h2>
      <p>Kına tahtı ve cibinliğinden bindallıya, kına kızlarından davul şova kadar 16 kalemlik
        paketimizle geceyi baştan sona biz planlıyoruz.</p>
      <div class="eylem"><a class="btn" href="/kina-organizasyonu/">Paketin tamamı</a></div>
    </div>
  </div>
</section>

<section class="bolum bolum--pudra">
  <div class="sar">
    %(galeri_ust)s
    %(galeri)s
    <div class="eylem eylem--orta"><a class="btn btn--cizgi" href="/salon/">Tüm fotoğraflar</a></div>
  </div>
</section>

<section class="bolum">
  <div class="sar sar--dar">
    %(sss_ust)s
    <div class="sss-liste">%(sss)s</div>
  </div>
</section>
%(cta)s""" % {
        "kahraman": resim("gelin-yolu", "Kırmızı halı gelin yolu ve çiçekli beyaz sütunlar",
                          boyut="100vw", yukle="eager", oncelik=True),
        "kur": SALON["kurulus_salon"], "kurf": SALON["kurulus_firma"],
        "kap": SALON["kapasite"], "yil": YIL_TECRUBE, "wp": WHATSAPP,
        "olcu": olcu_seridi(),
        "hikaye": resim("nikah-masasi", "Beyaz ve altın detaylı nikâh masası köşesi"),
        "bs": baklava(sol=True),
        "org_ust": bolum_ust("Organizasyonlar", "Her kutlamaya <em>uygun bir düzen</em>",
                             "Yemekli ya da kokteyl; salonu ister bütün olarak, ister %s "
                             "ayrı girişlerle ikiye bölerek kullanın." % SALON["bolunme"]),
        "kartlar": organizasyon_kartlari(),
        "kina_gorsel": kina_gorselleri(),
        "galeri_ust": bolum_ust("Salon", "Salondan <em>kareler</em>"),
        "galeri": galeri_html(GALERI[:7]),
        "sss_ust": bolum_ust("Sık sorulanlar", "Aklınızdaki <em>sorular</em>"),
        "sss": sss_govde, "cta": cta(),
    }
    return sayfa("Pınar Düğün Salonu | Bahçelievler Düğün, Kına ve Davet Salonu",
                 "Bahçelievler Kocasinan'da %d kişilik düğün salonu. Düğün, nişan, kına, "
                 "sünnet ve davetler için %d yıllık tecrübe. Tel: %s"
                 % (SALON["kapasite"], YIL_TECRUBE, SALON["tel_cep_yazi"]),
                 "/", govde, [ld_mekan(), sss_ld], "/", onyukle="gelin-yolu")


def salon_sayfasi():
    kb, kld = kirinti([("Ana sayfa", "/"), ("Salon", None)])
    govde = """
<div class="sar">%s</div>
%s
<div class="sar ic-gorsel">%s</div>
%s
<section class="bolum">
  <div class="sar">
    %s
    %s
  </div>
</section>
<section class="bolum bolum--pudra">
  <div class="sar">
    %s
    %s
  </div>
</section>
%s""" % (
        kb,
        ic_baslik("Salon", "%d kişilik, <em>ikiye bölünebilen</em> salon" % SALON["kapasite"],
                  "İsteğe göre %s olmak üzere ayrı girişlerle ikiye ayrılır. Klima ve "
                  "havalandırma, profesyonel sahne ve ses düzeni, geniş pist."
                  % SALON["bolunme"]),
        resim("salon-genel", "Salonun genel görünümü", boyut="100vw", yukle="eager"),
        olcu_seridi(),
        bolum_ust("Galeri", "Salonu <em>yakından</em> görün",
                  "Fotoğrafa dokunarak büyütebilirsiniz."),
        galeri_html(GALERI),
        bolum_ust("Salon özellikleri", "Rahat bir gece için <em>gereken her şey</em>"),
        hizmet_gruplari(("Salon", "Servis", "Misafir rahatlığı")),
        cta("Salonu yerinde görün",
            "Gelmeden önce arayıp gün belirlerseniz salonu ve düzeni size gösteririz."))
    return sayfa("Salon ve Fotoğraflar | Pınar Düğün Salonu Bahçelievler",
                 "Pınar Düğün Salonu'ndan fotoğraflar: %d kişilik salon, gelin yolu, nikâh "
                 "masası, pist ve kına tahtı. Bahçelievler Kocasinan." % SALON["kapasite"],
                 "/salon/", govde, [kld, ld_mekan()], "/salon/", onyukle="salon-genel")


def kina_sayfasi():
    kb, kld = kirinti([("Ana sayfa", "/"), ("Kına organizasyonu", None)])
    hizmet_ld = ('{"@context":"https://schema.org","@type":"Service",'
                 '"name":"Kına gecesi organizasyonu","serviceType":"Kına organizasyonu",'
                 '"provider":{"@id":"%s/#mekan"},"areaServed":"Bahçelievler, İstanbul",'
                 '"description":"16 kalemlik kına gecesi paketi: kına tahtı ve cibinliği, '
                 'gelin bindallısı, kına kızları, davul şov ve müzik."}' % SITE)
    govde = """
<div class="sar">%s</div>
%s
<section class="bolum bolum--ust-yok">
  <div class="sar vitrin">
    %s
    <div>
      %s
      <p class="ust-yazi">Paketin içinde</p>
      <h2>16 kalem, <em>tek plan</em></h2>
      <ul class="liste liste--iki">%s</ul>
    </div>
  </div>
</section>
<section class="bolum bolum--pudra">
  <div class="sar sar--dar">
    %s
    <ul class="zaman">
      <li><b>01</b><span>Misafirler karşılama masasında ağırlanır, arkadaş kaftanları ve kına taçları dağıtılır.</span></li>
      <li><b>02</b><span>Gelin bindallısıyla, kına kızları eşliğinde ve davul şovla salona çıkar.</span></li>
      <li><b>03</b><span>Gelin kına tahtına oturur; tef ve halay mendilleriyle eğlence başlar.</span></li>
      <li><b>04</b><span>El gülleri ve mumlarla kına tepsisi getirilir, kına yakılır.</span></li>
    </ul>
  </div>
</section>
%s""" % (
        kb,
        ic_baslik("Kına organizasyonu", "Kına geceniz <em>hazır</em>",
                  "Kına tahtından bindallıya, davul şovdan müziğe kadar geceyi baştan sona "
                  "biz planlıyoruz. Size yalnızca misafirlerinizi çağırmak kalıyor."),
        kina_gorselleri(), baklava(sol=True),
        "".join("<li>%s</li>" % kacir(k) for k in KINA_PAKETI),
        bolum_ust("Gecenin akışı", "Kına gecesi <em>nasıl ilerler</em>"),
        cta("Kına gecenizi planlayalım",
            "Tarih ve kişi sayısını yazın; paketi ve boş günleri birlikte konuşalım."))
    return sayfa("Kına Organizasyonu Bahçelievler | Pınar Düğün Salonu",
                 "Bahçelievler'de kına gecesi organizasyonu: kına tahtı, bindallı, kına "
                 "kızları, davul şov ve müzik dahil 16 kalemlik hazır paket.",
                 "/kina-organizasyonu/", govde, [kld, hizmet_ld], "/kina-organizasyonu/")


def menuler_sayfasi():
    kb, kld = kirinti([("Ana sayfa", "/"), ("Menüler", None)])
    govde = """
<div class="sar">%s</div>
%s
<section class="bolum bolum--ust-yok">
  <div class="sar">
    %s
    <div class="ekler">%s</div>
  </div>
</section>
%s""" % (
        kb,
        ic_baslik("Menüler", "Yemekli ya da <em>kokteyl</em>",
                  "İki yemekli ve üç pastalı menümüz var. İsteğe göre döner, ızgara ve ordövr "
                  "tabağıyla genişletebilirsiniz."),
        menu_kartlari(), "".join("<p>%s</p>" % kacir(e) for e in MENU_EKLER),
        cta("Menünüzü birlikte seçelim",
            "Kişi sayısına ve tarihe göre fiyat bilgisi için arayın ya da yazın."))
    return sayfa("Düğün Menüleri | Pınar Düğün Salonu Bahçelievler",
                 "Pınar Düğün Salonu menüleri: kırmızı et ve beyaz et yemekli menüler, "
                 "pastalı ve dondurmalı pasta kokteyl menüleri. Bahçelievler.",
                 "/menuler/", govde, [kld], "/menuler/")


def hizmetler_sayfasi():
    kb, kld = kirinti([("Ana sayfa", "/"), ("Hizmetler", None)])
    govde = """
<div class="sar">%s</div>
%s
<div class="sar ic-gorsel">%s</div>
<section class="bolum bolum--ust-yok">
  <div class="sar">%s</div>
</section>
<section class="bolum bolum--pudra">
  <div class="sar">
    %s
    %s
  </div>
</section>
%s""" % (
        kb,
        ic_baslik("Hizmetler", "Salonda <em>neler var</em>",
                  "Süslemeden fotoğrafa, gösteriden misafir rahatlığına kadar salonumuzda "
                  "sunduğumuz hizmetler."),
        resim("cicekli-sutunlar", "Gelin yolunu çevreleyen çiçek sütunları",
              boyut="100vw", yukle="eager"),
        hizmet_gruplari(),
        bolum_ust("Organizasyonlar", "Hangi kutlama <em>olursa olsun</em>"),
        organizasyon_kartlari(), cta())
    return sayfa("Hizmetler | Pınar Düğün Salonu Bahçelievler",
                 "Gelin yolu ve nikâh masası süsleme, full çekim kamera, aile fotoğrafı, "
                 "semazen, davul zurna, sinevizyon, bebek bakım odası ve mescit.",
                 "/hizmetler/", govde, [kld], "/hizmetler/", onyukle="cicekli-sutunlar")


def iletisim_sayfasi():
    kb, kld = kirinti([("Ana sayfa", "/"), ("İletişim", None)])
    govde = """
<div class="sar">%(kb)s</div>
%(baslik)s
<section class="bolum bolum--ust-yok">
  <div class="sar iletisim">
    <div>
      <div class="iletisim__blok"><p class="iletisim__etiket">Cep / WhatsApp</p><a href="tel:%(tc)s">%(tcy)s</a></div>
      <div class="iletisim__blok"><p class="iletisim__etiket">Sabit hat</p><a href="tel:%(ts)s">%(tsy)s</a></div>
      <div class="iletisim__blok"><p class="iletisim__etiket">E-posta</p><a href="mailto:%(ep)s">%(ep)s</a></div>
      <div class="iletisim__blok"><p class="iletisim__etiket">Adres</p>
        <address>%(adres)s<br>%(bina)s<br>%(ilce)s / %(il)s</address></div>
      <div class="eylem">
        <a class="btn" href="%(wp)s" target="_blank" rel="noopener">WhatsApp'tan yazın</a>
        <a class="btn btn--cizgi" href="%(harita)s" target="_blank" rel="noopener">Yol tarifi</a>
      </div>
    </div>
    <iframe class="harita" src="%(gomme)s" loading="lazy"
      referrerpolicy="no-referrer-when-downgrade" title="Pınar Düğün Salonu harita konumu"></iframe>
  </div>
</section>""" % {
        "kb": kb,
        "baslik": ic_baslik("İletişim", "Bize <em>ulaşın</em>",
                            "Fiyat ve boş tarih bilgisi için arayın ya da WhatsApp'tan yazın. "
                            "Salonu görmek isterseniz gün belirleyelim."),
        "tc": SALON["tel_cep"], "tcy": SALON["tel_cep_yazi"], "ts": SALON["tel_sabit"],
        "tsy": SALON["tel_sabit_yazi"], "ep": SALON["eposta"], "adres": SALON["adres_satir"],
        "bina": SALON["adres_bina"], "ilce": SALON["ilce"], "il": SALON["il"],
        "wp": WHATSAPP, "harita": HARITA_LINK, "gomme": HARITA_GOMME,
    }
    return sayfa("İletişim ve Yol Tarifi | Pınar Düğün Salonu Bahçelievler",
                 "Pınar Düğün Salonu iletişim: %s, %s. Kocasinan Merkez Mah. Mimar Sinan Cad. "
                 "No:7 Bahçelievler/İstanbul." % (SALON["tel_cep_yazi"], SALON["tel_sabit_yazi"]),
                 "/iletisim/", govde, [kld, ld_mekan()], "/iletisim/")


def kvkk_sayfasi():
    kb, kld = kirinti([("Ana sayfa", "/"), ("KVKK aydınlatma metni", None)])
    govde = """
<div class="sar">%s</div>
%s
<section class="bolum bolum--ust-yok">
  <div class="sar sar--dar yasal">
    <p><b>Veri sorumlusu:</b> %s, %s %s, %s/%s.</p>
    <p>Bu site üzerinden form ile kişisel veri toplanmaz. Bizi telefonla, WhatsApp üzerinden
      ya da e-postayla aradığınızda paylaştığınız ad, telefon numarası ve organizasyon
      bilgileri yalnızca talebinizi yanıtlamak ve rezervasyonunuzu yürütmek için kullanılır;
      üçüncü kişilerle reklam amacıyla paylaşılmaz.</p>
    <p>6698 sayılı Kişisel Verilerin Korunması Kanunu'nun 11. maddesi kapsamındaki
      haklarınız için <a href="mailto:%s">%s</a> adresine yazabilirsiniz.</p>
    <p>İletişim sayfasındaki harita Google tarafından sunulur ve Google'ın kendi gizlilik
      koşullarına tabidir.</p>
  </div>
</section>""" % (kb, ic_baslik("Yasal", "KVKK <em>aydınlatma metni</em>"),
                 SALON["tam_ad"], SALON["adres_satir"], SALON["adres_bina"],
                 SALON["ilce"], SALON["il"], SALON["eposta"], SALON["eposta"])
    return sayfa("KVKK Aydınlatma Metni | Pınar Düğün Salonu",
                 "Pınar Düğün Salonu kişisel verilerin korunması aydınlatma metni.",
                 "/kvkk/", govde, [kld], "")


def dort_yuz_dort():
    govde = """%s
<div class="sar" style="padding-bottom:110px">
  <div class="eylem eylem--orta">
    <a class="btn" href="/">Ana sayfa</a>
    <a class="btn btn--cizgi" href="/salon/">Salon</a>
  </div>
</div>""" % ic_baslik("404", "Sayfa <em>bulunamadı</em>",
                       "Aradığınız sayfa taşınmış olabilir. Salonumuzu ana sayfadan "
                       "inceleyebilirsiniz.")
    return sayfa("Sayfa bulunamadı | Pınar Düğün Salonu", "Aradığınız sayfa bulunamadı.",
                 "/404.html", govde, [], "", robots="noindex, follow")


# ---------------------------------------------------------------------------
# DESTEK DOSYALARI
# ---------------------------------------------------------------------------

ADRESLER = ["/", "/salon/", "/kina-organizasyonu/", "/menuler/", "/hizmetler/",
            "/iletisim/", "/kvkk/"]

# Eski WordPress sitesinin adresleri -> yeni karsiliklari.
# /hizmetler/ ve /menuler/ iki sitede de ayni yolda, yonlendirme gerekmez.
ESKI_ADRESLER = {
    "/kurumsal/": "/",
    "/fotograflar/": "/salon/",
    "/360-sanal-tur/": "/salon/",
    "/kina-organizasyon/": "/kina-organizasyonu/",
    "/bize-ulasin/": "/iletisim/",
}


def yonlendirme(hedef):
    """GitHub Pages sunucu tarafi yonlendirme yapmaz; meta refresh + canonical."""
    tam = SITE + hedef
    return """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sayfa taşındı | Pınar Düğün Salonu</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="%(tam)s">
<meta http-equiv="refresh" content="0; url=%(hedef)s">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;font:17px/1.6 system-ui,sans-serif;color:#151413;background:#fff;padding:24px;text-align:center}a{color:#8A6A3C}</style>
</head>
<body>
<p>Bu sayfa taşındı. <a href="%(hedef)s">Yeni sayfaya gidin</a>.</p>
<script>location.replace('%(hedef)s');</script>
</body>
</html>
""" % {"tam": tam, "hedef": hedef}


def sitemap():
    s = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for y in ADRESLER:
        oncelik = "1.0" if y == "/" else ("0.3" if y == "/kvkk/" else "0.8")
        s += ["  <url>", "    <loc>%s%s</loc>" % (SITE, y),
              "    <lastmod>%s</lastmod>" % BUGUN, "    <priority>%s</priority>" % oncelik,
              "  </url>"]
    s.append("</urlset>")
    return "\n".join(s) + "\n"


def robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE


def llms():
    return "\n".join([
        "# %s" % SALON["tam_ad"],
        "",
        "> Bahçelievler Kocasinan'da %d kişilik düğün, nişan, kına, sünnet ve davet "
        "salonu. %d yılından beri hizmet veriyor (önce Has Pınar Yemek, %d'ten itibaren "
        "düğün salonu)." % (SALON["kapasite"], SALON["kurulus_firma"], SALON["kurulus_salon"]),
        "",
        "Salon isteğe göre %s olmak üzere ayrı girişlerle ikiye bölünebilir. Klima, "
        "havalandırma, profesyonel sahne ve ses düzeni vardır." % SALON["bolunme"],
        "",
        "Adres: %s" % HARITA_ADRES,
        "Telefon: %s, %s" % (SALON["tel_cep_yazi"], SALON["tel_sabit_yazi"]),
        "E-posta: %s" % SALON["eposta"],
        "Instagram: %s" % SALON["instagram"],
        "",
        "## Sayfalar",
        "",
        "- [Ana sayfa](%s/): salon, organizasyonlar, sık sorulanlar." % SITE,
        "- [Salon](%s/salon/): fotoğraflar ve salon özellikleri." % SITE,
        "- [Kına organizasyonu](%s/kina-organizasyonu/): 16 kalemlik kına gecesi paketi." % SITE,
        "- [Menüler](%s/menuler/): iki yemekli, üç pastalı menü." % SITE,
        "- [Hizmetler](%s/hizmetler/): süsleme, fotoğraf, gösteri ve misafir hizmetleri." % SITE,
        "- [İletişim](%s/iletisim/): telefon, adres, harita." % SITE,
        "",
        "Fiyatlar tarih, kişi sayısı ve menüye göre değiştiği için sitede yayımlanmıyor; "
        "telefonla ya da WhatsApp'tan bilgi veriliyor.",
        "",
    ])


# ---------------------------------------------------------------------------
# CALISTIR
# ---------------------------------------------------------------------------

def main():
    yaz("assets/stil.css", STIL)
    yaz("assets/site.js", BETIK)
    yaz("favicon.svg", favicon())
    yaz("index.html", ana_sayfa())
    yaz("salon/index.html", salon_sayfasi())
    yaz("kina-organizasyonu/index.html", kina_sayfasi())
    yaz("menuler/index.html", menuler_sayfasi())
    yaz("hizmetler/index.html", hizmetler_sayfasi())
    yaz("iletisim/index.html", iletisim_sayfasi())
    yaz("kvkk/index.html", kvkk_sayfasi())
    yaz("404.html", dort_yuz_dort())
    for eski, yeni in ESKI_ADRESLER.items():
        yaz("%sindex.html" % eski.lstrip("/"), yonlendirme(yeni))
    yaz("sitemap.xml", sitemap())
    yaz("robots.txt", robots())
    yaz("llms.txt", llms())
    # GitHub Pages
    yaz("CNAME", "pinardugundavet.com\n")
    yaz(".nojekyll", "")
    print("Uretilen dosya: %d" % len(URETILEN))
    for y in URETILEN:
        print("  " + y)


if __name__ == "__main__":
    main()
