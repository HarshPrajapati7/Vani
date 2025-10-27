/* Mobile Navigation and Touch Enhancements */

(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    // Mobile menu toggle
    setupMobileMenu();
    
    // Add touch feedback
    addTouchFeedback();
    
    // Setup pull-to-refresh (optional)
    setupPullToRefresh();
    
    // Prevent zoom on double-tap for better UX
    preventDoubleTabZoom();
    
    // Add haptic feedback simulation
    addHapticFeedback();
  }

  function setupMobileMenu() {
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const navToggle = document.querySelector('.nav-toggle');
    
    if (menuBtn) {
      menuBtn.addEventListener('click', () => {
        if (navLinks) {
          navLinks.classList.toggle('open');
        }
      });
    }

    if (navToggle) {
      navToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        if (navLinks) {
          navLinks.classList.toggle('open');
        }
      });
    }

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (navLinks && navLinks.classList.contains('open')) {
        if (!navLinks.contains(e.target) && !navToggle?.contains(e.target)) {
          navLinks.classList.remove('open');
        }
      }
    });

    // Close menu when clicking a nav link
    if (navLinks) {
      navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          navLinks.classList.remove('open');
        });
      });
    }
  }

  function addTouchFeedback() {
    // Add visual feedback for touch interactions
    const interactiveElements = document.querySelectorAll('button, a, .btn, .nav-item, .card');
    
    interactiveElements.forEach(el => {
      el.addEventListener('touchstart', function() {
        this.style.transition = 'transform 0.1s, opacity 0.1s';
        this.style.transform = 'scale(0.97)';
        this.style.opacity = '0.8';
      }, { passive: true });
      
      el.addEventListener('touchend', function() {
        this.style.transform = '';
        this.style.opacity = '';
      }, { passive: true });
      
      el.addEventListener('touchcancel', function() {
        this.style.transform = '';
        this.style.opacity = '';
      }, { passive: true });
    });
  }

  function setupPullToRefresh() {
    let startY = 0;
    let pulling = false;
    
    document.addEventListener('touchstart', (e) => {
      if (window.scrollY === 0) {
        startY = e.touches[0].pageY;
        pulling = true;
      }
    }, { passive: true });
    
    document.addEventListener('touchmove', (e) => {
      if (!pulling) return;
      
      const currentY = e.touches[0].pageY;
      const distance = currentY - startY;
      
      if (distance > 80 && window.scrollY === 0) {
        // User pulled down enough - could trigger refresh
        console.log('Pull to refresh triggered');
      }
    }, { passive: true });
    
    document.addEventListener('touchend', () => {
      pulling = false;
    }, { passive: true });
  }

  function preventDoubleTabZoom() {
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (e) => {
      const now = Date.now();
      if (now - lastTouchEnd <= 300) {
        e.preventDefault();
      }
      lastTouchEnd = now;
    }, { passive: false });
  }

  function addHapticFeedback() {
    // Simulate haptic feedback on button clicks (if Vibration API is available)
    if ('vibrate' in navigator) {
      const buttons = document.querySelectorAll('button, .btn, .nav-item');
      buttons.forEach(btn => {
        btn.addEventListener('click', () => {
          navigator.vibrate(10); // 10ms vibration
        });
      });
    }
  }

  // Smooth scroll to top button (for long pages)
  window.scrollToTop = function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  // Show/hide scroll-to-top button
  window.addEventListener('scroll', () => {
    const scrollBtn = document.getElementById('scrollTopBtn');
    if (scrollBtn) {
      if (window.scrollY > 500) {
        scrollBtn.style.display = 'flex';
      } else {
        scrollBtn.style.display = 'none';
      }
    }
  }, { passive: true });

  // Add resize handler for orientation changes
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      // Recalculate viewport heights if needed
      document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
    }, 100);
  });

  // Set initial viewport height
  document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);

})();
