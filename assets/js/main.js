/* =============================================
   Roof Monsters — main.js
   Hero slider (Ken Burns) · Mobile nav
   Testimonial carousel · CountUp · Form
============================================= */

document.documentElement.classList.add('rm-js');

function initCurrentYear() {
  document.querySelectorAll('#current-year').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
}

function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header || header.dataset.bound === 'true') return;
  header.dataset.bound = 'true';

  window.addEventListener(
    'scroll',
    () => header.classList.toggle('scrolled', window.scrollY > 40),
    { passive: true },
  );
}

function initSiteNav() {
  if (document.body.dataset.siteNavBound === 'true') return;
  document.body.dataset.siteNavBound = 'true';

  function closeAllDropdowns() {
    document.querySelectorAll('.nav-dropdown-btn').forEach((btn) => {
      btn.setAttribute('aria-expanded', 'false');
    });
  }

  document.querySelectorAll('.nav-dropdown-wrap').forEach((wrap) => {
    const dropdownBtn = wrap.querySelector('.nav-dropdown-btn');
    const dropdownMenu = wrap.querySelector('.nav-dropdown-menu');
    if (!dropdownBtn || !dropdownMenu) return;

    dropdownBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const expanded = dropdownBtn.getAttribute('aria-expanded') === 'true';
      closeAllDropdowns();
      dropdownBtn.setAttribute('aria-expanded', String(!expanded));
    });

    dropdownMenu.addEventListener('click', (e) => e.stopPropagation());
  });

  function closeAllAreaSubmenus() {
    document.querySelectorAll('.nav-area-group-btn').forEach((btn) => {
      btn.setAttribute('aria-expanded', 'false');
    });
  }

  document.querySelectorAll('.nav-area-group').forEach((group) => {
    const btn = group.querySelector('.nav-area-group-btn');
    const submenu = group.querySelector('.nav-area-submenu');
    if (!btn || !submenu) return;

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      closeAllAreaSubmenus();
      btn.setAttribute('aria-expanded', String(!expanded));
    });

    submenu.addEventListener('click', (e) => e.stopPropagation());
  });

  document.addEventListener('click', () => {
    closeAllDropdowns();
    closeAllAreaSubmenus();
  });

  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileNav = document.getElementById('mobile-nav');
  const navOverlay = document.getElementById('nav-overlay');
  const mobileNavClose = document.getElementById('mobile-nav-close');
  const mobileServToggle = document.getElementById('mobile-services-toggle');
  const mobileServicesSub = document.getElementById('mobile-services-sub');
  const mobileAreasToggle = document.getElementById('mobile-areas-toggle');
  const mobileAreasSub = document.getElementById('mobile-areas-sub');

  function openMobileNav() {
    if (!mobileNav || !navOverlay || !hamburgerBtn) return;
    mobileNav.classList.add('is-open');
    navOverlay.classList.add('is-open');
    hamburgerBtn.classList.add('is-open');
    hamburgerBtn.setAttribute('aria-expanded', 'true');
    mobileNav.setAttribute('aria-hidden', 'false');
    mobileNav.removeAttribute('inert');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileNav() {
    if (!mobileNav || !navOverlay || !hamburgerBtn) return;
    mobileNav.classList.remove('is-open');
    navOverlay.classList.remove('is-open');
    hamburgerBtn.classList.remove('is-open');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    mobileNav.setAttribute('aria-hidden', 'true');
    mobileNav.setAttribute('inert', '');
    document.body.style.overflow = '';
  }

  if (hamburgerBtn) {
    hamburgerBtn.addEventListener('click', () => {
      if (hamburgerBtn.classList.contains('is-open')) {
        closeMobileNav();
      } else {
        openMobileNav();
      }
    });
  }

  if (mobileNavClose) mobileNavClose.addEventListener('click', closeMobileNav);
  if (navOverlay) navOverlay.addEventListener('click', closeMobileNav);

  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMobileNav);
    });
  }

  if (mobileServToggle && mobileServicesSub) {
    mobileServToggle.addEventListener('click', () => {
      const open = mobileServToggle.classList.toggle('is-open');
      mobileServicesSub.classList.toggle('is-open', open);
      mobileServToggle.setAttribute('aria-expanded', String(open));
    });
  }

  if (mobileAreasToggle && mobileAreasSub) {
    mobileAreasToggle.addEventListener('click', () => {
      const open = mobileAreasToggle.classList.toggle('is-open');
      mobileAreasSub.classList.toggle('is-open', open);
      mobileAreasToggle.setAttribute('aria-expanded', String(open));
    });
  }

  document.querySelectorAll('.mobile-area-county-toggle').forEach((toggle) => {
    toggle.addEventListener('click', () => {
      const targetId = toggle.getAttribute('data-target');
      const sub = targetId ? document.getElementById(targetId) : null;
      if (!sub) return;
      const open = toggle.classList.toggle('is-open');
      sub.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
    });
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) closeMobileNav();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMobileNav();
  });
}

