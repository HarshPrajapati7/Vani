/**
 * Vani App - Tier 1 Animations & Micro-interactions
 * Enhanced user experience with smooth transitions, loading states, and feedback animations
 */

// ========================================================================
// LOADING STATE MANAGER
// ========================================================================

class LoadingStateManager {
  static showSkeleton(containerId, type = 'card', count = 1) {
    const container = document.getElementById(containerId);
    if (!container) return;

    let html = '';
    for (let i = 0; i < count; i++) {
      if (type === 'card') {
        html += `
          <div class="skeleton-card">
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
          </div>
        `;
      } else if (type === 'stat') {
        html += `
          <div class="skeleton-stat">
            <div class="skeleton-line"></div>
            <div class="skeleton-value"></div>
            <div class="skeleton-line"></div>
          </div>
        `;
      } else if (type === 'chart') {
        html += `<div class="skeleton-chart"></div>`;
      }
    }
    container.innerHTML = html;
  }

  static clearSkeleton(containerId) {
    const container = document.getElementById(containerId);
    if (container) container.innerHTML = '';
  }

  static showSpinner(text = 'Loading...') {
    const spinner = document.createElement('div');
    spinner.className = 'loading-overlay';
    spinner.innerHTML = `
      <div class="loading-content">
        <div class="spinner"></div>
        <p>${text}</p>
      </div>
    `;
    spinner.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      backdrop-filter: blur(4px);
    `;
    spinner.querySelector('.loading-content').style.cssText = `
      background: white;
      border-radius: 12px;
      padding: 32px;
      text-align: center;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    `;
    document.body.appendChild(spinner);
    return spinner;
  }

  static hideSpinner() {
    const spinner = document.querySelector('.loading-overlay');
    if (spinner) {
      spinner.style.animation = 'fadeOut 0.2s cubic-bezier(0.4, 0, 0.2, 1)';
      setTimeout(() => spinner.remove(), 200);
    }
  }
}

// ========================================================================
// TOAST NOTIFICATION MANAGER
// ========================================================================

class ToastManager {
  static show(message, type = 'success', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const typeIcon = {
      success: '✓',
      error: '✕',
      warning: '!',
      info: 'ℹ'
    };

    toast.innerHTML = `
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 18px; font-weight: bold;">${typeIcon[type]}</span>
        <span>${message}</span>
      </div>
    `;

    document.body.appendChild(toast);

    // Auto-dismiss
    setTimeout(() => {
      toast.classList.add('closing');
      setTimeout(() => toast.remove(), 300);
    }, duration);

    return toast;
  }

  static success(message, duration = 3000) {
    return this.show(message, 'success', duration);
  }

  static error(message, duration = 4000) {
    return this.show(message, 'error', duration);
  }

  static warning(message, duration = 3000) {
    return this.show(message, 'warning', duration);
  }

  static info(message, duration = 3000) {
    return this.show(message, 'info', duration);
  }
}

// ========================================================================
// FORM VALIDATION & FEEDBACK
// ========================================================================

class FormValidator {
  constructor(formId) {
    this.form = document.getElementById(formId);
    this.errors = {};
    
    if (this.form) {
      this.setupValidation();
    }
  }

  setupValidation() {
    // Real-time validation on input
    this.form.querySelectorAll('input, textarea, select').forEach(field => {
      field.addEventListener('blur', () => this.validateField(field));
      field.addEventListener('change', () => this.validateField(field));
    });

    // Form submit
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  validateField(field) {
    const rules = field.dataset.validate?.split('|') || [];
    const value = field.value.trim();
    let error = null;

    for (const rule of rules) {
      if (rule === 'required' && !value) {
        error = 'This field is required';
        break;
      }
      if (rule === 'email' && value && !this.isValidEmail(value)) {
        error = 'Please enter a valid email';
        break;
      }
      if (rule === 'phone' && value && !this.isValidPhone(value)) {
        error = 'Please enter a valid phone number';
        break;
      }
      if (rule === 'number' && value && isNaN(value)) {
        error = 'Please enter a valid number';
        break;
      }
    }

    this.setFieldState(field, error);
    this.errors[field.name] = error;
    return !error;
  }

  setFieldState(field, error) {
    // Remove existing feedback
    field.classList.remove('input-success', 'input-error');
    const existingHelper = field.parentElement.querySelector('.input-helper');
    if (existingHelper) existingHelper.remove();

    if (error) {
      field.classList.add('input-error');
      const helper = document.createElement('div');
      helper.className = 'input-helper error';
      helper.textContent = error;
      field.parentElement.appendChild(helper);
    } else if (field.value.trim()) {
      field.classList.add('input-success');
      const helper = document.createElement('div');
      helper.className = 'input-helper success';
      helper.textContent = '✓ Looks good';
      field.parentElement.appendChild(helper);
    }
  }

  isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  isValidPhone(phone) {
    return /^[\d\s\-\+\(\)]{10,}$/.test(phone);
  }

  handleSubmit(e) {
    e.preventDefault();
    
    let isValid = true;
    this.form.querySelectorAll('input, textarea, select').forEach(field => {
      if (!this.validateField(field)) {
        isValid = false;
      }
    });

    if (isValid) {
      this.showSuccess();
    } else {
      ToastManager.error('Please fix the errors below');
    }
  }

  showSuccess() {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-state';
    successDiv.innerHTML = `
      <div class="success-checkmark"></div>
      <h3 style="text-align: center; color: var(--dark-forest);">Successfully submitted!</h3>
      <p style="text-align: center; color: var(--text-muted); margin-top: 8px;">Your data has been saved.</p>
    `;
    successDiv.style.cssText = `
      padding: 32px;
      text-align: center;
      background: rgba(16, 185, 129, 0.05);
      border-radius: 12px;
      margin-top: 16px;
    `;
    this.form.parentElement.appendChild(successDiv);
    
    // Reset form after 2 seconds
    setTimeout(() => {
      this.form.reset();
      successDiv.remove();
    }, 2000);
  }
}

// ========================================================================
// EMPTY STATE HANDLER
// ========================================================================

class EmptyStateHandler {
  static show(containerId, icon, title, description, actionText = null, actionCallback = null) {
    const container = document.getElementById(containerId);
    if (!container) return;

    let html = `
      <div class="empty-state">
        <div class="empty-state-icon">${icon}</div>
        <h3 class="empty-state-title">${title}</h3>
        <p class="empty-state-description">${description}</p>
    `;

    if (actionText && actionCallback) {
      html += `
        <div class="empty-state-action">
          <button class="btn btn-primary" onclick="window.__emptyStateCallback()">${actionText}</button>
        </div>
      `;
      window.__emptyStateCallback = actionCallback;
    }

    html += `</div>`;
    container.innerHTML = html;
  }

  static showNoFarms() {
    this.show('farmsTable', '🌾', 
      'No Farms Registered',
      'Start by adding your first farm to begin monitoring crop health and flood risks.',
      'Add Farm',
      () => {
        document.querySelector('.card-title').scrollIntoView({ behavior: 'smooth' });
        document.getElementById('farmerName').focus();
      }
    );
  }

  static showNoClaims() {
    this.show('claimsTimeline', '📋',
      'No Claims Yet',
      'When your farms are affected by flooding, you can file insurance claims here.',
      'Learn More',
      () => window.open('#', '_blank')
    );
  }

  static showNoAlerts() {
    this.show('weatherAlerts', '🌤️',
      'No Active Alerts',
      'Weather conditions are currently normal. We\'ll notify you of any alerts.',
      null
    );
  }
}

// ========================================================================
// BUTTON FEEDBACK MANAGER
// ========================================================================

class ButtonFeedback {
  static attach(selector) {
    document.querySelectorAll(selector).forEach(btn => {
      btn.addEventListener('click', (e) => {
        if (btn.disabled) return;
        
        // Create ripple effect
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
          pointer-events: none;
          animation: ripple 0.6s ease-out;
        `;

        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
      });
    });
  }
}

