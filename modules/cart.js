// ===== CART / CHECKOUT =====
// modules/cart.js — Extracted from app.js (lines 2538–2844)

let cart = [];
let orderType = 'dinein'; // 'dinein' | 'takeaway'
let currentTable = null;
let takeawayPhone = '';
let takeawayTime = '';
let cartMember = null;
let _pendingRedirect = null;

// ---- Order Type ----
function setOrderType(type) {
  orderType = type;
  if (type === 'dinein') {
    if (!currentTable) { changeTable(); return; }
  }
  renderMenu();
  updateCartBadge();
  updateFloatCart();
}

function confirmTakeaway() {
  const phone = document.getElementById('takeaway-phone-input')?.value.trim();
  const time  = document.getElementById('takeaway-time-input')?.value;
  if (!phone) { showToast(t('toastNoPhone'), 'error'); return; }
  if (!time)  { showToast(t('toastNoTime'), 'error'); return; }
  takeawayPhone = phone;
  takeawayTime  = time;
  closeTableModal();
  showPage('page-menu');
}

function cancelTakeaway() {
  orderType = 'dinein';
  if (!currentTable) changeTable();
  else showPage('page-menu');
}

function catLabel(c) { return CAT_I18N[c] ? t(CAT_I18N[c]) : c; }

// ---- Menu Rendering ----
function renderMenu() {
  const menu = DB.getMenu() || DEFAULT_MENU;
  const listEl = document.getElementById('menu-items-list');
  if (!listEl) return;

  listEl.innerHTML = menu.map(item => {
    const eff = getEffectivePrice(item);
    const inCart = cart.find(c => c.id === item.id);
    return `
    <div class="menu-item ${eff.isPromo ? 'promo-item' : ''}" onclick="addToCart('${item.id}')">
      <div class="menu-item-left">
        <span class="menu-emoji">${item.emoji || '🍽️'}</span>
        <div class="menu-item-info">
          <strong>${item.name}</strong>
          <small>${item.desc || ''}</small>
          <div class="menu-price-row">
            ${eff.isPromo
              ? `<span class="price-orig">RM${item.price.toFixed(2)}</span><span class="price-promo">RM${eff.price.toFixed(2)}</span>`
              : `<span class="price-normal">RM${item.price.toFixed(2)}</span>`}
          </div>
        </div>
      </div>
      <div class="menu-item-right">
        ${inCart
          ? `<div class="menu-qty-ctrl" onclick="event.stopPropagation();changeCartQty('${item.id}',1)">
               <button class="qty-btn" onclick="event.stopPropagation();changeMenuQty('${item.id}',-1)">−</button>
               <span>${inCart.qty}</span>
               <button class="qty-btn" onclick="event.stopPropagation();changeMenuQty('${item.id}',1)">+</button>
             </div>`
          : `<button class="add-btn">+</button>`}
      </div>
    </div>`;
  }).join('');
}

// ---- Category Filter ----
let currentCategory = 'all';
function filterCategory(cat) {
  currentCategory = cat;
  // Update active tab
  document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
  const activeBtn = document.querySelector(`.cat-btn[data-cat="${cat}"]`);
  if (activeBtn) activeBtn.classList.add('active');
  // Filter menu items in DOM
  const items = document.querySelectorAll('.menu-item');
  items.forEach(el => {
    const itemCat = el.getAttribute('data-category') || '';
    const show = cat === 'all' || itemCat === cat;
    el.style.display = show ? '' : 'none';
  });
}

// ---- Cart Operations ----
function addToCart(id) {
  const menu = DB.getMenu() || DEFAULT_MENU;
  const item = menu.find(m => m.id === id);
  if (!item) return;
  const eff = getEffectivePrice(item);
  const existing = cart.find(c => c.id === id);
  if (existing) {
    existing.qty++;
  } else {
    cart.push({ id: item.id, name: item.name, emoji: item.emoji, price: eff.price, qty: 1 });
  }
  updateCartBadge();
  updateFloatCart();
  showToast(`${item.emoji} ${item.name} added!`);
}

function changeMenuQty(id, delta) {
  const idx = cart.findIndex(c => c.id === id);
  if (idx === -1) return;
  cart[idx].qty += delta;
  if (cart[idx].qty <= 0) cart.splice(idx, 1);
  renderMenu();
  updateCartBadge();
  updateFloatCart();
}

