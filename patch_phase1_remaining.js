// Phase 1 Remaining: Merchant Data Isolation & ?m=xxx support
// This patch adds merchant-scoped data storage to the DB object

const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'app.js');
let content = fs.readFileSync(filePath, 'utf8');

// Helper to get current merchant ID
const getMerchantIdHelper = `
// ===== MERCHANT DATA ISOLATION HELPER =====
function _getCurrentMerchantId() {
  return window._currentMerchantId || 'default';
}
function _getMerchantStorageKey(baseKey) {
  const mid = _getCurrentMerchantId();
  return mid === 'default' ? baseKey : baseKey + '_' + mid;
}
`;

// Find the position after DB object closing brace
const dbObjectEnd = content.indexOf('};', content.indexOf('const DB = {'));
if (dbObjectEnd === -1) {
  console.error('Could not find DB object end');
  process.exit(1);
}

// Insert the helper after DB object
const insertPos = dbObjectEnd + 2;
content = content.slice(0, insertPos) + '\n' + getMerchantIdHelper + content.slice(insertPos);

// Now update DB methods to use merchant-scoped keys
// Replace getMembers
content = content.replace(
  /getMembers\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_members'\) \|\| '\[\]'\);\s*\}/,
  `getMembers()      { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_members')) || '[]'); }`
);

// Replace saveMembers
content = content.replace(
  /saveMembers\(m\)\s*\{\s*localStorage\.setItem\('loyalbrew_members', JSON\.stringify\(m\)\);\s*\}/,
  `saveMembers(m)    { localStorage.setItem(_getMerchantStorageKey('loyalbrew_members'), JSON.stringify(m)); }`
);

// Replace getTxns
content = content.replace(
  /getTxns\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_txns'\) \|\| '\[\]'\);\s*\}/,
  `getTxns()         { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_txns')) || '[]'); }`
);

// Replace saveTxns
content = content.replace(
  /saveTxns\(t\)\s*\{\s*localStorage\.setItem\('loyalbrew_txns', JSON\.stringify\(t\)\);\s*\}/,
  `saveTxns(t)       { localStorage.setItem(_getMerchantStorageKey('loyalbrew_txns'), JSON.stringify(t)); }`
);

// Replace getOrders
content = content.replace(
  /getOrders\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_orders'\) \|\| '\[\]'\);\s*\}/,
  `getOrders()       { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_orders')) || '[]'); }`
);

// Replace saveOrders
content = content.replace(
  /saveOrders\(o\)\s*\{\s*localStorage\.setItem\('loyalbrew_orders', JSON\.stringify\(o\)\);\s*\}/,
  `saveOrders(o)     { localStorage.setItem(_getMerchantStorageKey('loyalbrew_orders'), JSON.stringify(o)); }`
);

// Replace getMenu
content = content.replace(
  /getMenu\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_menu'\) \|\| 'null'\);\s*\}/,
  `getMenu()         { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_menu')) || 'null'); }`
);

// Replace saveMenu
content = content.replace(
  /saveMenu\(m\)\s*\{\s*localStorage\.setItem\('loyalbrew_menu', JSON\.stringify\(m\)\);\s*\}/,
  `saveMenu(m)       { localStorage.setItem(_getMerchantStorageKey('loyalbrew_menu'), JSON.stringify(m)); }`
);

// Replace getNewItems
content = content.replace(
  /getNewItems\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_new_items'\) \|\| '\[\]'\);\s*\}/,
  `getNewItems()     { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_new_items')) || '[]'); }`
);

// Replace saveNewItems
content = content.replace(
  /saveNewItems\(n\)\s*\{\s*localStorage\.setItem\('loyalbrew_new_items', JSON\.stringify\(n\)\);\s*\}/,
  `saveNewItems(n)   { localStorage.setItem(_getMerchantStorageKey('loyalbrew_new_items'), JSON.stringify(n)); }`
);

// Replace getStampCards
content = content.replace(
  /getStampCards\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_stamp_cards'\) \|\| '\[\]'\);\s*\}/,
  `getStampCards()   { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_stamp_cards')) || '[]'); }`
);

// Replace saveStampCards
content = content.replace(
  /saveStampCards\(s\)\s*\{\s*localStorage\.setItem\('loyalbrew_stamp_cards', JSON\.stringify\(s\)\);\s*\}/,
  `saveStampCards(s) { localStorage.setItem(_getMerchantStorageKey('loyalbrew_stamp_cards'), JSON.stringify(s)); }`
);