function initMobileNav() {
  initSiteNav();
}

function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');
  if (!slides.length) return;

  let current = 0;
  let slideInterval;

  function goTo(index) {
    const prevBg = slides[current].querySelector('.hero-slide-bg');
    slides[current].classList.remove('active');
    if (dots[current]) dots[current].classList.remove('active');
    if (prevBg) {
      prevBg.style.animation = 'none';
      void prevBg.offsetWidth;
    }

    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    if (dots[current]) dots[current].classList.add('active');

    const newBg = slides[current].querySelector('.hero-slide-bg');
    if (newBg) {
      newBg.style.animation = 'none';
      void newBg.offsetWidth;
      newBg.style.animation = '';
    }
  }

  function startSlider() {
    slideInterval = setInterval(() => goTo(current + 1), 6000);
  }

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      clearInterval(slideInterval);
      goTo(i);
      startSlider();
    });
  });

  startSlider();
}

function initTestimonialCarousel() {
  const track = document.getElementById('testimonial-track');
  const counter = document.getElementById('testimonial-counter');
  const prevBtn = document.getElementById('testimonial-prev');
  const nextBtn = document.getElementById('testimonial-next');

  if (!track) return;

  const cards = track.querySelectorAll('.testimonial-card');
  let tCurrent = 0;
  const total = cards.length;

  function getPerView() {
    return window.innerWidth < 768 ? 1 : 3;
  }

  function updateCarousel() {
    const pv = getPerView();
    const gap = 28;
    const cardW = cards[0].offsetWidth;
    const shift = (cardW + gap) * tCurrent;
    track.style.transform = `translateX(-${shift}px)`;
    const maxIndex = Math.max(0, total - pv);
    if (counter) counter.textContent = `${tCurrent + 1} / ${Math.ceil(total / pv)}`;
    if (prevBtn) prevBtn.disabled = tCurrent === 0;
    if (nextBtn) nextBtn.disabled = tCurrent >= maxIndex;
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (tCurrent > 0) {
        tCurrent--;
        updateCarousel();
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      const maxIndex = Math.max(0, total - getPerView());
      if (tCurrent < maxIndex) {
        tCurrent++;
        updateCarousel();
      }
    });
  }

  window.addEventListener('resize', () => {
    tCurrent = 0;
    updateCarousel();
  });
  updateCarousel();
}

function formatStatText(value, suffix) {
  return value.toLocaleString() + (suffix || '');
}

function animateCountUp(el) {
  const target = parseInt(el.dataset.target, 10);
  if (Number.isNaN(target)) return;
  const suffix = el.dataset.suffix ?? ' +';
  const duration = parseInt(el.dataset.duration, 10) || 1400;
  const startTime = performance.now();

  el.textContent = formatStatText(0, suffix);

  function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
  }

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeOutQuart(progress);
    const value = Math.floor(eased * target);
    el.textContent = formatStatText(value, suffix);

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = formatStatText(target, suffix);
    }
  }

  requestAnimationFrame(update);
}

function initCountUp() {
  const statSelectors = '.stat-num[data-target], .mini-stat-num[data-target]';
  const sections = document.querySelectorAll('[data-stats-section], .mini-stats-banner[data-countup]');

  sections.forEach((section) => {
    const statNums = section.querySelectorAll(statSelectors);
    if (!statNums.length) return;

    let countupFired = false;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !countupFired) {
          countupFired = true;
          statNums.forEach((el) => animateCountUp(el));
          observer.disconnect();
        }
      });
    }, { threshold: 0.25 });

    observer.observe(section);
  });
}

const RM_DIRECTIONS = ['left', 'right', 'bottom'];
const rmEnterMarked = new WeakSet();
let rmScrollObserver = null;

function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function prepareEnter(el, direction, delayMs, immediate) {
  if (!el || rmEnterMarked.has(el)) return;
  rmEnterMarked.add(el);
  el.setAttribute('data-rm-enter', direction);
  el.style.setProperty('--rm-enter-delay', `${delayMs || 0}ms`);
  if (immediate) {
    el.setAttribute('data-rm-enter-immediate', 'true');
  }
}

