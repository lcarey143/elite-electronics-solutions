(function () {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const layers = document.querySelectorAll('.layer-3d');
  const serviceCards = document.querySelectorAll('[data-tilt]');
  let ticking = false;

  function updateScroll3D() {
    const windowH = window.innerHeight;
    const viewportCenter = windowH / 2;

    layers.forEach((layer) => {
      const section = layer.closest('.section');
      if (!section) return;

      const rect = section.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > windowH) return;

      const depth = parseFloat(layer.dataset.depth) || 0.1;
      const sectionCenter = rect.top + rect.height / 2;
      const offset = (sectionCenter - viewportCenter) / windowH;
      const rotateX = offset * depth * 4;
      const translateY = offset * depth * 16;

      layer.style.transform = 'rotateX(' + rotateX + 'deg) translateY(' + translateY + 'px)';
    });

    ticking = false;
  }

  if (!reducedMotion && layers.length) {
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateScroll3D);
        ticking = true;
      }
    }, { passive: true });
    updateScroll3D();
  }

  if (!reducedMotion) {
    serviceCards.forEach((card) => {
      let rafId = null;
      card.addEventListener('mousemove', (e) => {
        if (rafId) return;
        rafId = requestAnimationFrame(() => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const rotateX = ((y - rect.height / 2) / (rect.height / 2)) * -4;
          const rotateY = ((x - rect.width / 2) / (rect.width / 2)) * 4;
          card.style.transform = 'perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg)';
          rafId = null;
        });
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  if (!reducedMotion) {
    initHeroCanvas();
  }
})();

function initHeroCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const heroSection = canvas.closest('.hero-section');
  let isVisible = true;
  let isAnimating = false;

  if (heroSection && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        isVisible = entries[0].isIntersecting;
        if (isVisible && !isAnimating) animate();
      },
      { threshold: 0.05 }
    );
    observer.observe(heroSection);
  }

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 30;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false, powerPreference: 'high-performance' });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

  const nodeCount = 35;
  const spread = 40;
  const nodes = [];
  const positions = [];

  for (let i = 0; i < nodeCount; i++) {
    const geometry = new THREE.SphereGeometry(0.1, 6, 6);
    const material = new THREE.MeshBasicMaterial({
      color: i % 3 === 0 ? 0x7cfc00 : i % 3 === 1 ? 0x2ecc71 : 0x1a5c3a,
      transparent: true,
      opacity: 0.7,
    });
    const node = new THREE.Mesh(geometry, material);
    node.position.set(
      (Math.random() - 0.5) * spread,
      (Math.random() - 0.5) * spread * 0.6,
      (Math.random() - 0.5) * spread
    );
    node.userData = { phase: Math.random() * Math.PI * 2, speed: 0.002 + Math.random() * 0.002 };
    scene.add(node);
    nodes.push(node);
  }

  const linePositions = [];
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      if (nodes[i].position.distanceTo(nodes[j].position) < 8) {
        positions.push([i, j]);
        linePositions.push(
          nodes[i].position.x, nodes[i].position.y, nodes[i].position.z,
          nodes[j].position.x, nodes[j].position.y, nodes[j].position.z
        );
      }
    }
  }

  const lineGeometry = new THREE.BufferGeometry();
  lineGeometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
  const lines = new THREE.LineSegments(
    lineGeometry,
    new THREE.LineBasicMaterial({ color: 0x2ecc71, transparent: true, opacity: 0.12 })
  );
  scene.add(lines);

  let mouseX = 0;
  let mouseY = 0;
  document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      isVisible = false;
    } else if (heroSection) {
      const rect = heroSection.getBoundingClientRect();
      isVisible = rect.bottom > 0 && rect.top < window.innerHeight;
      if (isVisible && !isAnimating) animate();
    }
  });

  let time = 0;
  let frame = 0;

  function animate() {
    if (!isVisible || document.hidden) {
      isAnimating = false;
      return;
    }
    isAnimating = true;
    requestAnimationFrame(animate);

    time += 0.01;
    frame++;

    nodes.forEach((node) => {
      const d = node.userData;
      node.position.y += Math.sin(time * 50 + d.phase) * 0.003;
    });

    if (frame % 3 === 0 && positions.length) {
      const arr = lineGeometry.attributes.position.array;
      positions.forEach(([a, b], idx) => {
        const offset = idx * 6;
        arr[offset] = nodes[a].position.x;
        arr[offset + 1] = nodes[a].position.y;
        arr[offset + 2] = nodes[a].position.z;
        arr[offset + 3] = nodes[b].position.x;
        arr[offset + 4] = nodes[b].position.y;
        arr[offset + 5] = nodes[b].position.z;
      });
      lineGeometry.attributes.position.needsUpdate = true;
    }

    camera.position.x += (mouseX * 2 - camera.position.x) * 0.02;
    camera.position.y += (-mouseY * 1.5 - camera.position.y) * 0.02;
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
  }

  animate();

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }, { passive: true });
}