// Replace getMemberStamps
content = content.replace(
  /getMemberStamps\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_member_stamps'\) \|\| '{}\'\);\s*\}/,
  `getMemberStamps() { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_member_stamps')) || '{}'); }`
);

// Replace saveMemberStamps
content = content.replace(
  /saveMemberStamps\(s\)\s*\{\s*localStorage\.setItem\('loyalbrew_member_stamps', JSON\.stringify\(s\)\);\s*\}/,
  `saveMemberStamps(s) { localStorage.setItem(_getMerchantStorageKey('loyalbrew_member_stamps'), JSON.stringify(s)); }`
);

// Replace getWallets
content = content.replace(
  /getWallets\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_wallets'\) \|\| '{}\'\);\s*\}/,
  `getWallets()      { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_wallets')) || '{}'); }`
);

// Replace saveWallets
content = content.replace(
  /saveWallets\(w\)\s*\{\s*localStorage\.setItem\('loyalbrew_wallets', JSON\.stringify\(w\)\);\s*\}/,
  `saveWallets(w)    { localStorage.setItem(_getMerchantStorageKey('loyalbrew_wallets'), JSON.stringify(w)); }`
);

// Replace getWalletTxns
content = content.replace(
  /getWalletTxns\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_wallet_txns'\) \|\| '\[\]'\);\s*\}/,
  `getWalletTxns()   { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_wallet_txns')) || '[]'); }`
);

// Replace saveWalletTxns
content = content.replace(
  /saveWalletTxns\(t\)\s*\{\s*localStorage\.setItem\('loyalbrew_wallet_txns', JSON\.stringify\(t\)\);\s*\}/,
  `saveWalletTxns(t) { localStorage.setItem(_getMerchantStorageKey('loyalbrew_wallet_txns'), JSON.stringify(t)); }`
);

// Replace getComplaints
content = content.replace(
  /getComplaints\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_complaints'\) \|\| '\[\]'\);\s*\}/,
  `getComplaints()   { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_complaints')) || '[]'); }`
);

// Replace saveComplaints
content = content.replace(
  /saveComplaints\(c\)\s*\{\s*localStorage\.setItem\('loyalbrew_complaints', JSON\.stringify\(c\)\);\s*\}/,
  `saveComplaints(c) { localStorage.setItem(_getMerchantStorageKey('loyalbrew_complaints'), JSON.stringify(c)); }`
);

// Replace getTopupRequests
content = content.replace(
  /getTopupRequests\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_topup_requests'\) \|\| '\[\]'\);\s*\}/,
  `getTopupRequests() { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_topup_requests')) || '[]'); }`
);

// Replace saveTopupRequests
content = content.replace(
  /saveTopupRequests\(r\)\s*\{\s*localStorage\.setItem\('loyalbrew_topup_requests', JSON\.stringify\(r\)\);\s*\}/,
  `saveTopupRequests(r) { localStorage.setItem(_getMerchantStorageKey('loyalbrew_topup_requests'), JSON.stringify(r)); }`
);

// Replace getCommissions
content = content.replace(
  /getCommissions\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_commissions'\) \|\| '\[\]'\);\s*\}/,
  `getCommissions()  { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_commissions')) || '[]'); }`
);

// Replace saveCommissions
content = content.replace(
  /saveCommissions\(c\)\s*\{\s*localStorage\.setItem\('loyalbrew_commissions', JSON\.stringify\(c\)\);\s*\}/,
  `saveCommissions(c) { localStorage.setItem(_getMerchantStorageKey('loyalbrew_commissions'), JSON.stringify(c)); }`
);

// Replace getPaymentProofs
content = content.replace(
  /getPaymentProofs\(\)\s*\{\s*return JSON\.parse\(localStorage\.getItem\('loyalbrew_payment_proofs'\) \|\| '\[\]'\);\s*\}/,
  `getPaymentProofs() { return JSON.parse(localStorage.getItem(_getMerchantStorageKey('loyalbrew_payment_proofs')) || '[]'); }`
);

// Replace savePaymentProofs
content = content.replace(
  /savePaymentProofs\(p\)\s*\{\s*localStorage\.setItem\('loyalbrew_payment_proofs', JSON\.stringify\(p\)\);\s*\}/,
  `savePaymentProofs(p) { localStorage.setItem(_getMerchantStorageKey('loyalbrew_payment_proofs'), JSON.stringify(p)); }`
);

fs.writeFileSync(filePath, content, 'utf8');
console.log('✅ Phase 1 Remaining: Merchant data isolation applied');