// ---- Table Selection ----
function changeTable() {
  document.getElementById('table-modal')?.classList.remove('hidden');
}
function closeTableModal() {
  document.getElementById('table-modal')?.classList.add('hidden');
}
function confirmTable() {
  const input = document.getElementById('table-number-input');
  const val = parseInt(input?.value);
  if (!val || val < 1) { showToast(t('invalidTable'), 'error'); return; }
  currentTable = val;
  closeTableModal();
  showPage('page-menu');
  updateFloatCart();
}

// ---- Cart Page Rendering ----
function renderCart() {
  const listEl = document.getElementById('cart-items-list');
  if (cart.length === 0) {
    listEl.innerHTML = `<div class="cart-empty">
      <i class="fas fa-shopping-cart"></i>
      <p>${t('cartEmpty')}</p>
      <button class="btn-primary" onclick="showPage('page-menu')">${t('browseMenu')}</button>
    </div>`;
    document.getElementById('sum-subtotal').textContent = 'RM0.00';
    document.getElementById('sum-tax').textContent = 'RM0.00';
    document.getElementById('sum-total').textContent = 'RM0.00';
    document.getElementById('sum-points').textContent = '+0 pts';
  } else {
    listEl.innerHTML = cart.map(item => `
      <div class="cart-item">
        <span class="cart-item-emoji">${item.emoji}</span>
        <div class="cart-item-info">
          <strong>${item.name}</strong>
          <small>RM${item.price.toFixed(2)} ${t('eachUnit')}</small>
        </div>
        <div class="cart-item-right">
          <span class="cart-item-price">RM${(item.price * item.qty).toFixed(2)}</span>
          <div class="cart-qty-row">
            <button class="cqty-btn" onclick="changeCartQty('${item.id}',-1)">−</button>
            <span class="cqty-num">${item.qty}</span>
            <button class="cqty-btn" onclick="changeCartQty('${item.id}',1)">+</button>
          </div>
          <button class="remove-btn" onclick="removeCartItem('${item.id}')">
            <i class="fas fa-trash"></i> ${t('removeItem')}
          </button>
        </div>
      </div>`).join('');
    updateCartSummary();
  }

  // Order type display
  const otDisplay = document.getElementById('order-type-display');
  const takeawayFields = document.getElementById('takeaway-fields');
  const dineinField    = document.getElementById('dinein-field');
  if (orderType === 'takeaway') {
    otDisplay.className = 'order-type-display takeaway';
    otDisplay.innerHTML = `<i class="fas fa-shopping-bag"></i><span>${t('cartTakeaway')}</span>
      <button class="ot-change" onclick="showPage('page-menu');setOrderType('takeaway')">${t('cartChange')}</button>`;
    takeawayFields?.classList.remove('hidden');
    dineinField?.classList.add('hidden');
    const phEl = document.getElementById('takeaway-phone');
    const tmEl = document.getElementById('takeaway-time');
    if (takeawayPhone && phEl) phEl.value = takeawayPhone;
    if (takeawayTime  && tmEl) tmEl.value = takeawayTime;
  } else {
    otDisplay.className = 'order-type-display dinein';
    otDisplay.innerHTML = `<i class="fas fa-chair"></i><span>${t('cartDineIn')}</span>
      <button class="ot-change" onclick="showPage('page-menu')">${t('cartChange')}</button>`;
    takeawayFields?.classList.add('hidden');
    dineinField?.classList.remove('hidden');
    document.getElementById('cart-table-display').textContent = currentTable || '-';
  }
  if (orderType === 'takeaway' && takeawayPhone) {
    const cartPhoneEl = document.getElementById('cart-phone');
    if (cartPhoneEl && !cartPhoneEl.value) cartPhoneEl.value = takeawayPhone;
  }
}

function changeCartQty(id, delta) {
  const idx = cart.findIndex(c => c.id === id);
  if (idx === -1) return;
  cart[idx].qty += delta;
  if (cart[idx].qty <= 0) cart.splice(idx, 1);
  renderCart();
  updateCartBadge();
  updateFloatCart();
}

function removeCartItem(id) {
  cart = cart.filter(c => c.id !== id);
  renderCart();
  updateCartBadge();
  updateFloatCart();
}

