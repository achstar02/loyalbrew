const fs = require('fs');

// ============================================================
// Step 1: Update index.html - add data-i18n attributes
// ============================================================
const htmlPath = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html';
let html = fs.readFileSync(htmlPath, 'utf8');

// Define replacements: [regex, key, zhFull, enFull, msFull, taFull]
// For elements with pure Chinese text (no / English), add data-i18n and the text will be auto-filled
// For elements with "中文 / English", we need to handle the format
const updates = [
  { re: /(<div class="text-sm text-white\/70">)欢迎回来(<\/div>)/, key: 'welcomeBack', zh: '欢迎回来', en: 'Welcome Back', ms: 'Selamat Kembali', ta: 'மீண்டும் வரவேற்கிறோம்' },
  { re: /(<div class="mt-1 text-2xl font-bold tracking-tight">)今天想喝点什么\？(<\/div>)/, key: 'drinkToday', zh: '今天想喝点什么？', en: "What's your drink today?", ms: 'Minum apa hari ini?', ta: 'இன்று என்ன குடிக்கிறீர்கள்?' },
  { re: /(<div class="mt-3 text-xs text-white\/60">)主按钮会在后续接 Firebase：检查商家 credits，成功操作后自动扣 1。(<\/div>)/, key: 'firebaseNote', zh: '主按钮会在后续接 Firebase：检查商家 credits，成功操作后自动扣 1。', en: 'Main button will connect to Firebase: check merchant credits, auto-deduct 1 on success.', ms: 'Butang utama akan sambung ke Firebase: semak kredit peniaga, potong 1 secara auto.', ta: 'முக்கிய பொத்தான் Firebase-ஐ இணைக்கும்: வர்த்தகர் கடன்களைச் சரிபார்க்கவும், வெற்றிக்குப் பின் 1ஐ தானாகக் கழிக்கும்.' },
  { re: /(<span class="text-xs font-semibold text-white\/70">)进入(<\/span>)/, key: 'enter', zh: '进入', en: 'Enter', ms: 'Masuk', ta: 'நுழை' },
  { re: /(<span class="text-xs font-semibold text-white\/70">)获取(<\/span>)/, key: 'get', zh: '获取', en: 'Get', ms: 'Dapat', ta: 'பெறு' },
  { re: /(<span class="text-xs font-semibold text-white\/70">)查看(<\/span>)/, key: 'view', zh: '查看', en: 'View', ms: 'Lihat', ta: 'பார்' },
  { re: /(<button class="back-btn" onclick="showPage\('page-landing'\)"><i class="fas fa-arrow-left"><\/i> )返回(<\/button>)/, key: 'back', zh: '返回', en: 'Back', ms: 'Kembali', ta: 'திரும்ப' },
  { re: /(<button id="super-admin-nav"[^>]*><i class="fas fa-crown text-\[#2a1a10\] text-sm"><\/i><span class="text-xs font-bold text-\[#2a1a10\]">)超级管理(<\/span>)/, key: 'superAdmin', zh: '超级管理', en: 'Super Admin', ms: 'Super Admin', ta: 'சூப்பர் நிர்வாகி' },
  { re: /(<h3 style="margin:0 0 12px;font-size:0\.95rem"><i class="fas fa-bolt" style="color:#ff9800"><\/i> )快捷操作 \/ Quick Actions(<\/h3>)/, key: 'quickActions', zh: '快捷操作 / Quick Actions', en: 'Quick Actions', ms: 'Tindakan Pantas', ta: 'விரைவு செயல்கள்' },
  { re: /(<span style="font-size:0\.8rem">)查看订单(<\/span>)/, key: 'viewOrders2', zh: '查看订单', en: 'View Orders', ms: 'Lihat Pesanan', ta: 'ஆர்டர்களைப் பார்' },
  { re: /(<span style="font-size:0\.8rem">)菜单管理(<\/span>)/, key: 'menuMgmt2', zh: '菜单管理', en: 'Menu Management', ms: 'Urusan Menu', ta: 'பட்டியல் மேலாண்மை' },
  { re: /(<span style="font-size:0\.8rem">)店铺设置(<\/span>)/, key: 'shopSettings2', zh: '店铺设置', en: 'Shop Settings', ms: 'Tetapan Kedai', ta: 'கடை அமைப்புகள்' },
  { re: /(<span style="font-size:0\.8rem">)厨房显示(<\/span>)/, key: 'kitchenDisplay2', zh: '厨房显示', en: 'Kitchen Display', ms: 'Paparan Dapur', ta: 'சமையலறை காட்சி' },
  { re: /(<button class="btn-merchant full" onclick="addPoints\(\)"><i class="fas fa-check-circle"><\/i> <span>)确认加分(<\/span>)/, key: 'confirmPoints', zh: '确认加分', en: 'Confirm Points', ms: 'Sahkan Mata', ta: 'புள்ளிகளை உறுதிப்படுத்து' },
  { re: /(<button class="btn-sm-white" style="width:100%;justify-content:center;margin-top:8px" onclick="openTopUpPlaceholder\(\)"><i class="fas fa-wallet"><\/i> )充值（对接支付网关）(<\/button>)/, key: 'topUpGateway', zh: '充值（对接支付网关）', en: 'Top Up (Payment Gateway)', ms: 'Top Up (Gateway Pembayaran)', ta: 'மீண்டும் நிரப்பு (கட்டண வாயில்)' },
  { re: /(<h3><i class="fas fa-store"><\/i> Shop Info \/ )店铺信息(<\/h3>)/, key: 'shopInfo', zh: '店铺信息', en: 'Shop Info', ms: 'Info Kedai', ta: 'கடை தகவல்' },
  { re: /(<label><i class="fas fa-tag"><\/i> Shop Name \/ )店名(<\/label>)/, key: 'shopName', zh: '店名', en: 'Shop Name', ms: 'Nama Kedai', ta: 'கடை பெயர்' },
  { re: /(<label><i class="fas fa-bullhorn"><\/i> Announcement \/ )公告(<\/label>)/, key: 'announcement', zh: '公告', en: 'Announcement', ms: 'Pengumuman', ta: 'அறிவிப்பு' },
  { re: /(<label><i class="fas fa-image"><\/i> Banner Image URL \/ )横幅图片(<\/label>)/, key: 'bannerUrl', zh: '横幅图片', en: 'Banner Image URL', ms: 'URL Imej Sepanduk', ta: 'பேனர் பட URL' },
  { re: /(<button class="btn-merchant" onclick="saveShopSettings\(\)"><i class="fas fa-save"><\/i> Save Shop Info \/ )保存(<\/button>)/, key: 'saveShop', zh: '保存', en: 'Save Shop Info', ms: 'Simpan Info Kedai', ta: 'கடைத் தகவலைச் சேமி' },
  { re: /(<h3><i class="fas fa-star"><\/i> Points Settings \/ )积分设置(<\/h3>)/, key: 'pointsSettings', zh: '积分设置', en: 'Points Settings', ms: 'Tetapan Mata', ta: 'புள்ளிகள் அமைப்புகள்' },
  { re: /(<label><i class="fas fa-calculator"><\/i> Points per RM \/ )每RM积分(<\/label>)/, key: 'pointsPerRM', zh: '每RM积分', en: 'Points per RM', ms: 'Mata per RM', ta: 'RM ஒவ்வொன்றுக்கும் புள்ளிகள்' },
  { re: /(<button class="btn-merchant" onclick="savePointsSettings\(\)"><i class="fas fa-save"><\/i> Save Points Settings \/ )保存(<\/button>)/, key: 'savePoints2', zh: '保存', en: 'Save Points Settings', ms: 'Simpan Tetapan Mata', ta: 'புள்ளிகள் அமைப்புகளைச் சேமி' },
];

