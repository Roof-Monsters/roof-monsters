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
      const rating = Number(payload.ratingValue || 5).toFixed(1);
      const count = Number(payload.reviewCount || reviews.length || 0);
      const label = count === 1 ? ' review' : ' reviews';
      const summaryText = `${rating} \u00b7 ${count}${label}`;
      if (summaryEl) summaryEl.textContent = summaryText;
      if (mapRatingEl) {
        mapRatingEl.textContent = `${formatStars(payload.ratingValue || 5)} ${rating} \u00b7 ${count} Google review${count === 1 ? '' : 's'}`;
        mapRatingEl.setAttribute('aria-label', `${rating} out of 5 stars, ${count} Google reviews`);
      }
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
        const response = await fetch('./data/google-reviews.json', { cache: 'no-store' });
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

function initEstimateForms() {
  document.querySelectorAll('.estimate-form').forEach((form) => {
    if (form.dataset.bound === 'true') return;
    form.dataset.bound = 'true';

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = form.querySelector('[name="name"]')?.value.trim();
      const email = form.querySelector('[name="email"]')?.value.trim();
      if (!name || !email) {
        alert('Please enter your name and email.');
        return;
      }
      alert(`Thank you, ${name}! We'll be in touch shortly.`);
      form.reset();
    });
  });
}

function initSiteChrome() {
  initCurrentYear();
  initHeaderScroll();
  initMobileNav();
}

function initPageFeatures() {
  initEnterAnimations();
  initHeroParallax();
  initParallaxBanners();
  initHeroSlider();
  initTestimonialCarousel();
  initRmGoogleReviews();
  initCountUp();
  initEstimateForms();
}

function initApp() {
  initSiteChrome();
  initPageFeatures();
}

document.addEventListener('site:includes-loaded', initApp, { once: true });

if (document.querySelector('.site-header') && !document.getElementById('site-header-include')) {
  initApp();
}