function updateCartSummary() {
  const subtotal = cart.reduce((s, c) => s + c.price * c.qty, 0);
  const tax      = subtotal * 0.06;
  let total      = subtotal + tax;

  const useWallet    = document.getElementById('use-wallet-checkbox')?.checked;
  let walletDeduct = 0;
  if (useWallet && cartMember) {
    const wallet = getMemberWallet(cartMember.id);
    walletDeduct = Math.min(wallet.balance, total);
    total = Math.max(0, total - walletDeduct);
  }

  const _psRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;
  const pts = Math.floor(total * _psRate);

  document.getElementById('sum-subtotal').textContent = 'RM' + subtotal.toFixed(2);
  document.getElementById('sum-tax').textContent      = 'RM' + tax.toFixed(2);
  document.getElementById('sum-total').textContent     = 'RM' + total.toFixed(2);
  document.getElementById('sum-points').textContent   = '+' + pts + ' pts';

  const deductRow = document.getElementById('wallet-deduct-row');
  if (walletDeduct > 0) {
    deductRow?.classList.remove('hidden');
    document.getElementById('sum-wallet-deduct').textContent = '-RM' + walletDeduct.toFixed(2);
  } else {
    deductRow?.classList.add('hidden');
  }
}

function toggleWalletPay() { updateCartSummary(); }

// ---- Member Lookup in Cart ----
function lookupCartMember() {
  const phone = document.getElementById('cart-phone').value.trim();
  if (!phone) return;
  const member = DB.getMembers().find(m => m.phone === phone);
  const infoEl = document.getElementById('cart-member-info');
  if (!member) {
    cartMember = null;
    infoEl.innerHTML = '<span style="color:#c62828">Member not found</span>';
    infoEl.classList.remove('hidden');
    document.getElementById('wallet-pay-section')?.classList.add('hidden');
    return;
  }
  cartMember = member;
  infoEl.innerHTML = `<i class="fas fa-user-circle"></i> <div><strong>${member.name}</strong><br>
    <small>${getTier(member.points)} · ${member.points} pts</small></div>`;
  infoEl.classList.remove('hidden');
  const wallet = getMemberWallet(member.id);
  const walletSection = document.getElementById('wallet-pay-section');
  walletSection?.classList.remove('hidden');
  document.getElementById('wallet-pay-info').innerHTML =
    `<div class="wallet-mini-balance"><i class="fas fa-wallet"></i> Balance: <strong>RM${wallet.balance.toFixed(2)}</strong></div>`;
  document.getElementById('use-wallet-checkbox').checked = false;
  updateCartSummary();
}

// ---- Place Order ----
function placeOrder() {
  if (cart.length === 0) { showToast(t('cartEmpty'), 'error'); return; }

  let finalPhone = '';
  let finalPickupTime = '';

  if (orderType === 'dinein') {
    if (!currentTable) {
      showToast(t('selectTableFirst'), 'error');
      showPage('page-menu');
      changeTable();
      return;
    }
  } else {
    const tPhone = document.getElementById('takeaway-phone')?.value.trim();
    const tTime  = document.getElementById('takeaway-time')?.value;
    if (!tPhone) { showToast(t('toastNoPhone'), 'error'); return; }
    if (!tTime)  { showToast(t('toastNoTime'), 'error');  return; }
    finalPhone      = tPhone;
    finalPickupTime = tTime;
    takeawayPhone   = tPhone;
    takeawayTime    = tTime;
  }

  const subtotal = cart.reduce((s, c) => s + c.price * c.qty, 0);
  const tax      = subtotal * 0.06;
  let total      = subtotal + tax;

  const useWallet   = document.getElementById('use-wallet-checkbox')?.checked;
  const payMethod   = document.querySelector('input[name="payment"]:checked')?.value || 'cash';
  let walletDeduct  = 0;
  let memberId      = null;
  let walletBalance = 0;

  // Member lookup
  const phoneInput  = (orderType === 'takeaway'
    ? document.getElementById('takeaway-phone')?.value.trim()
    : document.getElementById('cart-phone')?.value.trim()) || '';
  const lookupMember = phoneInput
    ? DB.getMembers().find(m => m.phone === phoneInput)
    : null;

  if (lookupMember) {
    memberId = lookupMember.id;
    if (useWallet) {
      const w = getMemberWallet(memberId);
      walletBalance = w.balance;
      walletDeduct = Math.min(w.balance, total);
      total = Math.max(0, total - walletDeduct);
    }
  }

  // Payment proof
  const proofEl = document.getElementById('payment-proof-preview');
  const proofImg = proofEl?.src || '';

  // Special request
  const noteEl = document.getElementById('special-request');
  const note   = noteEl?.value?.trim() || '';

  const orderId   = 'ORD' + Date.now();
  const _psRate   = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;
  const pointsEarn = Math.floor(total * _psRate);

  const order = {
    id: orderId,
    items: cart.map(c => ({ id: c.id, name: c.name, emoji: c.emoji, price: c.price, qty: c.qty })),
    subtotal, tax, total,
    table: currentTable,
    pickupTime: finalPickupTime,
    phone: finalPhone || phoneInput,
    memberId,
    memberName: lookupMember?.name || '',
    paymentMethod: payMethod,
    paymentProof: proofImg,
    walletDeduct,
    walletBalance: walletBalance - walletDeduct,
    pointsEarn,
    note,
    status: 'pending',
    createdAt: new Date().toISOString(),
    orderType,
  };

  // Save order
  const orders = DB.getOrders();
  orders.push(order);
  DB.saveOrders(orders);

  // Award stamps
  if (memberId) awardStampsForOrder(order);

  // Clear cart
  cart = [];
  updateCartBadge();
  updateFloatCart();

  // Show confirm page
  showOrderConfirm(order);
}

