/* =========================================
   CURTAIN INTRO ANIMATION
   Plays once on page load, then self-destructs.
   ========================================= */

(function initCurtainAnimation() {
  const scene    = document.getElementById('curtain-scene');
  const overlay  = document.getElementById('overlay-black');
  const glow     = document.getElementById('curtain-glow');
  const left     = document.getElementById('curtain-left');
  const right    = document.getElementById('curtain-right');

  // Safety — if curtain elements don't exist, bail silently
  if (!scene || !overlay || !left || !right) {
    console.warn('Curtain elements not found, skipping intro animation.');
    return;
  }

  // Prevent scrolling during the animation
  document.body.style.overflow = 'hidden';

  // ── STEP 1: After a brief pause, fade the black overlay & activate glow ──
  setTimeout(function () {
    overlay.classList.add('fade-out');
    if (glow) glow.classList.add('glow-active');
  }, 400);

  // ── STEP 2: After black fades (1.2s + 400ms initial), open the curtains ──
  setTimeout(function () {
    left.classList.add('curtain-open');
    right.classList.add('curtain-open');
  }, 1800);

  // ── STEP 3: After curtains fully open (1.8s transition), cleanup ──
  setTimeout(function () {
    // Hide and remove the entire scene from the DOM
    scene.classList.add('curtain-done');
    scene.remove();

    // Restore scrolling
    document.body.style.overflow = '';

    console.log('✨ Curtain intro animation complete.');
  }, 3800);
})();
