// ===== LOYALBREW SECURITY PATCH =====
// Add rate limiting, XSS sanitization, and file validation
// Include this AFTER app.js loads

(function() {
  'use strict';
  
  // ===== RATE LIMITING =====
  var _rateLimits = {
    login: { attempts: 0, lockedUntil: 0 },
    register: { attempts: 0, lockedUntil: 0 }
  };

  window._secCheckRateLimit = function(type, maxAttempts, lockoutMs) {
    var rl = _rateLimits[type];
    if (!rl) return true;
    var now = Date.now();
    if (rl.lockedUntil > now) {
      var remaining = Math.ceil((rl.lockedUntil - now) / 1000);
      if (typeof showToast === 'function') {
        showToast('Too many attempts. Wait ' + remaining + ' seconds', 'error');
      }
      return false;
    }
    return true;
  };

  window._secRecordFailure = function(type, maxAttempts, lockoutMs) {
    var rl = _rateLimits[type];
    if (!rl) return;
    rl.attempts++;
    if (rl.attempts >= (maxAttempts || 5)) {
      rl.lockedUntil = Date.now() + (lockoutMs || 60000);
      rl.attempts = 0;
      if (typeof showToast === 'function') {
        showToast('Account temporarily locked due to too many attempts', 'error');
      }
    }
  };

  window._secReset = function(type) {
    var rl = _rateLimits[type];
    if (rl) { rl.attempts = 0; rl.lockedUntil = 0; }
  };

  // ===== ENHANCED XSS SANITIZATION =====
  window._secSanitize = function(str, maxLen) {
    if (!str) return '';
    var s = String(str);
    // Remove null bytes
    s = s.replace(/\0/g, '');
    // Escape HTML entities
    s = s.replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/\//g, '&#47;');
    // Remove control characters
    s = s.replace(/[\x00-\x1F\x7F]/g, '');
    // Trim and limit length
    if (maxLen && s.length > maxLen) {
      s = s.substring(0, maxLen);
    }
    return s.trim();
  };

  // ===== FILE VALIDATION =====
  window._secValidateFile = function(file, maxSizeMB) {
    if (!file) return { valid: false, error: 'No file provided' };
    
    // Check size
    var maxBytes = (maxSizeMB || 5) * 1024 * 1024;
    if (file.size > maxBytes) {
      return { valid: false, error: 'File too large. Max ' + (maxSizeMB || 5) + 'MB allowed.' };
    }
    
    // Check MIME type
    var allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
      return { valid: false, error: 'Invalid file type. Only JPEG, PNG, GIF allowed.' };
    }
    
    // Check extension
    var ext = (file.name || '').toLowerCase().split('.').pop();
    if (!['jpg', 'jpeg', 'png', 'gif'].includes(ext)) {
      return { valid: false, error: 'Invalid file extension.' };
    }
    
    return { valid: true };
  };

  // ===== SECURE DOM TEXT SETTING =====
  window._secSetText = function(elementId, text) {
    var el = typeof elementId === 'string' ? document.getElementById(elementId) : elementId;
    if (el) {
      el.textContent = text || '';
    }
  };

  console.log('[Security] Security patch loaded');
})();