function prepareReveal(el, delayMs) {
  if (!el || rmEnterMarked.has(el)) return;
  rmEnterMarked.add(el);
  el.setAttribute('data-rm-reveal', 'true');
  el.style.setProperty('--rm-enter-delay', `${delayMs || 0}ms`);
}

function applyEnterRules() {
  document.querySelectorAll('.section-eyebrow, .section-header-h, .hero-form-kicker').forEach((el) => {
    prepareEnter(el, 'left', 0, false);
  });

  document.querySelectorAll('.hero-eyebrow').forEach((el) => prepareEnter(el, 'left', 0, true));
  document.querySelectorAll('.hero__headline h1, .hero-content h1').forEach((el) => prepareEnter(el, 'left', 80, true));
  document.querySelectorAll('.hero-lead, .hero-sub').forEach((el) => prepareEnter(el, 'left', 160, true));
  document.querySelectorAll('.hero-call-link, .hero-cta-primary').forEach((el) => prepareEnter(el, 'left', 240, true));
  document.querySelectorAll('.hero-lead-panel, .hero-form-card, #estimate').forEach((el) => prepareEnter(el, 'right', 120, true));
  document.querySelectorAll('.header-cta').forEach((el) => prepareEnter(el, 'right', 180, true));

  document.querySelectorAll('.page-hero h1').forEach((el) => prepareEnter(el, 'left', 0, true));
  document.querySelectorAll('.page-hero .breadcrumb').forEach((el) => prepareEnter(el, 'left', 100, true));

  document.querySelectorAll('.section-header h2').forEach((el) => prepareEnter(el, 'left', 80, false));
  document.querySelectorAll('.section-header .section-desc').forEach((el, index) => {
    prepareReveal(el, index * 40);
  });

  document.querySelectorAll('.about-copy').forEach((el) => prepareEnter(el, 'left', 0, false));
  document.querySelectorAll('.about-highlights').forEach((el) => prepareEnter(el, 'right', 80, false));

  document.querySelectorAll('.company-content').forEach((el) => prepareEnter(el, 'left', 0, false));
  document.querySelectorAll('.company-image img').forEach((el) => prepareEnter(el, 'right', 120, false));
  document.querySelectorAll('.offers-content').forEach((el) => prepareEnter(el, 'left', 0, false));

  document.querySelectorAll('.service-intro-grid .service-intro-content').forEach((el) => {
    prepareEnter(el, 'left', 0, false);
  });
  document.querySelectorAll('.service-intro-grid .service-intro-img').forEach((el) => {
    prepareEnter(el, 'right', 100, false);
  });

  document.querySelectorAll('.service-cta-content').forEach((el) => prepareEnter(el, 'left', 0, false));
  document.querySelectorAll('.cta-form-card, .contact-card').forEach((el) => {
    prepareEnter(el, 'right', 120, false);
  });

  document.querySelectorAll(
    '.services-grid .rm-service-card, .services-page-grid .service-page-card, .why-choose-grid .why-card, .testimonial-card, .blog-card, .gallery-item, .offer-card, .team-content, .team-image',
  ).forEach((el, index) => {
    prepareEnter(el, RM_DIRECTIONS[index % RM_DIRECTIONS.length], (index % 3) * 90, false);
  });

  document.querySelectorAll('.atlas-inner > *').forEach((el, index) => {
    prepareEnter(el, index === 0 ? 'left' : 'right', index * 100, false);
  });

  document.querySelectorAll('.rm-map-review-shell').forEach((el) => {
    prepareEnter(el, 'bottom', 120, false);
  });

  document.querySelectorAll('[data-rm-reveal]').forEach((el, index) => {
    prepareReveal(el, index * 50);
  });
}

function revealImmediateEnter() {
  document.querySelectorAll('[data-rm-enter-immediate="true"]').forEach((el) => {
    el.classList.add('is-visible');
  });

  document.querySelectorAll('.hero-license-bar').forEach((el) => {
    el.classList.add('is-visible');
  });
}

function ensureEnterScrollObserver() {
  if (prefersReducedMotion()) return;

  if (!rmScrollObserver) {
    rmScrollObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
  }

  document.querySelectorAll(
    '[data-rm-enter]:not([data-rm-enter-immediate]):not(.is-visible), [data-rm-reveal]:not(.is-visible)',
  ).forEach((el) => {
    rmScrollObserver.observe(el);
  });
}

