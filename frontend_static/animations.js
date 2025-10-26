// Initialize Lenis for smooth scrolling
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smooth: true,
  direction: 'vertical',
  smoothTouch: false
});

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      lenis.scrollTo(target, { offset: -80 });
    }
  });
});

// Initialize Barba.js for page transitions
barba.init({
  transitions: [{
    name: 'default-transition',
    
    leave(data) {
      return anime({
        targets: data.current.container,
        opacity: [1, 0],
        translateY: [0, -50],
        easing: 'easeInQuad',
        duration: 400
      }).finished;
    },
    
    enter(data) {
      window.scrollTo(0, 0);
      return anime({
        targets: data.next.container,
        opacity: [0, 1],
        translateY: [50, 0],
        easing: 'easeOutQuad',
        duration: 600
      }).finished;
    }
  }]
});

// Hero text animation with Textbits for stunning effects
function animateText() {
  const heroTitle = document.querySelector('.hero h1');
  const heroDesc = document.querySelector('.hero p');
  
  if (heroTitle && heroTitle.textContent && typeof textbits !== 'undefined') {
    // Apply Textbits scramble effect to the title
    heroTitle.setAttribute('data-textbits', 'scramble');
    heroTitle.style.opacity = '1';
    
    // Initialize Textbits
    textbits.scramble(heroTitle, {
      duration: 1500,
      delay: 300,
      characters: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
      speed: 50
    });
  } else if (heroTitle && heroTitle.textContent) {
    // Fallback animation with split text
    const words = heroTitle.textContent.split(' ');
    heroTitle.innerHTML = words.map(word => 
      `<span class="word" style="display:inline-block;opacity:0;">${word}&nbsp;</span>`
    ).join('');
    
    anime.timeline()
      .add({
        targets: '.hero h1 .word',
        opacity: [0, 1],
        translateY: [30, 0],
        rotateX: [-90, 0],
        scale: [0.8, 1],
        easing: 'spring(1, 80, 10, 0)',
        duration: 1200,
        delay: anime.stagger(80, {start: 300})
      });
  }
  
  if (heroDesc) {
    // Apply fade-in with slide up
    anime({
      targets: heroDesc,
      opacity: [0, 1],
      translateY: [20, 0],
      easing: 'easeOutQuad',
      duration: 800,
      delay: 800
    });
    
    // Add glitch effect on hover
    heroDesc.addEventListener('mouseenter', () => {
      if (typeof textbits !== 'undefined') {
        textbits.glitch(heroDesc, {
          duration: 600,
          intensity: 0.3
        });
      }
    });
  }

  // Animate CTA buttons with bounce
  anime({
    targets: '.cta .btn',
    opacity: [0, 1],
    translateY: [30, 0],
    scale: [0.9, 1],
    easing: 'spring(1, 80, 10, 0)',
    duration: 1000,
    delay: anime.stagger(100, {start: 1000})
  });

  // Animate hero visual with scale and fade
  anime({
    targets: '.hero-visual',
    opacity: [0, 1],
    scale: [0.95, 1],
    easing: 'easeOutQuad',
    duration: 1200,
    delay: 1200
  });

  // Floating animation for neon rings with random movement
  anime({
    targets: '.neon-ring',
    translateY: ['0px', '-12px'],
    translateX: ['0px', '5px'],
    scale: [1, 1.05],
    opacity: [0.3, 0.7],
    easing: 'easeInOutSine',
    duration: 3000,
    direction: 'alternate',
    loop: true
  });

  anime({
    targets: '.neon-edge',
    translateY: ['0px', '-8px'],
    translateX: ['0px', '-5px'],
    easing: 'easeInOutSine',
    duration: 4000,
    direction: 'alternate',
    loop: true
  });

  anime({
    targets: '.neon-halo',
    scale: [1, 1.1],
    opacity: [0.2, 0.5],
    easing: 'easeInOutSine',
    duration: 5000,
    direction: 'alternate',
    loop: true
  });

  // Animate features on scroll with 3D rotation
  const featureCards = document.querySelectorAll('#features > div > div');
  if (featureCards.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          anime({
            targets: entry.target,
            opacity: [0, 1],
            translateY: [40, 0],
            rotateX: [-15, 0],
            rotateY: [-10, 0],
            easing: 'spring(1, 80, 10, 0)',
            duration: 1000
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    featureCards.forEach((card, i) => {
      card.style.opacity = '0';
      setTimeout(() => observer.observe(card), i * 50);
    });
  }

  // Add parallax effect to hero visual
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroVisual = document.querySelector('.hero-visual');
    if (heroVisual) {
      heroVisual.style.transform = `translateY(${scrolled * 0.2}px) scale(${1 - scrolled * 0.0001})`;
    }
  });
}

// Initialize animations on page load
window.addEventListener('DOMContentLoaded', animateText);

// Re-initialize animations after Barba transition
barba.hooks.after(() => {
  animateText();
});

