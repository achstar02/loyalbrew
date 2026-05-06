const fs = require('fs');

const s = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

// Missing translations to add
const missingTranslations = {
  en: {
    bankTitle: 'Bank Transfer Details',
    loyalbrew_brand: 'LoyalBrew — Loyalty & Order System',
    merchant_name_default: 'LoyalBrew Cafe Sdn Bhd',
    demo_label: 'Demo:',
    email_optional: 'Email (optional)',
    referral_code_label: 'Referral Code (referrer\'s phone, optional)',
    admin_label: 'admin',
    new_items: 'New Items',
    bill_amount: 'Bill Amount (RM)',
    all: 'All',
    pending: 'Pending',
    preparing: 'Preparing',
    done: 'Done',
    price_label: 'Price (RM)',
    hot_drinks: 'Hot Drinks',
    cold_drinks: 'Cold Drinks',
    food: 'Food',
    desserts: 'Desserts',
    snacks: 'Snacks',
    card_emoji_icon: 'Card Emoji/Icon',
    flat_discount: 'Flat Discount (RM)',
    min_amount: 'Minimum Amount (RM)',
    qr_description: 'Each table has a unique QR code. Customers can scan and order directly.',
    congratulations: 'Congratulations!',
    stamps_collected: 'You have collected all stamps!',
    whats_new_title: 'What\'s New at LoyalBrew!',
    invite_friends_title: 'Invite Friends, Earn Commissions!',
    no_commissions_yet: 'No commissions yet. Start referring!',
    upload_photo_optional: 'Upload Photo (optional)',
    order_id_optional: 'Order ID (optional)',
    response_action_taken: 'Response / Action Taken',
    walletBalance: 'Balance',
  },
  zh: {
    loyalbrew_brand: 'LoyalBrew — 忠诚会员 & 点餐系统',
    merchant_name_default: 'LoyalBrew Cafe Sdn Bhd',
    demo_label: '演示:',
    email_optional: '邮箱（可选）',
    referral_code_label: '推荐码（推荐人电话，可选）',
    admin_label: '管理员',
    new_items: '新品',
    bill_amount: '账单金额 (RM)',
    all: '全部',
    pending: '待处理',
    preparing: '准备中',
    done: '已完成',
    price_label: '价格 (RM)',
    hot_drinks: '热饮',
    cold_drinks: '冷饮',
    food: '食物',
    desserts: '甜点',
    snacks: '小食',
    card_emoji_icon: '卡片表情/图标',
    flat_discount: '固定折扣 (RM)',
    min_amount: '最低金额 (RM)',
    qr_description: '每张桌子都有独特的二维码。顾客可以扫描并直接点餐。',
    congratulations: '恭喜！',
    stamps_collected: '您已收集所有印章！',
    whats_new_title: 'LoyalBrew 新品上市！',
    invite_friends_title: '邀请朋友，赚取佣金！',
    no_commissions_yet: '还没有佣金。开始推荐吧！',
    upload_photo_optional: '上传照片（可选）',
    order_id_optional: '订单编号（可选）',
    response_action_taken: '回复 / 已采取的行动',
    walletBalance: '余额',
  },
  ms: {
    bankTitle: 'Maklumat Pemindahan Bank',
    loyalbrew_brand: 'LoyalBrew — Sistem Kesetiaan & Pesanan',
    merchant_name_default: 'LoyalBrew Cafe Sdn Bhd',
    demo_label: 'Demo:',
    email_optional: 'E-mel (opsyenal)',
    referral_code_label: 'Kod Rujukan (telefon perujuk, opsyenal)',
    admin_label: 'admin',
    new_items: 'Item Baru',
    bill_amount: 'Jumlah Bil (RM)',
    all: 'Semua',
    pending: 'Menunggu',
    preparing: 'Menyediakan',
    done: 'Selesai',
    price_label: 'Harga (RM)',
    hot_drinks: 'Minuman Panas',
    cold_drinks: 'Minuman Sejuk',
    food: 'Makanan',
    desserts: 'Pencuci Mulut',
    snacks: 'Snek',
    card_emoji_icon: 'Emoji/Ikon Kad',
    flat_discount: 'Diskaun Tetap (RM)',
    min_amount: 'Jumlah Minimum (RM)',
    qr_description: 'Setiap meja mempunyai kod QR unik. Pelanggan boleh imbas dan pesan terus.',
    congratulations: 'Tahniah!',
    stamps_collected: 'Anda telah mengumpul semua setem!',
    whats_new_title: 'Apa yang Baru di LoyalBrew!',
    invite_friends_title: 'Jemput Kawan, Jana Komisen!',
    no_commissions_yet: 'Tiada komisen lagi. Mulakan merujuk!',
    upload_photo_optional: 'Muat Naik Foto (opsyenal)',
    order_id_optional: 'ID Pesanan (opsyenal)',
    response_action_taken: 'Jawapan / Tindakan Diambil',
    walletBalance: 'Baki',
  }
};

// Parse the LANGS object
const lines = s.split('\n');
let result = [];
let inLangs = false;
let inEn = false;
let inZh = false;
let inMs = false;
let braceCount = 0;
let enEndLine = -1;
let zhEndLine = -1;
let msEndLine = -1;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  
  // Track LANGS object
  if (line.match(/const LANGS\s*=\s*\{/)) {
    inLangs = true;
  }
  
  if (inLangs) {
    // Track which language section we're in
    if (line.match(/^\s*en:\s*\{/)) {
      inEn = true;
      braceCount = 1;
    } else if (line.match(/^\s*zh:\s*\{/)) {
      inZh = true;
      inEn = false;
      braceCount = 1;
    } else if (line.match(/^\s*ms:\s*\{/)) {
      inMs = true;
      inZh = false;
      braceCount = 1;
    } else if (line.match(/^\s*ta:\s*\{/)) {
      inMs = false;
      inLangs = false;
    }
    
    // Track braces
    if (inEn || inZh || inMs) {
      for (const c of line) {
        if (c === '{') braceCount++;
        if (c === '}') braceCount--;
      }
      
      // When closing brace found, record the line
      if (braceCount === 0) {
        if (inEn) {
          enEndLine = i;
          inEn = false;
        } else if (inZh) {
          zhEndLine = i;
          inZh = false;
        } else if (inMs) {
          msEndLine = i;
          inMs = false;
        }
      }
    }
  }
}

console.log('en ends at line:', enEndLine + 1);
console.log('zh ends at line:', zhEndLine + 1);
console.log('ms ends at line:', msEndLine + 1);

// Generate the missing translations lines
function generateMissingLines(translations, indent = '    ') {
  return Object.entries(translations).map(([key, value]) => {
    const escaped = value.replace(/'/g, "\\'");
    return `${indent}${key}: '${escaped}',`;
  }).join('\n');
}

// Insert missing translations
const enMissing = generateMissingLines(missingTranslations.en);
const zhMissing = generateMissingLines(missingTranslations.zh);
const msMissing = generateMissingLines(missingTranslations.ms);

// Build the new file content
const outputLines = [...lines];

// Insert at the end of each language section (before the closing brace)
// We need to do this in reverse order to maintain correct line numbers
const insertions = [
  { line: msEndLine, content: '\n' + msMissing },
  { line: zhEndLine, content: '\n' + zhMissing },
  { line: enEndLine, content: '\n' + enMissing }
];

// Sort by line number descending
insertions.sort((a, b) => b.line - a.line);

for (const ins of insertions) {
  outputLines.splice(ins.line, 0, ins.content);
}

fs.writeFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app_fixed.js', outputLines.join('\n'));
console.log('Fixed file saved to app_fixed.js');