// ---- Order Confirmation View ----
function showOrderConfirm(order) {
  showPage('page-order-confirm');
  const el = document.getElementById('confirm-order-details');
  if (!el) return;
  el.innerHTML = `
    <div class="confirm-header">
      <div class="confirm-icon">✅</div>
      <h2>${t('orderPlaced')}</h2>
      <p>${t('thankYou')}</p>
      <p class="confirm-order-id">${order.id}</p>
    </div>
    <div class="confirm-items">
      ${order.items.map(i => `
        <div class="confirm-item">
          <span>${i.emoji} ${i.name} <em>×${i.qty}</em></span>
          <span>RM${(i.price * i.qty).toFixed(2)}</span>
        </div>`).join('')}
    </div>
    <div class="confirm-summary">
      <div class="confirm-row"><span>${t('subtotal')}</span><span>RM${order.subtotal.toFixed(2)}</span></div>
      <div class="confirm-row"><span>${t('sst')}</span><span>RM${order.tax.toFixed(2)}</span></div>
      ${order.walletDeduct > 0 ? `<div class="confirm-row wallet-row"><span>${t('walletDeduction')}</span><span>-RM${order.walletDeduct.toFixed(2)}</span></div>` : ''}
      <div class="confirm-row total-row"><span>${t('totalLabel')}</span><span>RM${order.total.toFixed(2)}</span></div>
    </div>
    <div class="confirm-meta">
      ${order.orderType === 'dinein'
        ? `<div class="confirm-meta-row"><i class="fas fa-chair"></i> ${t('confirmTable2')}: <strong>${order.table}</strong></div>`
        : `<div class="confirm-meta-row"><i class="fas fa-clock"></i> ${t('confirmPickup')}: <strong>${order.pickupTime}</strong></div>`}
      ${order.phone ? `<div class="confirm-meta-row"><i class="fas fa-phone"></i> ${order.phone}</div>` : ''}
      ${order.paymentMethod === 'cash' ? `<div class="confirm-meta-row cash-notice"><i class="fas fa-info-circle"></i> ${t('cashPayCounter')}</div>` : ''}
      ${order.pointsEarn > 0 ? `<div class="confirm-meta-row"><i class="fas fa-star"></i> ${t('confirmPointsEarned')}: <strong>+${order.pointsEarn} pts</strong></div>` : ''}
    </div>
    <div id="confirm-stamp-earned" class="hidden" style="margin-top:12px"></div>
    <div class="confirm-actions">
      <button class="btn-secondary" onclick="showPage('page-menu')">${t('orderMore')}</button>
      <button class="btn-primary" onclick="gotoStampFromDash()">${t('viewStamp')}</button>
    </div>`;

  // Cash pay: show notify kitchen button
  if (order.paymentMethod === 'cash') {
    el.innerHTML += `<button class="btn-orange" style="width:100%;margin-top:12px" onclick="confirmCashPaidFromDetail('${order.id}')">
      ${t('cashPaidBtn')}
    </button>`;
  }
}

// ---- Badge & Float Cart ----
function updateCartBadge() {
  const badge = document.getElementById('cart-badge');
  if (badge) badge.textContent = cart.reduce((s, c) => s + c.qty, 0);
}

function updateFloatCart() {
  const float = document.getElementById('float-cart');
  if (!float) return;
  const count = cart.reduce((s, c) => s + c.qty, 0);
  if (count === 0) {
    float.classList.add('hidden');
    return;
  }
  const total = cart.reduce((s, c) => s + c.price * c.qty, 0);
  float.classList.remove('hidden');
  document.getElementById('float-cart-count').textContent =
    count + (count === 1 ? ' ' + t('floatItem') : ' ' + t('floatItems'));
  document.getElementById('float-cart-total').textContent = 'RM' + total.toFixed(2);
}
