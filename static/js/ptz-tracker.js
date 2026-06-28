(function () {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  if (reducedMotion || isTouch) return;

  const toggle = document.getElementById('aiToggle');
  const head = document.getElementById('ptzHead');

  if (!toggle || !head) return;

  const PIVOT_Y_RATIO = 0.615;
  const MIN_ANGLE = -45;
  const MAX_ANGLE = 45;
  const SMOOTH = 0.14;

  let targetAngle = 0;
  let currentAngle = 0;
  let rafId = null;

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function normalizeAngle(degrees) {
    let value = degrees;
    while (value > 180) value -= 360;
    while (value < -180) value += 360;
    return value;
  }

  function setHeadRotation(angle) {
    head.style.transform = 'rotate(' + angle.toFixed(2) + 'deg)';
  }

  function tick() {
    currentAngle += (targetAngle - currentAngle) * SMOOTH;
    setHeadRotation(currentAngle);

    if (Math.abs(targetAngle - currentAngle) > 0.08) {
      rafId = requestAnimationFrame(tick);
    } else {
      currentAngle = targetAngle;
      setHeadRotation(currentAngle);
      rafId = null;
    }
  }

  function queueTick() {
    if (!rafId) {
      rafId = requestAnimationFrame(tick);
    }
  }

  function updateTarget(clientX, clientY) {
    const rect = toggle.getBoundingClientRect();
    const pivotScreenX = rect.left + rect.width / 2;
    const pivotScreenY = rect.top + rect.height * PIVOT_Y_RATIO;
    const angleRad = Math.atan2(clientY - pivotScreenY, clientX - pivotScreenX);
    const degrees = normalizeAngle(angleRad * (180 / Math.PI) + 90);

    targetAngle = clamp(degrees, MIN_ANGLE, MAX_ANGLE);
    queueTick();
  }

  document.addEventListener('mousemove', (event) => {
    updateTarget(event.clientX, event.clientY);
  }, { passive: true });

  setHeadRotation(0);
})();
