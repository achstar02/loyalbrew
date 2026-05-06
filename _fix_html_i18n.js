const fs = require('fs');

// 1. Read index.html
const htmlPath = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html';
let html = fs.readFileSync(htmlPath, 'utf8');

// 2. Define i18n keys for each hardcoded Chinese string
// Format: [regex to match the line, data-i18n key, en text, zh text, ms text, ta text]
const replacements = [
  // L70: 欢迎回来
  { re: /<div class="text-sm text-white\/70">欢迎回来<\/div>/,
    key: 'welcomeBack', zh: '欢迎回来', en: 'Welcome Back', ms: 'Selamat Kembali', ta: 'மீண்டும் வரவேற்கிறோம்' },
  // L71: 今天想喝点什么？
  { re: /<div class="mt-1 text-2xl font-bold tracking-tight">今天想喝点什么？<\/div>/,
    key: 'drinkToday', zh: '今天想喝点什么？', en: "What's your drink today?", ms: 'Minum apa hari ini?', ta: 'இன்று என்ன குடிக்கிறீர்கள்?' },
  // L72: 主按钮会在后续接 Firebase...
  { re: /<div class="mt-3 text-xs text-white\/60">主按钮会在后续接 Firebase：检查商家 credits，成功操作后自动扣 1。<\/div>/,
    key: 'firebaseNote', zh: '主按钮会在后续接 Firebase：检查商家 credits，成功操作后自动扣 1。', en: 'Main button will connect to Firebase: check merchant credits, auto-deduct 1 on success.', ms: 'Butang utama akan sambung ke Firebase: semak kredit peniaga, potong 1 secara auto.', ta: 'முக்கிய பொத்தான் Firebase-ஐ இணைக்கும்: வர்த்தகர் கடன்களைச் சரிபார்க்கவும், வெற்றிக்குப் பின் 1ஐ தானாகக் கழிக்கும்.' },
  // L123: 进入
  { re: /<span class="text-xs font-semibold text-white\/70">进入<\/span>/,
    key: 'enter', zh: '进入', en: 'Enter', ms: 'Masuk', ta: 'நுழை' },
  // L136: 获取
  { re: /<span class="text-xs font-semibold text-white\/70">获取<\/span>/,
    key: 'get', zh: '获取', en: 'Get', ms: 'Dapat', ta: 'பெறு' },
  // L149: 查看
  { re: /<span class="text-xs font-semibold text-white\/70">查看<\/span>/,
    key: 'view', zh: '查看', en: 'View', ms: 'Lihat', ta: 'பார்' },
  // L568: 返回
  { re: /<button class="back-btn" onclick="showPage\('page-landing'\)"><i class="fas fa-arrow-left"><\/i> 返回<\/button>/,
    key: 'back', zh: '返回', en: 'Back', ms: 'Kembali', ta: 'திரும்ப' },
  // L671: 快捷操作 / Quick Actions
  { re: /<h3[^>]*><i class="fas fa-bolt"[^>]*><\/i> 快捷操作 \/ Quick Actions<\/h3>/,
    key: 'quickActions', zh: '快捷操作 / Quick Actions', en: 'Quick Actions', ms: 'Tindakan Pantas', ta: 'விரைவு செயல்கள்' },
  // L675: 查看订单
  { re: /<span style="font-size:0\.8rem">查看订单<\/span>/,
    key: 'viewOrders', zh: '查看订单', en: 'View Orders', ms: 'Lihat Pesanan', ta: 'ஆர்டர்களைப் பார்' },
  // L679: 菜单管理
  { re: /<span style="font-size:0\.8rem">菜单管理<\/span>/,
    key: 'menuMgmt', zh: '菜单管理', en: 'Menu Management', ms: 'Urusan Menu', ta: 'பட்டியல் மேலாண்மை' },
  // L683: 店铺设置
  { re: /<span style="font-size:0\.8rem">店铺设置<\/span>/,
    key: 'shopSettings', zh: '店铺设置', en: 'Shop Settings', ms: 'Tetapan Kedai', ta: 'கடை அமைப்புகள்' },
  // L687: 厨房显示
  { re: /<span style="font-size:0\.8rem">厨房显示<\/span>/,
    key: 'kitchenDisplay', zh: '厨房显示', en: 'Kitchen Display', ms: 'Paparan Dapur', ta: 'சமையலறை காட்சி' },
  // L711: 确认加分
  { re: /<span>确认加分<\/span>/,
    key: 'confirmAddPoints', zh: '确认加分', en: 'Confirm Points', ms: 'Sahkan Mata', ta: 'புள்ளிகளை உறுதிப்படுத்து' },
  // L712: 充值（对接支付网关）
  { re: /<i class="fas fa-wallet"><\/i> 充值（对接支付网关）<\/button>/,
    key: 'topUpGateway', zh: '充值（对接支付网关）', en: 'Top Up (Payment Gateway)', ms: 'Top Up (Gateway Pembayaran)', ta: 'மீண்டும் நிரப்பு (கட்டண வாயில்)' },
  // L1092: Shop Info / 店铺信息
  { re: /<h3><i class="fas fa-store"><\/i> Shop Info \/ 店铺信息<\/h3>/,
    key: 'shopInfo', zh: '店铺信息', en: 'Shop Info', ms: 'Info Kedai', ta: 'கடை தகவல்' },
  // L1094: Shop Name / 店名
  { re: /<label><i class="fas fa-tag"><\/i> Shop Name \/ 店名<\/label>/,
    key: 'shopName', zh: '店名', en: 'Shop Name', ms: 'Nama Kedai', ta: 'கடை பெயர்' },
  // L1098: Announcement / 公告
  { re: /<label><i class="fas fa-bullhorn"><\/i> Announcement \/ 公告<\/label>/,
    key: 'announcement', zh: '公告', en: 'Announcement', ms: 'Pengumuman', ta: 'அறிவிப்பு' },
  // L1102: Banner Image URL / 横幅图片
  { re: /<label><i class="fas fa-image"><\/i> Banner Image URL \/ 横幅图片<\/label>/,
    key: 'bannerUrl', zh: '横幅图片', en: 'Banner Image URL', ms: 'URL Imej Sepanduk', ta: 'பேனர் பட URL' },
  // L1106: Save Shop Info / 保存
  { re: /<button class="btn-merchant" onclick="saveShopSettings\(\)"><i class="fas fa-save"><\/i> Save Shop Info \/ 保存<\/button>/,
    key: 'saveShopInfo', zh: '保存', en: 'Save Shop Info', ms: 'Simpan Info Kedai', ta: 'கடைத் தகவலைச் சேமி' },
  // L1111: Points Settings / 积分设置
  { re: /<h3><i class="fas fa-star"><\/i> Points Settings \/ 积分设置<\/h3>/,
    key: 'pointsSettings', zh: '积分设置', en: 'Points Settings', ms: 'Tetapan Mata', ta: 'புள்ளி அமைப்புகள்' },
  // L1113: Points per RM / 每RM积分
  { re: /<label><i class="fas fa-calculator"><\/i> Points per RM \/ 每RM积分<\/label>/,
    key: 'pointsPerRM', zh: '每RM积分', en: 'Points per RM', ms: 'Mata per RM', ta: 'RM ஒவ்வொன்றுக்கும் புள்ளிகள்' },
  // L1117: Save Points Settings / 保存
  { re: /<button class="btn-merchant" onclick="savePointsSettings\(\)"><i class="fas fa-save"><\/i> Save Points Settings \/ 保存<\/button>/,
    key: 'savePoints', zh: '保存', en: 'Save Points Settings', ms: 'Simpan Tetapan Mata', ta: 'புள்ளி அமைப்புகளைச் சேமி' },
];

