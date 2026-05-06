const fs = require('fs');

// ============================================================
// Fix 1: Update index.html - add data-i18n attributes
// ============================================================
const htmlPath = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html';
let html = fs.readFileSync(htmlPath, 'utf8');

// Define updates: [search regex, i18n key, zh text, en text, ms text, ta text]
// We need to ensure the regex and replacements handle special chars properly
const updates = [
  { key: 'welcomeBack', zh: '欢迎回来', en: 'Welcome Back', ms: 'Selamat Kembali', ta: 'மீண்டும் வரவேற்கிறோம்',
    search: '>欢迎回来<' },
  { key: 'drinkToday', zh: '今天想喝点什么？', en: "What's your drink today?", ms: 'Minum apa hari ini?', ta: 'இன்று என்ன குடிக்கிறீர்கள்?',
    search: '>今天想喝点什么？<' },
  { key: 'firebaseNote', zh: '主按钮会在后续接 Firebase：检查商家 credits，成功操作后自动扣 1。', en: 'Main button will connect to Firebase: check merchant credits, auto-deduct 1 on success.', ms: 'Butang utama akan sambung ke Firebase: semak kredit peniaga, potong 1 secara auto.', ta: 'முக்கிய பொத்தான் Firebase-ஐ இணைக்கும்: வர்த்தகர் கடன்களைச் சரிபார்க்கவும், வெற்றிக்குப் பின் 1ஐ தானாகக் கழிக்கும்.',
    search: '>主按钮会在后续接 Firebase' },
  { key: 'enter', zh: '进入', en: 'Enter', ms: 'Masuk', ta: 'நுழை',
    search: '>进入<' },
  { key: 'getBtn', zh: '获取', en: 'Get', ms: 'Dapat', ta: 'பெறு',
    search: '>获取<' },
  { key: 'view', zh: '查看', en: 'View', ms: 'Lihat', ta: 'பார்',
    search: '>查看</span>' },
  { key: 'back', zh: '返回', en: 'Back', ms: 'Kembali', ta: 'திரும்ப',
    search: '> 返回</button>' },
  { key: 'superAdmin', zh: '超级管理', en: 'Super Admin', ms: 'Super Admin', ta: 'சூப்பர் நிர்வாகி',
    search: '>超级管理</span>' },
  { key: 'quickActions', zh: '快捷操作 / Quick Actions', en: 'Quick Actions', ms: 'Tindakan Pantas', ta: 'விரைவு செயல்கள்',
    search: '> 快捷操作 / Quick Actions<' },
  { key: 'viewOrders2', zh: '查看订单', en: 'View Orders', ms: 'Lihat Pesanan', ta: 'ஆர்டர்களைப் பார்',
    search: '>查看订单<' },
  { key: 'menuMgmt2', zh: '菜单管理', en: 'Menu Management', ms: 'Urusan Menu', ta: 'பட்டியல் மேலாண்மை',
    search: '>菜单管理<' },
  { key: 'shopSettings2', zh: '店铺设置', en: 'Shop Settings', ms: 'Tetapan Kedai', ta: 'கடை அமைப்புகள்',
    search: '>店铺设置<' },
  { key: 'kitchenDisplay2', zh: '厨房显示', en: 'Kitchen Display', ms: 'Paparan Dapur', ta: 'சமையலறை காட்சி',
    search: '>厨房显示<' },
  { key: 'confirmPoints', zh: '确认加分', en: 'Confirm Points', ms: 'Sahkan Mata', ta: 'புள்ளிகளை உறுதிப்படுத்து',
    search: '>确认加分<' },
  { key: 'topUpGateway', zh: '充值（对接支付网关）', en: 'Top Up (Payment Gateway)', ms: 'Top Up (Gateway Pembayaran)', ta: 'மீண்டும் நிரப்பு (கட்டண வாயில்)',
    search: '> 充值（对接支付网关）' },
  { key: 'shopInfo', zh: '店铺信息', en: 'Shop Info', ms: 'Info Kedai', ta: 'கடை தகவல்',
    search: '> Shop Info / 店铺信息<' },
  { key: 'shopName', zh: '店名', en: 'Shop Name', ms: 'Nama Kedai', ta: 'கடை பெயர்',
    search: '> Shop Name / 店名<' },
  { key: 'announcement', zh: '公告', en: 'Announcement', ms: 'Pengumuman', ta: 'அறிவிப்பு',
    search: '> Announcement / 公告<' },
  { key: 'bannerUrl', zh: '横幅图片', en: 'Banner Image URL', ms: 'URL Imej Sepanduk', ta: 'பேனர் பட URL',
    search: '> Banner Image URL / 横幅图片<' },
  { key: 'saveShop', zh: '保存', en: 'Save Shop Info', ms: 'Simpan Info Kedai', ta: 'கடைத் தகவலைச் சேமி',
    search: '> Save Shop Info / 保存<' },
  { key: 'pointsSettings', zh: '积分设置', en: 'Points Settings', ms: 'Tetapan Mata', ta: 'புள்ளிகள் அமைப்புகள்',
    search: '> Points Settings / 积分设置<' },
  { key: 'pointsPerRM', zh: '每RM积分', en: 'Points per RM', ms: 'Mata per RM', ta: 'RM ஒவ்வொன்றுக்கும் புள்ளிகள்',
    search: '> Points per RM / 每RM积分<' },
  { key: 'savePoints2', zh: '保存', en: 'Save Points Settings', ms: 'Simpan Tetapan Mata', ta: 'புள்ளிகள் அமைப்புகளைச் சேமி',
    search: '> Save Points Settings / 保存<' },
];

