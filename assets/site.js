/* Progressive enhancements only: all content and ordinary links work without JS. */
document.documentElement.classList.add('js');
const rail = document.querySelector('.rail');
const menu = document.querySelector('.menu-toggle');
if (rail && menu) {
  menu.hidden = false;
  const closeMenu = () => {
    rail.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
  };
  menu.addEventListener('click', () => {
    const expanded = !rail.classList.contains('is-open');
    rail.classList.toggle('is-open', expanded);
    menu.setAttribute('aria-expanded', String(expanded));
  });
  rail.querySelectorAll('.site-nav a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && rail.classList.contains('is-open')) {
      closeMenu();
      menu.focus();
    }
  });
}
const languageLinks = document.querySelectorAll('[data-language-link]');
const syncLanguageHash = () => languageLinks.forEach(link => {
  link.hash = location.hash;
});
syncLanguageHash();
window.addEventListener('hashchange', syncLanguageHash);
const copyButton = document.querySelector('[data-copy-email]');
if (copyButton && navigator.clipboard && window.isSecureContext) {
  copyButton.hidden = false;
  copyButton.addEventListener('click', async () => {
    const feedback = document.querySelector('.copy-feedback');
    try {
      await navigator.clipboard.writeText(copyButton.dataset.copyEmail);
      feedback.textContent = copyButton.dataset.success;
    } catch {
      feedback.textContent = copyButton.dataset.failure;
    }
  });
}
const sectionLinks = [...document.querySelectorAll('.site-nav a[href^="#"]')];
if ('IntersectionObserver' in window && sectionLinks.length) {
  const sections = sectionLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (!visible.length) return;
    const id = visible[0].target.id;
    sectionLinks.forEach(link => {
      if (link.hash === '#' + id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-10% 0px -55% 0px', threshold: 0 });
  sections.forEach(section => observer.observe(section));
}
const printButton = document.querySelector('[data-print]');
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener('click', () => window.print());
}