let count = 0;
for (const r of replacements) {
  const m = html.match(r.re);
  if (m) {
    // Replace Chinese text with data-i18n attribute
    const orig = m[0];
    let replacement = orig;
    
    // Check if element already has data-i18n
    if (!orig.includes('data-i18n=')) {
      // Insert data-i18n before the closing > of the opening tag
      // Strategy: find the first > that's not inside quotes
      let inQuote = null;
      let insertPos = -1;
      for (let i = 0; i < orig.length; i++) {
        const c = orig[i];
        if (inQuote) {
          if (c === inQuote && orig[i-1] !== '\\') { inQuote = null; }
        } else {
          if (c === '"' || c === "'") { inQuote = c; }
          else if (c === '>') { insertPos = i; break; }
        }
      }
      if (insertPos >= 0) {
        replacement = orig.slice(0, insertPos) + ` data-i18n="${r.key}"` + orig.slice(insertPos);
        html = html.replace(orig, replacement);
        count++;
      }
    }
  } else {
    console.log('NOT MATCHED:', r.key);
  }
}

fs.writeFileSync(htmlPath, html, 'utf8');
console.log('HTML updated:', count, 'elements with data-i18n');

// 3. Now update app.js to add these keys to all 4 language objects
const jsPath = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let js = fs.readFileSync(jsPath, 'utf8');

// For each key, add to en/zh/ms/ta objects
for (const r of replacements) {
  // Add to zh (Chinese) - the original text
  const zhRegex = new RegExp(`(zh:\\s*\\{[^}]*?)(\\s*\\})`, 's');
  // We need to insert new keys before the closing } of zh object
  // Find the zh: { ... } block
}

// Actually, let me find the language objects more carefully
// They're structured as: en: { ... }, zh: { ... }, ms: { ... }, ta: { ... }
// Let me find where zh: { starts and ends

console.log('Need to add translation keys to app.js manually');
console.log('Keys to add:');
for (const r of replacements) {
  console.log(`  ${r.key}: en="${r.en}", zh="${r.zh}", ms="${r.ms}", ta="${r.ta}"`);
}