let htmlCount = 0;
for (const u of updates) {
  const m = html.match(u.re);
  if (m) {
    const replacement = m[1] + `<span data-i18n="${u.key}">${u.zh}</span>` + m[m.length-1];
    html = html.replace(m[0], replacement);
    htmlCount++;
  } else {
    console.log('HTML NOT MATCHED:', u.key);
  }
}

fs.writeFileSync(htmlPath, html, 'utf8');
console.log('HTML updated:', htmlCount, 'elements with data-i18n');

// ============================================================
// Step 2: Update app.js - add keys to all 4 language objects
// ============================================================
const jsPath = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let js = fs.readFileSync(jsPath, 'utf8');

// For each language (en, zh, ms, ta), find the object and add keys
const langs = ['en', 'zh', 'ms', 'ta'];
const langTexts = {};
for (const u of updates) {
  langTexts[u.key] = { zh: u.zh, en: u.en, ms: u.ms, ta: u.ta };
}

// Function to find the language object boundaries
function findLangObject(str, lang) {
  const startPattern = new RegExp(`^\\s*${lang}:\\s*\\{`, 'm');
  const startMatch = str.match(startPattern);
  if (!startMatch) return null;
  
  const startIdx = str.indexOf(startMatch[0]);
  let braceCount = 0;
  let inString = false;
  let stringChar = null;
  let i = startIdx;
  
  // Skip to the first { after the lang:
  while (i < str.length && str[i] !== '{') i++;
  braceCount = 1;
  i++;
  
  while (i < str.length && braceCount > 0) {
    const c = str[i];
    if (inString) {
      if (c === stringChar && str[i-1] !== '\\') { inString = false; }
    } else {
      if (c === '"' || c === "'") { inString = true; stringChar = c; }
      else if (c === '{') braceCount++;
      else if (c === '}') braceCount--;
    }
    i++;
  }
  
  // i is now just after the closing }
  return { start: startIdx, end: i - 1 };
}

let jsCount = 0;
for (const lang of langs) {
  const bounds = findLangObject(js, lang);
  if (!bounds) {
    console.log(`Could not find ${lang}: object`);
    continue;
  }
  
  // Build the new keys string
  let newKeys = '';
  for (const u of updates) {
    const text = langTexts[u.key][lang];
    newKeys += `\n    ${u.key}: '${text}',`;
  }
  
  // Insert before the closing }
  const before = js.slice(0, bounds.end - 1);
  const after = js.slice(bounds.end - 1);
  
  js = before + newKeys + after;
  jsCount += updates.length;
}

fs.writeFileSync(jsPath, js, 'utf8');
console.log('JS updated:', jsCount, 'translation keys added');

// Verify syntax
try {
  new Function(js);
  console.log('JS syntax: OK');
} catch(e) {
  console.log('JS syntax ERROR:', e.message);
}
