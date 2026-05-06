// _patch_softdelete.js - 将硬删除改为14天软删除
const fs = require('fs');
const path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(path, 'utf8');
const orig = c;

// 1. 修改弹窗警告文字（14天软删除说明）
c = c.replace(
  '此操作将删除该商家的所有数据，无法恢复！',
  '商家将进入 14 天待删除状态，14 天后可永久解除。在此期间可在「已解除」列表恢复。'
);

// 2. 修改按钮文字
c = c.replace(
  '确认解除</button>',
  '确认解除（14天）</button>'
);

// 3. 把 deleteDoc 改为 updateDoc（软删除）
c = c.replace(
  "await fb.deleteDoc(ref);\n      showToast(\"商家 [\" + merchantName + \"] 已解除\", \"success\");",
  `await fb.updateDoc(fb.doc(fb.db, "merchants", merchantId), {
        status: "deleted",
        deletedAt: new Date().toISOString()
      });
      showToast("商家 [\" + merchantName + \"] 已移至待删除（14天后）\", "success");`
);

// 4. 在 renderSuperAdminMerchantsList 中过滤已删除商家
// 找到 async function renderSuperAdminMerchantsList() { 后的 forEach/if/filter
c = c.replace(
  /(async function renderSuperAdminMerchantsList\(\) \{[\s\S]{0,300}?\bconst\s+docs\s*=\s*snapshot\.docs\b)/,
  "$1\r\n    const all = snapshot.docs.filter(d => d.data().status !== 'deleted');"
);

// 5. 在 _loadSuperAdminMerchants 中过滤已删除商家
c = c.replace(
  /(async function _loadSuperAdminMerchants\(\) \{[\s\S]{0,300}?\bconst\s+docs\s*=\s*snapshot\.docs\b)/,
  "$1\r\n    const all = snapshot.docs.filter(d => d.data().status !== 'deleted');"
);

// 6. 把 docs.map 改为 all.map（在两个函数中）
c = c.replace(/(renderSuperAdminMerchantsList[\s\S]{0,2000}?)docs\.map\((m)/g, '$1all.map($2');
c = c.replace(/(_loadSuperAdminMerchants[\s\S]{0,2000}?)docs\.map\((m)/g, '$1all.map($2');

if (c !== orig) {
  fs.writeFileSync(path, c, 'utf8');
  console.log('=== SOFT DELETE PATCH APPLIED ===');
  console.log('1. Modal warning text updated (14 days)');
  console.log('2. Button text updated');
  console.log('3. deleteDoc → updateDoc (status=deleted)');
  console.log('4. renderSuperAdminMerchantsList: filter status!==deleted');
  console.log('5. _loadSuperAdminMerchants: filter status!==deleted');
} else {
  console.log('No changes made - pattern not found');
}