let htmlCount = 0;
for (const u of updates) {
  const idx = html.indexOf(u.search);
  if (idx >= 0) {
    // Find the opening tag before this position
    let tagStart = html.lastIndexOf('<', idx);
    // Find the closing > of the opening tag
    let tagEnd = html.indexOf('>', tagStart);
    if (tagEnd > idx) {
      console.log('ERROR: tagEnd > idx for', u.key);
      continue;
    }
    // Insert data-i18n before the closing >
    const before = html.slice(0, tagEnd);
    const after = html.slice(tagEnd);
    const newTag = before + ` data-i18n="${u.key}"` + after;
    html = newTag;
    htmlCount++;
  } else {
    console.log('NOT FOUND:', u.key, u.search.slice(0, 30));
  }
}

fs.writeFileSync(htmlPath, html, 'utf8');
console.log('HTML updated:', htmlCount, 'elements with data-i18n');

// ============================================================
// Fix 2: Update app.js - add keys to language objects
// ============================================================
const jsPath = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let js = fs.readFileSync(jsPath, 'utf8');

// For each language, find the object and add keys before the closing }
for (const lang of ['en', 'zh', 'ms', 'ta']) {
  // Find the lang: { ... } block
  const langRegex = new RegExp(`(^\\s*${lang}:\\s*\\{)`, 'm');
  const match = js.match(langRegex);
  if (!match) {
    console.log(`Could not find ${lang}: object`);
    continue;
  }
  
  // Find the matching closing brace
  const startIdx = js.indexOf(match[1]);
  let braceCount = 0;
  let inString = false;
  let stringChar = '';
  let i = startIdx;
  
  // Skip to the first {
  while (i < js.length && js[i] !== '{') i++;
  braceCount = 1;
  i++;
  
  while (i < js.length && braceCount > 0) {
    const c = js[i];
    if (inString) {
      if (c === stringChar && js[i-1] !== '\\') {
        inString = false;
      }
    } else {
      if (c === '"' || c === "'") {
        inString = true;
        stringChar = c;
      } else if (c === '{') {
        braceCount++;
      } else if (c === '}') {
        braceCount--;
      }
    }
    i++;
  }
  
  // i is now just after the closing }
  const objEnd = i - 1;
  
  // Build new keys string, properly escaping quotes in values
  let newKeys = '';
  for (const u of updates) {
    const text = u[lang];
    // Escape single quotes in the text for JS string
    const escaped = text.replace(/'/g, "\\'");
    newKeys += `\n    ${u.key}: '${escaped}',`;
  }
  
  // Insert before the closing }
  js = js.slice(0, objEnd) + newKeys + js.slice(objEnd);
}

fs.writeFileSync(jsPath, js, 'utf8');
console.log('JS updated with', updates.length * 4, 'translation keys');

// Verify syntax
try {
  new Function(js);
  console.log('JS syntax: OK');
} catch(e) {
  console.log('JS syntax ERROR:', e.message);
}
