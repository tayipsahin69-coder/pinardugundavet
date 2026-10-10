(function () {
  document.documentElement.classList.add('js');
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

  // ---- kahraman slayti ----
  var hareketAz = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var slaytlar = document.querySelectorAll('.slayt');
  if (slaytlar.length > 1 && !hareketAz) {
    var s = 0;
    setInterval(function () {
      slaytlar[s].classList.remove('aktif');
      s = (s + 1) % slaytlar.length;
      slaytlar[s].classList.add('aktif');
    }, 6500);
  }

  // ---- belirme + sayac (scroll dinleyici; IntersectionObserver'a bagli degil) ----
  var belirler = [].slice.call(document.querySelectorAll('.belir'));
  var sayilar = [].slice.call(document.querySelectorAll('[data-sayi]'));
  function say(el) {
    var hedef = +el.getAttribute('data-sayi'), t0 = Date.now(), sure = 1600;
    if (hareketAz) return;
    (function adim() {
      var o = Math.min(1, (Date.now() - t0) / sure);
      el.textContent = Math.round(hedef * (1 - Math.pow(1 - o, 3)));
      if (o < 1) setTimeout(adim, 30);
    })();
  }
  function bak() {
    var h = window.innerHeight || document.documentElement.clientHeight;
    if (!h) { belirler.forEach(function (e) { e.classList.add('gorundu'); }); belirler = []; return; }
    belirler = belirler.filter(function (e) {
      if (e.getBoundingClientRect().top < h * 0.9) { e.classList.add('gorundu'); return false; }
      return true;
    });
    sayilar = sayilar.filter(function (e) {
      if (e.getBoundingClientRect().top < h * 0.95) { say(e); return false; }
      return true;
    });
  }
  var bekle = false;
  window.addEventListener('scroll', function () {
    if (bekle) return; bekle = true;
    setTimeout(function () { bekle = false; bak(); }, 80);
  }, { passive: true });
  window.addEventListener('resize', bak);
  bak();

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
