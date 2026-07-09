document.documentElement.classList.add('rm-js');

const SERVICE_SLUGS = [
  'comprehensive-roof-installations',
  'expert-roof-repairs-and-maintenance',
  'free-roof-inspections-and-consultations',
  'storm-damage-repair-specialists',
  'gutter-installation-and-cleaning',
  'skylight-installation-and-repair',
];

const LOCATION_SLUGS = [
  'roofing-company-dunedin-florida',
  'roofing-company-clearwater-florida',
  'roofing-company-st-petersburg-florida',
  'roofing-company-largo-florida',
  'roofing-company-palm-harbor-florida',
  'roofing-company-seminole-florida',
  'roofing-company-safety-harbor-florida',
  'roofing-company-tampa-florida',
  'roofing-company-new-port-richey-florida',
  'roofing-company-pinellas-county-florida',
  'roofing-company-pasco-county-florida',
  'roofing-company-hernando-county-florida',
  'roofing-company-hillsborough-county-florida',
  'roofing-company-manatee-county-florida',
];

const BLOG_POST_SLUGS = [
  'october-roofing-season-in-tampa-bay-why-fall-is-the-best-time-to-schedule-your-roof-work',
  'the-roof-monsters-way-what-sets-our-roofing-company-apart',
  'how-to-prepare-your-roof-for-floridas-hurricane-season',
];

function getSiteBase() {
  if (typeof window.__RM_BASE__ === 'string' && window.__RM_BASE__) {
    return window.__RM_BASE__;
  }
  const path = window.location.pathname;
  const marker = '/roof-monsters/';
  const idx = path.indexOf(marker);
  return idx >= 0 ? path.slice(0, idx + marker.length) : '/';
}

function getIncludeBase() {
  const script = document.querySelector('script[src*="includes.js"]');
  if (!script || !script.src) {
    return `${window.location.origin}${getSiteBase()}`;
  }
  return script.src.replace(/includes\.js(?:\?.*)?$/, '');
}

function normalizeSitePath(pathname) {
  let path = pathname || '/';
  const siteBase = getSiteBase();
  if (siteBase !== '/' && path.startsWith(siteBase.replace(/\/$/, ''))) {
    path = path.slice(siteBase.length - 1);
    if (!path.startsWith('/')) path = `/${path}`;
  }
  if (path.endsWith('/index.html')) {
    path = path.slice(0, -'index.html'.length);
  } else if (path.endsWith('.html')) {
    path = `${path.slice(0, -5)}/`;
  }
  if (!path.startsWith('/')) path = `/${path}`;
  if (path !== '/' && !path.endsWith('/')) path = `${path}/`;
  return path;
}

function pathToNavId(path) {
  if (path === '/') return 'home';
  if (path === '/blog/' || BLOG_POST_SLUGS.some((slug) => path === `/${slug}/`)) return 'blog';
  if (path === '/services/' || path.startsWith('/services/')) return 'services';
  if (
    path === '/about-us/locations-we-serve/'
    || LOCATION_SLUGS.some((slug) => path === `/about-us/locations-we-serve/${slug}/`)
  ) return 'service-areas';
  return path.replace(/^\/|\/$/g, '');
}

function getCurrentNavPage() {
  return pathToNavId(normalizeSitePath(window.location.pathname));
}

function applyNavActive() {
  const currentPath = normalizeSitePath(window.location.pathname);
  const page = getCurrentNavPage();

  document.querySelectorAll(
    '.site-nav > a, .nav-dropdown-menu a, .mobile-nav-links > a, .mobile-services-sub a, .mobile-areas-sub a',
  ).forEach((link) => {
    link.classList.remove('active');
    link.removeAttribute('aria-current');
    const href = link.getAttribute('href') || '';
    if (!href || href.startsWith('tel:') || href.startsWith('#')) return;

    let linkPath;
    try {
      linkPath = normalizeSitePath(new URL(href, document.baseURI).pathname);
    } catch {
      return;
    }

    const isMatch = linkPath === currentPath
      || (page === 'services' && linkPath === '/services/' && currentPath.startsWith('/services/'))
      || (page === 'blog' && linkPath === '/blog/' && BLOG_POST_SLUGS.some((slug) => currentPath === `/${slug}/`))
      || (page === 'service-areas' && linkPath === '/about-us/locations-we-serve/' && currentPath === '/about-us/locations-we-serve/');

    if (isMatch) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });
}

const INCLUDE_VERSION = '20260709c';

async function fetchInclude(path) {
  const url = path.startsWith('http')
    ? path
    : `${getIncludeBase()}${path.replace(/^\//, '')}?v=${INCLUDE_VERSION}`;
  const response = await fetch(url, { cache: 'no-store' });
  if (!response.ok) {
    throw new Error(`Failed to load ${url} (${response.status})`);
  }
  return response.text();
}

function injectInclude(slot, html) {
  if (!slot || !html) return;
  slot.insertAdjacentHTML('afterend', html.trim());
  slot.remove();
}

async function loadPartialIncludes() {
  const slots = Array.from(document.querySelectorAll('[data-partial]'));
  for (const slot of slots) {
    const partialPath = slot.getAttribute('data-partial');
    if (!partialPath) continue;
    const html = await fetchInclude(partialPath);
    injectInclude(slot, html);
  }
}

async function loadSiteIncludes() {
  const headerSlot = document.getElementById('site-header-include');
  const footerSlot = document.getElementById('site-footer-include');
  const tasks = [];

  if (headerSlot) {
    tasks.push(
      fetchInclude('header.html').then((html) => injectInclude(headerSlot, html)),
    );
  }

  if (footerSlot) {
    tasks.push(
      fetchInclude('footer.html').then((html) => injectInclude(footerSlot, html)),
    );
  }

  await Promise.all(tasks);
  await loadPartialIncludes();

  if (!document.querySelector('.site-header')) {
    console.warn('Site header was not injected. Check header.html and includes.js.');
    return;
  }

  applyNavActive();
  document.dispatchEvent(new CustomEvent('site:includes-loaded'));
  if (typeof window.rmInitEstimateForms === 'function') {
    window.rmInitEstimateForms();
  }
}

function initSiteIncludes() {
  loadSiteIncludes().catch((error) => {
    console.error('Site includes failed to load:', error);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initSiteIncludes);
} else {
  initSiteIncludes();
}
