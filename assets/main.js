// Both language versions render fully without JavaScript.
// Preserve the current section when changing language.
document.querySelectorAll('.language-switch a:not([aria-current])').forEach(link => {
  const base = link.getAttribute('href');
  const sync = () => { link.href = base + window.location.hash; };
  sync();
  window.addEventListener('hashchange', sync);
});

// Indicate the section currently being read in the page navigation.
const sectionLinks = [...document.querySelectorAll('.section-nav a')];
const sections = [...document.querySelectorAll('main > section[id]')];
let scheduled = false;
function updateSection() {
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= 180) current = section;
  }
  if (current) sectionLinks.forEach(link => {
    if (link.hash === '#' + current.id) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  scheduled = false;
}
window.addEventListener('scroll', () => {
  if (!scheduled) { scheduled = true; requestAnimationFrame(updateSection); }
}, { passive: true });
window.addEventListener('resize', updateSection);
updateSection();