function initEnterAnimations() {
  applyEnterRules();

  if (prefersReducedMotion()) {
    document.querySelectorAll('[data-rm-enter], [data-rm-reveal], .hero-license-bar').forEach((el) => {
      el.classList.add('is-visible');
    });
    return;
  }

  revealImmediateEnter();
  ensureEnterScrollObserver();
}

window.rmInitEnterAnimations = initEnterAnimations;

function initHeroParallax() {
  if (document.querySelector('.hero-stage')) return;

  const hero = document.querySelector('#hero.hero');
  if (!hero) return;
  if (prefersReducedMotion()) return;

  const slides = hero.querySelector('.hero-slides');
  if (!slides) return;

  let ticking = false;

  function update() {
    const rect = hero.getBoundingClientRect();
    const heroHeight = hero.offsetHeight || 1;
    const scrolledPast = Math.min(Math.max(-rect.top, 0), heroHeight);
    const rate = 0.42;

    slides.style.transform = `translate3d(0, ${scrolledPast * rate}px, 0)`;
    ticking = false;
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
}

function reviewsFeedUrl() {
  const base = typeof window.__RM_BASE__ === 'string' ? window.__RM_BASE__ : '/';
  const normalized = base.endsWith('/') ? base : `${base}/`;
  return `${normalized}data/google-reviews.json`;
}

function applyLiveReviewCounts(count) {
  const n = Number(count);
  if (!Number.isFinite(n)) return;
  document.querySelectorAll('[data-rm-live-review-count]').forEach((el) => {
    const suffix = el.getAttribute('data-rm-live-review-suffix') || '';
    el.textContent = `${n}${suffix}`;
    if (el.hasAttribute('data-target')) {
      el.setAttribute('data-target', String(n));
    }
  });
}

async function initRmLiveReviewCounts() {
  if (!document.querySelector('[data-rm-live-review-count]')) return;
  try {
    const response = await fetch(reviewsFeedUrl(), { cache: 'no-store' });
    if (!response.ok) return;
    const payload = await response.json();
    if (payload && payload.reviewCount != null) {
      applyLiveReviewCounts(payload.reviewCount);
    }
  } catch (error) {
    console.warn('Live review count fetch failed:', error);
  }
}

function initRmGoogleReviews() {
  const carousels = document.querySelectorAll('[data-rm-review-carousel]');
  if (!carousels.length) return;

  carousels.forEach((carousel) => {
    const track = carousel.querySelector('.rm-review-carousel-track');
    const prevBtn = carousel.querySelector('.rm-review-carousel-btn.prev');
    const nextBtn = carousel.querySelector('.rm-review-carousel-btn.next');
    const showcase = carousel.closest('.rm-google-reviews-showcase');
    const dotsContainer = showcase
      ? showcase.querySelector('.rm-review-carousel-dots')
      : null;
    const summaryEl = document.getElementById('rm-review-summary');
    const mapRatingEl = document.getElementById('rm-map-rating');
    const seedEl = showcase ? showcase.querySelector('#google-reviews-seed') : null;

    if (!track || !prevBtn || !nextBtn || !dotsContainer || !showcase) return;

    let cards = [];
    let currentIndex = 0;
    let reviews = [];

    function escapeHtml(value) {
      return String(value || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function getInitial(name) {
      const clean = String(name || '').trim();
      return clean ? clean.charAt(0).toUpperCase() : '?';
    }

    function formatStars(count) {
      const stars = Math.max(1, Math.min(5, Number(count) || 5));
      return '\u2605'.repeat(stars);
    }

    function reviewCardMarkup(review) {
      return (
        '<article class="rm-review-card">'
        + '<div class="rm-review-card-header">'
        + '<span class="rm-review-avatar" style="background:'
        + escapeHtml(review.avatarColor || '#1a56c4')
        + ';" aria-hidden="true">'
        + escapeHtml(getInitial(review.name))
        + '</span>'
        + '<div>'
        + '<div class="rm-review-name">'
        + escapeHtml(review.name)
        + '</div>'
        + '<div class="rm-review-meta">'
        + escapeHtml(review.meta || '')
        + '</div>'
        + '</div>'
        + '</div>'
        + '<div class="rm-review-card-stars" role="img" aria-label="'
        + escapeHtml(String(Number(review.stars) || 5))
        + ' stars">'
        + formatStars(review.stars)
        + '</div>'
        + '<p class="rm-review-text">'
        + escapeHtml(review.text || '')
        + '</p>'
        + '<div class="rm-review-date">'
        + escapeHtml(review.date || '')
        + '</div>'
        + '</article>'
      );
    }

    function applySummary(payload) {
      const ratingNum = Number(payload.ratingValue || 5);
      const rating = ratingNum.toFixed(1);
      const count = Number(payload.reviewCount || reviews.length || 0);
      const roundedStars = Math.max(1, Math.min(5, Math.round(ratingNum)));
      const label = count === 1 ? ' review' : ' reviews';
      const summaryText = `${rating} \u00b7 ${count}${label}`;
      if (summaryEl) summaryEl.textContent = summaryText;
      const starsEl = showcase.querySelector('.rm-google-stars-display');
      if (starsEl) {
        starsEl.textContent = formatStars(roundedStars);
        starsEl.setAttribute('aria-label', `${rating} out of 5 stars`);
      }
      if (mapRatingEl) {
        mapRatingEl.textContent = `${formatStars(roundedStars)} ${rating} \u00b7 ${count} Google review${count === 1 ? '' : 's'}`;
        mapRatingEl.setAttribute('aria-label', `${rating} out of 5 stars, ${count} Google reviews`);
      }
      applyLiveReviewCounts(count);
    }

    function visibleCount() {
      if (window.innerWidth <= 720) return 1;
      if (window.innerWidth <= 1060) return 2;
      return 3;
    }

    function pageCount() {
      return Math.max(1, Math.ceil(cards.length / visibleCount()));
    }

    function maxIndex() {
      return Math.max(0, cards.length - visibleCount());
    }

    function cardSpan() {
      if (!cards.length) return 0;
      const styles = window.getComputedStyle(track);
      const gap = parseFloat(styles.columnGap || styles.gap || '0');
      return cards[0].getBoundingClientRect().width + gap;
    }

    function updateButtons() {
      const singlePage = pageCount() <= 1 || cards.length === 0;
      prevBtn.disabled = singlePage || currentIndex <= 0;
      nextBtn.disabled = singlePage || currentIndex >= maxIndex();
    }

    function update() {
      currentIndex = Math.max(0, Math.min(currentIndex, maxIndex()));
      track.style.transform = `translateX(${-currentIndex * cardSpan()}px)`;

      const activePage = Math.floor(currentIndex / visibleCount());
      dotsContainer.querySelectorAll('.rm-review-carousel-dot').forEach((dot, index) => {
        const isActive = index === activePage;
        dot.classList.toggle('active', isActive);
        if (isActive) {
          dot.setAttribute('aria-current', 'true');
        } else {
          dot.removeAttribute('aria-current');
        }
      });

      updateButtons();
    }

    function buildDots() {
      dotsContainer.innerHTML = '';
      for (let index = 0; index < pageCount(); index += 1) {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = `rm-review-carousel-dot${index === 0 ? ' active' : ''}`;
        dot.setAttribute('aria-label', `Go to review page ${index + 1}`);
        if (index === 0) dot.setAttribute('aria-current', 'true');
        dot.addEventListener('click', () => {
          currentIndex = index * visibleCount();
          update();
        });
        dotsContainer.appendChild(dot);
      }
    }

    function renderReviews(payload) {
      reviews = Array.isArray(payload.reviews) ? payload.reviews.slice() : [];
      applySummary(payload);

      if (!reviews.length) {
        track.innerHTML = '<article class="rm-review-card"><p class="rm-review-text">Reviews will appear here once posted on Google.</p></article>';
      } else {
        track.innerHTML = reviews.map(reviewCardMarkup).join('');
      }

      cards = Array.from(track.querySelectorAll('.rm-review-card'));
      currentIndex = 0;
      carousel.classList.toggle('single-review', cards.length <= 1);
      buildDots();
      update();
    }

    function parseSeedPayload() {
      if (!seedEl) return null;
      try {
        return JSON.parse(seedEl.textContent || '{}');
      } catch (error) {
        console.warn('Google review seed parse failed:', error);
        return null;
      }
    }

    async function loadReviews() {
      let payload = null;
      try {
        const response = await fetch(reviewsFeedUrl(), { cache: 'no-store' });
        if (response.ok) {
          payload = await response.json();
        }
      } catch (error) {
        console.warn('Google review feed fetch failed, using seed data:', error);
      }

      if (!payload) payload = parseSeedPayload();
      if (!payload || !Array.isArray(payload.reviews)) {
        payload = { ratingValue: 5, reviewCount: 0, reviews: [] };
      }

      renderReviews(payload);
    }

    prevBtn.addEventListener('click', () => {
      currentIndex -= 1;
      update();
    });
    nextBtn.addEventListener('click', () => {
      currentIndex += 1;
      update();
    });
    window.addEventListener('resize', () => {
      buildDots();
      update();
    });

    loadReviews();
  });
}

function initParallaxBanners() {
  const sections = document.querySelectorAll('.atlas-banner--parallax, .rm-parallax-section');
  if (!sections.length) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  let ticking = false;

  function update() {
    sections.forEach((section) => {
      const bg = section.querySelector('.atlas-banner-bg, .rm-parallax-bg');
      if (!bg) return;

      const rect = section.getBoundingClientRect();
      const speed = 0.45;
      const offset = (rect.top - window.innerHeight * 0.5) * -speed;
      bg.style.transform = `translate3d(0, ${offset}px, 0) scale(1.1)`;
    });
    ticking = false;
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
}

const RM_FORMSPREE_ENDPOINT = 'https://formspree.io/f/mbdvvbnp';
const HERO_FORM_SUCCESS_RESET_MS = 3000;

const formSuccessResetTimers = new WeakMap();

const RM_FORM_DEFAULTS = {
  provider: 'formspree',
  formspreeId: 'mbdvvbnp',
  endpoint: RM_FORMSPREE_ENDPOINT,
  recipientEmail: 'info@roofmonsters.co',
  subjectPrefix: 'Roof Monsters website lead',
  fallbackEmail: 'info@roofmonsters.co',
  fallbackPhone: '(727) 439-3869',
};

let rmFormConfig = null;

function formspreeEndpoint(config) {
  if (config.endpoint) return config.endpoint;
  const id = config.formspreeId;
  if (id && id !== 'PLACEHOLDER') return `https://formspree.io/f/${id}`;
  return RM_FORMSPREE_ENDPOINT;
}

function ensureFormStatus(form) {
  let status = form.querySelector('.form-status');
  if (!status) {
    status = document.createElement('p');
    status.className = 'form-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.hidden = true;
    form.appendChild(status);
  }
  return status;
}

function escapeFormHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function getFormFieldsWrap(form) {
  return form.querySelector('.estimate-form-fields');
}

function setFormFieldsVisible(form, visible) {
  const fields = getFormFieldsWrap(form);
  if (fields) {
    fields.hidden = !visible;
    return;
  }
  form.querySelectorAll(':scope > *').forEach((el) => {
    if (el.classList.contains('form-success') || el.classList.contains('form-status')) return;
    el.hidden = !visible;
  });
}

function setFormSubmitting(form, isSubmitting, submitBtn, originalText) {
  form.classList.toggle('is-sending', isSubmitting);
  if (!submitBtn) return;
  submitBtn.disabled = isSubmitting;
  submitBtn.setAttribute('aria-busy', String(isSubmitting));
  submitBtn.textContent = isSubmitting ? 'Sending...' : originalText;
}

function clearFormSuccessReset(form) {
  const timer = formSuccessResetTimers.get(form);
  if (!timer) return;
  clearTimeout(timer);
  formSuccessResetTimers.delete(form);
}

function resetEstimateFormAfterSuccess(form) {
  const submitBtn = form.querySelector('[type="submit"]');
  const originalText = submitBtn?.dataset.rmOriginalText || submitBtn?.textContent?.trim() || 'Send';
  const existingSuccess = form.querySelector('.form-success');
  const status = form.querySelector('.form-status');

  clearFormSuccessReset(form);
  form.classList.remove('is-submitted', 'is-sending');
  delete form.dataset.rmSubmitting;
  form.removeAttribute('aria-label');
  setFormFieldsVisible(form, true);
  if (existingSuccess) existingSuccess.hidden = true;
  if (status) {
    status.hidden = true;
    status.textContent = '';
  }
  form.reset();
  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
    submitBtn.removeAttribute('aria-busy');
  }
}

function scheduleHeroFormReset(form) {
  if (!form.classList.contains('hero-estimate-form')) return;
  clearFormSuccessReset(form);
  formSuccessResetTimers.set(
    form,
    window.setTimeout(() => resetEstimateFormAfterSuccess(form), HERO_FORM_SUCCESS_RESET_MS),
  );
}
function showFormError(form, message) {
  clearFormSuccessReset(form);
  const status = ensureFormStatus(form);
  const existingSuccess = form.querySelector('.form-success');
  if (!message) {
    status.hidden = true;
    status.textContent = '';
    return;
  }

  form.classList.remove('is-submitted', 'is-sending');
  delete form.dataset.rmSubmitting;
  setFormFieldsVisible(form, true);
  if (existingSuccess) existingSuccess.hidden = true;

  status.className = 'form-status form-status--error';
  status.textContent = message;
  status.hidden = false;
}

function showEstimateFormSuccess(form) {
  const existingSuccess = form.querySelector('.form-success');
  const status = ensureFormStatus(form);
  const message = existingSuccess?.textContent?.trim()
    || 'Thank you — we received your request and will respond soon.';

  form.classList.remove('is-sending');
  form.classList.add('is-submitted');
  form.dataset.rmSubmitting = 'success';
  setFormFieldsVisible(form, false);

  if (existingSuccess) {
    if (!existingSuccess.querySelector('.fa-circle-check')) {
      existingSuccess.innerHTML = `<i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>${escapeFormHtml(message)}</span>`;
    }
    existingSuccess.hidden = false;
    status.hidden = true;
  } else {
    status.className = 'form-status form-status--success';
    status.innerHTML = `<i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>${escapeFormHtml(message)}</span>`;
    status.hidden = false;
  }

  form.setAttribute('aria-label', 'Estimate request sent');
  scheduleHeroFormReset(form);
}

async function loadFormConfig() {
  if (rmFormConfig) return rmFormConfig;
  try {
    const base = window.__RM_BASE__ || '/';
    const res = await fetch(`${base}data/site-forms.json`, { cache: 'no-store' });
    if (res.ok) {
      rmFormConfig = { ...RM_FORM_DEFAULTS, ...(await res.json()) };
      return rmFormConfig;
    }
  } catch {
    /* use defaults */
  }
  rmFormConfig = { ...RM_FORM_DEFAULTS };
  return rmFormConfig;
}

function readEstimateField(form, name, fallbackSelector) {
  const field = form.querySelector(`[name="${name}"]`) || form.querySelector(fallbackSelector);
  return field?.value?.trim() || '';
}

function buildEstimatePayload(form, config) {
  const payload = new FormData();
  const assign = (key, value) => {
    if (value) payload.append(key, value);
  };

  assign('name', readEstimateField(form, 'name', 'input[type="text"]'));
  const email = readEstimateField(form, 'email', 'input[type="email"]');
  assign('email', email);
  if (email) payload.append('_replyto', email);
  assign('phone', readEstimateField(form, 'phone', 'input[type="tel"]'));
  assign('address', readEstimateField(form, 'address', 'input[placeholder*="Street"], input[placeholder*="address"]'));
  assign('message', readEstimateField(form, 'message', 'textarea'));

  const service = form.querySelector('[name="service"]');
  if (service?.value) payload.append('service', service.value);

  const property = form.querySelector('[name="property"]:checked');
  if (property?.value) payload.append('property', property.value);

  payload.append('_subject', `${config.subjectPrefix} — ${document.title}`);
  payload.append('page', `${window.location.pathname}${window.location.search}`);
  payload.append('source', form.id || form.className || 'estimate-form');
  return payload;
}

function isValidEmail(value) {
  const email = String(value || '').trim();
  if (!email || email.length > 254) return false;
  // Practical RFC-ish check — rejects spaces and obvious fakes without being brittle.
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i.test(email)
    && !/(test@test\.|asdf@|noreply@|noemail@)/i.test(email);
}

function normalizePhoneDigits(value) {
  return String(value || '').replace(/\D/g, '');
}

function isValidPhone(value) {
  const digits = normalizePhoneDigits(value);
  // US-focused: 10 digits, or 11 starting with 1.
  if (digits.length === 10) return true;
  if (digits.length === 11 && digits.startsWith('1')) return true;
  return false;
}

function validateEstimateContact(form) {
  const name = readEstimateField(form, 'name', 'input[type="text"], input[name="name"]');
  const email = readEstimateField(form, 'email', 'input[type="email"]');
  const phone = readEstimateField(form, 'phone', 'input[type="tel"]');
  const emailOk = isValidEmail(email);
  const phoneOk = isValidPhone(phone);

  if (!name) {
    return { ok: false, message: 'Please enter your name.' };
  }
  if (!emailOk && !phoneOk) {
    return {
      ok: false,
      message: 'Please enter a valid email address or a valid phone number (at least one is required).',
    };
  }
  if (email && !emailOk) {
    return { ok: false, message: 'Please enter a valid email address, or clear the email field and use phone instead.' };
  }
  if (phone && !phoneOk) {
    return { ok: false, message: 'Please enter a valid 10-digit phone number, or clear the phone field and use email instead.' };
  }
  return { ok: true, name, email: emailOk ? email : '', phone: phoneOk ? phone : '' };
}

async function submitEstimateForm(form) {
  if (form.dataset.rmSubmitting === 'true' || form.dataset.rmSubmitting === 'success') {
    return;
  }
  clearFormSuccessReset(form);
  form.dataset.rmSubmitting = 'true';

  const config = await loadFormConfig();
  const endpoint = formspreeEndpoint(config);
  if (!endpoint) {
    delete form.dataset.rmSubmitting;
    showFormError(form, `Online forms are not configured yet. Please call ${config.fallbackPhone} or email ${config.fallbackEmail}.`);
    return;
  }

  const contact = validateEstimateContact(form);
  if (!contact.ok) {
    delete form.dataset.rmSubmitting;
    showFormError(form, contact.message);
    return;
  }

  const payload = buildEstimatePayload(form, config);
  // Prefer validated contact values (empty invalid optional field if the other is valid).
  payload.set('name', contact.name);
  if (contact.email) {
    payload.set('email', contact.email);
    payload.set('_replyto', contact.email);
  } else {
    // Formspree expects an email field — use a clearly labeled phone-only placeholder.
    const digits = normalizePhoneDigits(contact.phone);
    const phoneEmail = `phone-${digits}@no-email.roofmonsters.co`;
    payload.set('email', phoneEmail);
    payload.delete('_replyto');
    payload.set('contact_method', 'phone-only');
  }
  if (contact.phone) {
    payload.set('phone', contact.phone);
  } else {
    payload.delete('phone');
  }

  const submitBtn = form.querySelector('[type="submit"]');
  const originalText = submitBtn?.textContent?.trim() || 'Send';
  if (submitBtn) submitBtn.dataset.rmOriginalText = originalText;
  setFormSubmitting(form, true, submitBtn, originalText);
  showFormError(form, '');

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      body: payload,
      headers: { Accept: 'application/json' },
    });
    let data = {};
    try {
      data = await res.json();
    } catch {
      data = {};
    }

    if (res.ok) {
      showEstimateFormSuccess(form);
      return;
    }

    const fieldErrors = Array.isArray(data.errors)
      ? data.errors.map((entry) => entry.message).filter(Boolean).join(' ')
      : '';
    const reason = fieldErrors || data.error || `Request failed (${res.status})`;
    throw new Error(reason);
  } catch (error) {
    delete form.dataset.rmSubmitting;
    const message = error instanceof Error && error.message
      ? error.message
      : 'Could not send right now.';
    showFormError(
      form,
      `${message} Please call ${config.fallbackPhone} or email ${config.fallbackEmail}.`,
    );
    setFormSubmitting(form, false, submitBtn, originalText);
  }
}