// Add ripple animation
if (!document.querySelector('style[data-animations]')) {
  const style = document.createElement('style');
  style.setAttribute('data-animations', 'true');
  style.textContent = `
    @keyframes ripple {
      to {
        width: 100px;
        height: 100px;
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);
}

// ========================================================================
// SCROLL REVEAL ANIMATIONS
// ========================================================================

class ScrollReveal {
  static setup() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.card, .stat-card, .timeline-item').forEach(el => {
      el.classList.add('reveal-item');
      observer.observe(el);
    });
  }
}

// Add reveal item styles
if (!document.querySelector('style[data-reveal]')) {
  const style = document.createElement('style');
  style.setAttribute('data-reveal', 'true');
  style.textContent = `
    .reveal-item {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }
    .reveal-item.revealed {
      opacity: 1;
      transform: translateY(0);
    }
  `;
  document.head.appendChild(style);
}

// ========================================================================
// INITIALIZATION
// ========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // Attach button feedback
  ButtonFeedback.attach('.btn, button');

  // Setup scroll reveal
  ScrollReveal.setup();
});

// Export for global use
window.LoadingStateManager = LoadingStateManager;
window.ToastManager = ToastManager;
window.FormValidator = FormValidator;
window.EmptyStateHandler = EmptyStateHandler;
window.ButtonFeedback = ButtonFeedback;
window.ScrollReveal = ScrollReveal;
