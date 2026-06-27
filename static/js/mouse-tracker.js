(function () {
  'use strict';

  const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (isTouch || reducedMotion) {
    document.body.classList.add('touch-device');
    return;
  }

  const glow = document.getElementById('cursorGlow');
  const dot = document.getElementById('cursorDot');
  if (!glow || !dot) return;

  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let glowX = mouseX;
  let glowY = mouseY;
  let isMoving = false;
  let idleTimer = null;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    dot.style.transform = 'translate(' + mouseX + 'px, ' + mouseY + 'px) translate(-50%, -50%)';

    if (!isMoving) {
      isMoving = true;
      glow.style.opacity = '0.5';
      animateGlow();
    }

    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      isMoving = false;
    }, 120);
  }, { passive: true });

  function animateGlow() {
    if (!isMoving) return;
    glowX += (mouseX - glowX) * 0.12;
    glowY += (mouseY - glowY) * 0.12;
    glow.style.transform = 'translate(' + glowX + 'px, ' + glowY + 'px) translate(-50%, -50%)';
    requestAnimationFrame(animateGlow);
  }

  dot.style.transform = 'translate(' + mouseX + 'px, ' + mouseY + 'px) translate(-50%, -50%)';
  glow.style.transform = 'translate(' + glowX + 'px, ' + glowY + 'px) translate(-50%, -50%)';

  const hoverTargets = document.querySelectorAll('a, button, .service-card');
  hoverTargets.forEach((el) => {
    el.addEventListener('mouseenter', () => {
      dot.style.width = '12px';
      dot.style.height = '12px';
    });
    el.addEventListener('mouseleave', () => {
      dot.style.width = '8px';
      dot.style.height = '8px';
    });
  });
})();
