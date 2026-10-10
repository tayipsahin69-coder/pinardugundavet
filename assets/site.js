(function () {
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
