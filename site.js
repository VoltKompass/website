// VoltKompass – gemeinsame Seitenlogik (Navigation, Lesefortschritt, Sprungleiste)
(function () {
  const nav = document.querySelector('.nav');
  const progress = document.querySelector('.read-progress');
  const article = document.querySelector('main article');

  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 12);
    if (progress && article) {
      const start = article.offsetTop;
      const total = article.offsetHeight - window.innerHeight;
      const ratio = total > 0 ? Math.min(Math.max((window.scrollY - start) / total, 0), 1) : 0;
      progress.style.transform = `scaleX(${ratio})`;
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  // Sprungleiste: aktiven Abschnitt hervorheben
  const jumpLinks = [...document.querySelectorAll('.article-jump a[href^="#"]')];
  const targets = jumpLinks
    .map(link => document.getElementById(decodeURIComponent(link.hash.slice(1))))
    .filter(Boolean);
  if (targets.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        jumpLinks.forEach(link => {
          const active = link.hash.slice(1) === entry.target.id;
          link.classList.toggle('is-active', active);
          if (active) link.scrollIntoView({ block: 'nearest', inline: 'nearest' });
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    targets.forEach(t => observer.observe(t));
  }
})();
