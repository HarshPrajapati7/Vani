/* Mobile Navigation and Touch Enhancements - Accessibility Improved */

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
    
    // Keyboard accessibility
    setupKeyboardNavigation();
    
    // Add touch feedback
    addTouchFeedback();
    
    // Setup pull-to-refresh (optional)
    setupPullToRefresh();
    
    // Prevent zoom on double-tap for better UX
    preventDoubleTabZoom();
    
    // Add haptic feedback simulation
    addHapticFeedback();

    // iOS viewport fix
    setupViewportHeight();
  }

  function setupMobileMenu() {
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const navToggle = document.querySelector('.nav-toggle');
    
    if (menuBtn) {
      menuBtn.addEventListener('click', () => {
        if (navLinks) {
          navLinks.classList.toggle('open');
          // Set aria-expanded for accessibility
          menuBtn.setAttribute('aria-expanded', navLinks.classList.contains('open'));
        }
      });
    }

    if (navToggle) {
      navToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        if (navLinks) {
          navLinks.classList.toggle('open');
          navToggle.setAttribute('aria-expanded', navLinks.classList.contains('open'));
        }
      });
    }

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (navLinks && navLinks.classList.contains('open')) {
        if (!navLinks.contains(e.target) && !navToggle?.contains(e.target) && !menuBtn?.contains(e.target)) {
          navLinks.classList.remove('open');
          if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
          if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
        }
      }
    });

    // Close menu when clicking a nav link
    if (navLinks) {
      navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          navLinks.classList.remove('open');
          if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
          if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
        });
      });
    }
  }

  /**
   * Keyboard navigation - Enter/Space to toggle menu, Escape to close
   */
  function setupKeyboardNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle) {
      navToggle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          navToggle.click();
        }
      });
    }

    // Escape key closes menu
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navLinks && navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
        if (navToggle) {
          navToggle.setAttribute('aria-expanded', 'false');
          navToggle.focus();
        }
      }
    });

    // Tab trap in mobile menu (optional: keep focus within menu)
    if (navLinks) {
      navLinks.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
          const focusableElements = navLinks.querySelectorAll('a, button');
          const firstElement = focusableElements[0];
          const lastElement = focusableElements[focusableElements.length - 1];

          if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
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
        console.log('[UX] Pull to refresh triggered');
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

  /**
   * iOS Viewport Height Fix
   * Fixes the 100vh issue on mobile with dynamic browser bar
   */
  function setupViewportHeight() {
    const setVH = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
      document.documentElement.style.setProperty('--dvh', `${window.innerHeight}px`);
    };

    setVH();
    
    // Recalculate on resize/orientation change
    window.addEventListener('resize', () => {
      setVH();
      
      // Trigger map recalculation if map exists
      if (window.recalcMapSize) {
        window.recalcMapSize();
      }
    });

    // Handle orientation changes
    window.addEventListener('orientationchange', () => {
      setTimeout(setVH, 100);
      if (window.recalcMapSize) {
        setTimeout(window.recalcMapSize, 200);
      }
    });
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

  console.log('[Mobile Nav] Initialized with accessibility enhancements');

})();
