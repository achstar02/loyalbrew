// ===== DATA STORE & CONSTANTS =====
// modules/data.js — Extracted from app.js

// ===== SAFE LOCALSTORAGE WRAPPER =====
const safeLS = (() => {
  const noop = () => {};
  const ls = (() => {
    try { return localStorage; } catch(e) { return { getItem: noop, setItem: noop, removeItem: noop }; }
  })();
  return {
    get(k, fb)    { try { const v = ls.getItem(k); return v !== null ? v : (fb !== undefined ? fb : null); } catch(e) { return fb !== undefined ? fb : null; } },
    set(k, v)     { try { ls.setItem(k, String(v)); } catch(e) { /* quota/unavailable */ } },
    del(k)        { try { ls.removeItem(k); } catch(e) { /* noop */ } },
    json(k, fb)   { try { const v = ls.getItem(k); if (v === null) return fb !== undefined ? fb : null; return JSON.parse(v); } catch(e) { return fb !== undefined ? fb : null; } },
    setJSON(k, v)  { try { ls.setItem(k, JSON.stringify(v)); } catch(e) { /* quota/unavailable */ } }
  };
})();

// ===== MERCHANT DATA ISOLATION =====
function _getCurrentMerchantId() {
  return window._currentMerchantId || 'default';
}
function _getMerchantStorageKey(baseKey) {
  const mid = _getCurrentMerchantId();
  return mid === 'default' ? baseKey : baseKey + '_' + mid;
}