// Add magnetic effect to buttons with enhanced animation
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    
    anime({
      targets: btn,
      translateX: x * 0.3,
      translateY: y * 0.3,
      scale: 1.05,
      duration: 300,
      easing: 'easeOutQuad'
    });
  });
  
  btn.addEventListener('mouseleave', () => {
    anime({
      targets: btn,
      translateX: 0,
      translateY: 0,
      scale: 1,
      duration: 500,
      easing: 'spring(1, 80, 10, 0)'
    });
  });
  
  // Click ripple effect
  btn.addEventListener('click', (e) => {
    const ripple = document.createElement('span');
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    ripple.style.cssText = `
      position: absolute;
      left: ${x}px;
      top: ${y}px;
      width: 0;
      height: 0;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.5);
      transform: translate(-50%, -50%);
      pointer-events: none;
    `;
    
    btn.style.position = 'relative';
    btn.style.overflow = 'hidden';
    btn.appendChild(ripple);
    
    anime({
      targets: ripple,
      width: '300px',
      height: '300px',
      opacity: [0.5, 0],
      duration: 600,
      easing: 'easeOutQuad',
      complete: () => ripple.remove()
    });
  });
});

// Add shimmer effect to heading on hover with Textbits
const heading = document.querySelector('.hero h1');
if (heading) {
  heading.addEventListener('mouseenter', () => {
    if (typeof textbits !== 'undefined') {
      textbits.shimmer(heading, {
        duration: 1000,
        color: '#10b981'
      });
    } else {
      anime({
        targets: '.hero h1 .word',
        color: ['#ffffff', '#10b981', '#ffffff'],
        scale: [1, 1.05, 1],
        duration: 1500,
        delay: anime.stagger(50),
        easing: 'easeInOutQuad'
      });
    }
  });
}

// Custom cursor with magnetic effect
const cursor = document.createElement('div');
const cursorDot = document.createElement('div');
cursor.className = 'custom-cursor';
cursorDot.className = 'custom-cursor-dot';

cursor.style.cssText = `
  width: 40px;
  height: 40px;
  border: 2px solid #10b981;
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: difference;
  transition: width 0.3s ease, height 0.3s ease, border-color 0.3s ease;
  display: none;
`;

cursorDot.style.cssText = `
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: 10000;
  display: none;
`;

document.body.appendChild(cursor);
document.body.appendChild(cursorDot);

let mouseX = 0, mouseY = 0;
let cursorX = 0, cursorY = 0;
let dotX = 0, dotY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  cursor.style.display = 'block';
  cursorDot.style.display = 'block';
});

// Smooth cursor follow
function animateCursor() {
  cursorX += (mouseX - cursorX) * 0.15;
  cursorY += (mouseY - cursorY) * 0.15;
  dotX += (mouseX - dotX) * 0.25;
  dotY += (mouseY - dotY) * 0.25;
  
  cursor.style.left = cursorX - 20 + 'px';
  cursor.style.top = cursorY - 20 + 'px';
  cursorDot.style.left = dotX - 4 + 'px';
  cursorDot.style.top = dotY - 4 + 'px';
  
  requestAnimationFrame(animateCursor);
}
animateCursor();

// Cursor scale on interactive elements
const interactiveElements = document.querySelectorAll('a, button, .btn');
interactiveElements.forEach(el => {
  el.addEventListener('mouseenter', () => {
    cursor.style.width = '60px';
    cursor.style.height = '60px';
    cursor.style.borderColor = '#34d399';
    cursorDot.style.transform = 'scale(1.5)';
  });
  
  el.addEventListener('mouseleave', () => {
    cursor.style.width = '40px';
    cursor.style.height = '40px';
    cursor.style.borderColor = '#10b981';
    cursorDot.style.transform = 'scale(1)';
  });
});

// Logo pulse and rotate animation
const logo = document.querySelector('.brand .logo');
if (logo) {
  anime({
    targets: logo,
    scale: [1, 1.08, 1],
    rotate: ['0deg', '5deg', '0deg'],
    easing: 'easeInOutSine',
    duration: 3000,
    loop: true
  });
  
  logo.addEventListener('mouseenter', () => {
    anime({
      targets: logo,
      rotate: '360deg',
      duration: 800,
      easing: 'easeOutCubic'
    });
  });
}

// Navigation link hover with line animation
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(link => {
  const underline = document.createElement('span');
  underline.style.cssText = `
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #10b981, #34d399);
    transition: width 0.3s ease;
  `;
  link.style.position = 'relative';
  link.appendChild(underline);
  
  link.addEventListener('mouseenter', () => {
    anime({
      targets: link,
      scale: 1.05,
      duration: 300,
      easing: 'easeOutQuad'
    });
    anime({
      targets: underline,
      width: '100%',
      duration: 400,
      easing: 'easeOutCubic'
    });
  });
  
  link.addEventListener('mouseleave', () => {
    anime({
      targets: link,
      scale: 1,
      duration: 300,
      easing: 'easeOutQuad'
    });
    anime({
      targets: underline,
      width: '0%',
      duration: 400,
      easing: 'easeOutCubic'
    });
  });
});

// Add scroll progress indicator
const progressBar = document.createElement('div');
progressBar.style.cssText = `
  position: fixed;
  top: 0;
  left: 0;
  width: 0%;
  height: 3px;
  background: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
  z-index: 9999;
  transition: width 0.1s ease;
`;
document.body.appendChild(progressBar);

window.addEventListener('scroll', () => {
  const winScroll = document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const scrolled = (winScroll / height) * 100;
  progressBar.style.width = scrolled + '%';
});
