// 验证所有 Phase 2 修改
const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

const checks = [
  ['(必填)', '联系电话标签改为必填'],
  ['请填写有效的联系电话', 'phone必填验证逻辑'],
  ['请填写商家名称、商家ID、密码和联系电话', '错误提示包含电话'],
  ['event.currentTarget.classList.add', 'switchMerchantTab event guard (应含条件判断)'],
  ['_psRate', 'updateCartSummary pointsRate'],
  ['_apRate', 'addPoints pointsRate'],
];

let allOk = true;
for (const [str, desc] of checks) {
  const ok = c.includes(str);
  console.log(ok ? '✅' : '❌', desc, ok ? '' : `← 缺少: ${str}`);
  if (!ok) allOk = false;
}

// 额外检查 switchMerchantTab guard
const guardIdx = c.indexOf('event.currentTarget.classList.add');
if (guardIdx >= 0) {
  const guardCtx = c.substring(guardIdx - 20, guardIdx + 50);
  const hasGuard = guardCtx.includes('if (event && event.currentTarget)');
  console.log(hasGuard ? '✅' : '❌', 'switchMerchantTab event guard 有 if 条件');
  if (!hasOk2) allOk = false;
}

console.log(allOk ? '\n🎉 ALL CHECKS PASSED!' : '\n⚠️ Some checks failed');
