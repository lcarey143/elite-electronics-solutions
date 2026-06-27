(function () {
  'use strict';

  const config = window.EES_CONFIG || {};
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const bookingForm = document.getElementById('bookingForm');
  const bookingLayout = document.getElementById('bookingLayout');
  const bookingSuccess = document.getElementById('bookingSuccess');
  const bookingRef = document.getElementById('bookingRef');
  const bookingEmailNote = document.getElementById('bookingEmailNote');
  const bookingError = document.getElementById('bookingError');
  const bookingSubmit = document.getElementById('bookingSubmit');
  const preferredDate = document.getElementById('id_preferred_date');

  if (preferredDate) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    preferredDate.min = tomorrow.toISOString().split('T')[0];
  }

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  }, { passive: true });

  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('.reveal-on-scroll, .glass-card, .service-card, .pricing-card, .partner-card, .contact-card, .credential-card').forEach((el) => {
      el.classList.add('reveal-on-scroll');
      revealObserver.observe(el);
    });
  }

  function getCsrfToken() {
    if (config.csrfToken) return config.csrfToken;
    const cookie = document.cookie.match(/csrftoken=([^;]+)/);
    return cookie ? cookie[1] : '';
  }

  if (bookingForm) {
    bookingForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const checked = bookingForm.querySelectorAll('input[name="services"]:checked');
      if (checked.length === 0) {
        bookingError.textContent = 'Please select at least one service.';
        bookingError.hidden = false;
        return;
      }

      bookingError.hidden = true;
      bookingSubmit.disabled = true;
      bookingSubmit.textContent = 'Submitting...';

      const formData = new FormData(bookingForm);

      try {
        const response = await fetch(config.bookingUrl || bookingForm.action, {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': getCsrfToken(),
          },
          body: formData,
        });

        let data;
        const text = await response.text();
        try {
          data = JSON.parse(text);
        } catch (parseErr) {
          bookingError.textContent = response.status === 403
            ? 'Session expired. Please refresh the page and try again.'
            : 'Server error. Please refresh and try again, or call (242) 375-4179.';
          bookingError.hidden = false;
          return;
        }

        if (!response.ok || !data.success) {
          const errors = data.errors
            ? Object.values(data.errors).flat().join(' ')
            : data.error || 'Something went wrong. Please try again.';
          bookingError.textContent = errors;
          bookingError.hidden = false;
          return;
        }

        bookingLayout.hidden = true;
        bookingSuccess.hidden = false;
        bookingRef.textContent = data.reference;
        if (bookingEmailNote) {
          bookingEmailNote.hidden = !data.email_sent;
        }
        bookingSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } catch (err) {
        bookingError.textContent = 'Network error. Please check your connection and try again.';
        bookingError.hidden = false;
      } finally {
        bookingSubmit.disabled = false;
        bookingSubmit.textContent = 'Submit Booking Request';
      }
    });
  }
})();