function initEstimateForms() {
  document.querySelectorAll('.estimate-form').forEach((form) => {
    const formNotes = form.querySelectorAll('.form-note');
    formNotes.forEach((note, index) => {
      if (index > 0) note.remove();
    });

    if (form.dataset.bound === 'true') return;
    form.dataset.bound = 'true';

    if (!form.getAttribute('action')) {
      form.setAttribute('action', RM_FORMSPREE_ENDPOINT);
    }
    if (!form.getAttribute('method')) {
      form.setAttribute('method', 'POST');
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      void submitEstimateForm(form);
    });
  });
}

window.rmInitEstimateForms = initEstimateForms;

function initSiteChrome() {
  initCurrentYear();
  initHeaderScroll();
  initMobileNav();
}

function initPageFeatures() {
  try {
    initEnterAnimations();
    initHeroParallax();
    initParallaxBanners();
    initHeroSlider();
    initTestimonialCarousel();
    initRmGoogleReviews();
    initRmLiveReviewCounts();
    initCountUp();
  } catch (error) {
    console.error('Roof Monsters page feature init error:', error);
  } finally {
    initEstimateForms();
  }
}

function initApp() {
  initSiteChrome();
  initPageFeatures();
}

document.addEventListener('site:includes-loaded', initApp, { once: true });

if (document.querySelector('.estimate-form')) {
  initEstimateForms();
}

if (document.querySelector('.site-header') && !document.getElementById('site-header-include')) {
  initApp();
}