// ===== DATABASE LAYER (localStorage) =====
const DB = {
  getMembers()          { return safeLS.json(_getMerchantStorageKey('loyalbrew_members') || '[]'); },
  saveMembers(m)        { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_members'), m); },
  getTxns()             { return safeLS.json(_getMerchantStorageKey('loyalbrew_txns') || '[]'); },
  saveTxns(t)           { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_txns'), t); },
  getOrders()           { return safeLS.json(_getMerchantStorageKey('loyalbrew_orders') || '[]'); },
  saveOrders(o)         { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_orders'), o); },
  getMenu()             { return safeLS.json(_getMerchantStorageKey('loyalbrew_menu') || 'null'); },
  saveMenu(m)           { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_menu'), m); },
  getNewItems()         { return safeLS.json(_getMerchantStorageKey('loyalbrew_new_items') || '[]'); },
  saveNewItems(n)       { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_new_items'), n); },
  getAnnounceSeen()     { return safeLS.get('loyalbrew_announce_seen') || ''; },
  setAnnounceSeen(v)    { safeLS.set('loyalbrew_announce_seen', v); },
  getStampCards()       { return safeLS.json(_getMerchantStorageKey('loyalbrew_stamp_cards') || '[]'); },
  saveStampCards(s)     { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_stamp_cards'), s); },
  getMemberStamps()     { return safeLS.json(_getMerchantStorageKey('loyalbrew_member_stamps') || '{}'); },
  saveMemberStamps(s)   { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_member_stamps'), s); },
  getWallets()          { return safeLS.json(_getMerchantStorageKey('loyalbrew_wallets') || '{}'); },
  saveWallets(w)        { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_wallets'), w); },
  getWalletTxns()       { return safeLS.json(_getMerchantStorageKey('loyalbrew_wallet_txns') || '[]'); },
  saveWalletTxns(t)     { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_wallet_txns'), t); },
  getComplaints()       { return safeLS.json(_getMerchantStorageKey('loyalbrew_complaints') || '[]'); },
  saveComplaints(c)     { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_complaints'), c); },
  getTopupRequests()    { return safeLS.json(_getMerchantStorageKey('loyalbrew_topup_requests') || '[]'); },
  saveTopupRequests(r) { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_topup_requests'), r); },
  getCommissions()      { return safeLS.json(_getMerchantStorageKey('loyalbrew_commissions') || '[]'); },
  saveCommissions(c)   { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_commissions'), c); },
  getPaymentProofs()    { return safeLS.json(_getMerchantStorageKey('loyalbrew_payment_proofs') || '[]'); },
  savePaymentProofs(p) { safeLS.setJSON(_getMerchantStorageKey('loyalbrew_payment_proofs'), p); },
  getCurrentMemberPhone()   { return safeLS.get('loyalbrew_current_member') || null; },
  setCurrentMemberPhone(p)  { if (p) safeLS.set('loyalbrew_current_member', p); else safeLS.del('loyalbrew_current_member'); },
};

// ===== DEFAULT MENU =====
const DEFAULT_MENU = [
  { id: 'm1',  name: 'Espresso',       emoji: '☕', price: 8.00,  category: 'Hot Drinks',  desc: 'Rich & bold single shot' },
  { id: 'm2',  name: 'Cappuccino',     emoji: '☕', price: 12.00, category: 'Hot Drinks',  desc: 'Espresso with steamed milk foam' },
  { id: 'm3',  name: 'Caramel Latte',  emoji: '🍮', price: 14.00, category: 'Hot Drinks',  desc: 'Sweet caramel with smooth latte' },
  { id: 'm4',  name: 'Teh Tarik',      emoji: '🍵', price: 7.00,  category: 'Hot Drinks',  desc: 'Classic pulled milk tea' },
  { id: 'm5',  name: 'Iced Americano', emoji: '🧊', price: 11.00, category: 'Cold Drinks', desc: 'Double shot over ice' },
  { id: 'm6',  name: 'Iced Latte',     emoji: '🥤', price: 13.00, category: 'Cold Drinks', desc: 'Chilled espresso with milk' },
  { id: 'm7',  name: 'Matcha Latte',   emoji: '🍵', price: 14.00, category: 'Cold Drinks', desc: 'Premium matcha over milk' },
  { id: 'm8',  name: 'Mango Smoothie', emoji: '🥭', price: 12.00, category: 'Cold Drinks', desc: 'Fresh mango blended smooth' },
  { id: 'm9',  name: 'Nasi Lemak',     emoji: '🍛', price: 13.00, category: 'Food',        desc: 'Coconut rice with classic sides' },
  { id: 'm10', name: 'Club Sandwich',  emoji: '🥪', price: 16.00, category: 'Food',        desc: 'Triple decker toasted sandwich' },
  { id: 'm11', name: 'Chicken Wrap',   emoji: '🌯', price: 15.00, category: 'Food',        desc: 'Grilled chicken in a soft tortilla' },
  { id: 'm12', name: 'Aglio Olio',     emoji: '🍝', price: 18.00, category: 'Food',        desc: 'Pasta with garlic and olive oil' },
  { id: 'm13', name: 'Chocolate Cake', emoji: '🎂', price: 11.00, category: 'Desserts',    desc: 'Rich moist chocolate slice' },
  { id: 'm14', name: 'Cheesecake',     emoji: '🍰', price: 12.00, category: 'Desserts',    desc: 'Creamy New York style' },
  { id: 'm15', name: 'Waffle',         emoji: '🧇', price: 14.00, category: 'Desserts',    desc: 'Crispy waffle with toppings' },
  { id: 'm16', name: 'French Fries',   emoji: '🍟', price: 9.00,  category: 'Snacks',      desc: 'Golden crispy fries' },
  { id: 'm17', name: 'Chicken Wings',  emoji: '🍗', price: 15.00, category: 'Snacks',      desc: '6 pieces crispy wings' },
  { id: 'm18', name: 'Garlic Bread',   emoji: '🥖', price: 8.00,  category: 'Snacks',      desc: 'Toasted with herb butter' },
];

// ===== DEFAULT REWARDS =====
const REWARDS = [
  { id: 'r1', name: 'Free Coffee',   icon: '☕', points: 100, color: '#8B4513' },
  { id: 'r2', name: 'Free Muffin',   icon: '🧁', points: 80,  color: '#e91e63' },
  { id: 'r3', name: 'Free Tea',      icon: '🍵', points: 60,  color: '#4caf50' },
  { id: 'r4', name: '10% Discount',  icon: '🏷️', points: 150, color: '#ff9800' },
  { id: 'r5', name: 'Free Sandwich', icon: '🥪', points: 200, color: '#9c27b0' },
  { id: 'r6', name: 'Birthday Cake', icon: '🎂', points: 300, color: '#f44336' },
];

// ===== SEED DATA =====
function seedData() {
  if (DB.getMembers().length === 0) {
    DB.saveMembers([
      { id: 'MB001', name: 'Ahmad Razif', phone: '0123456789', email: 'ahmad@email.com', points: 850,  joinDate: '2024-01-15' },
      { id: 'MB002', name: 'Siti Nurul',  phone: '0112345678', email: 'siti@email.com',  points: 320,  joinDate: '2024-02-20' },
      { id: 'MB003', name: 'Raj Kumar',   phone: '0134567890', email: 'raj@email.com',   points: 1250, joinDate: '2023-11-10' },
      { id: 'MB004', name: 'Mei Ling',   phone: '0167891234', email: '',                points: 75,   joinDate: '2024-04-01' },
    ]);
    DB.saveTxns([
      { id: 't1', memberId: 'MB001', memberName: 'Ahmad Razif', type: 'earn',   points: 50,   note: 'RM50 purchase',  date: '2024-04-10' },
      { id: 't2', memberId: 'MB001', memberName: 'Ahmad Razif', type: 'redeem', points: -100, note: 'Free Coffee',    date: '2024-04-08' },
      { id: 't3', memberId: 'MB001', memberName: 'Ahmad Razif', type: 'earn',   points: 25,   note: 'RM25 purchase',  date: '2024-04-05' },
      { id: 't4', memberId: 'MB002', memberName: 'Siti Nurul',  type: 'earn',   points: 120,  note: 'RM120 purchase', date: '2024-04-09' },
      { id: 't5', memberId: 'MB003', memberName: 'Raj Kumar',   type: 'earn',   points: 200,  note: 'RM200 purchase', date: '2024-04-07' },
    ]);
  }
  if (!DB.getMenu()) DB.saveMenu(DEFAULT_MENU);
  // Seed demo stamp cards
  if (DB.getStampCards().length === 0) {
    DB.saveStampCards([
      {
        id: 'sc_demo1', name: 'Coffee Lover Card', emoji: '☕',
        totalStamps: 8, rule: 'per_order', ruleValue: null, ruleItemId: null,
        rewardType: 'free_item', rewardValue: 'm1',
        color: '#8B4513', active: true, createdAt: new Date().toISOString(),
      },
      {
        id: 'sc_demo2', name: 'Big Spender Card', emoji: '💰',
        totalStamps: 5, rule: 'per_amount', ruleValue: 20, ruleItemId: null,
        rewardType: 'discount_flat', rewardValue: 5,
        color: '#1b5e20', active: true, createdAt: new Date().toISOString(),
      },
    ]);
  }
}
