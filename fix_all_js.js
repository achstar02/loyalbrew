// Comprehensive fix for ALL merchant translation issues in app.js
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let content = fs.readFileSync(file, 'utf8');
let changes = 0;

function fix(old, newText) {
    if (content.includes(old)) {
        content = content.replace(old, newText);
        changes++;
        console.log(`  FIXED: ${old.substring(0, 60)}...`);
    } else {
        console.log(`  SKIP: not found - ${old.substring(0, 60)}`);
    }
}

console.log('=== FIX 1: Stamp card reward type labels ===');
fix("label.textContent = 'Free Menu Item';", "label.textContent = mt('mRewardFreeItem');");
fix("label.textContent = 'Discount Amount (RM)';", "label.textContent = mt('mRewardFlatDiscount');");
fix("label.textContent = 'Discount Percentage (%)';", "label.textContent = mt('mRewardPctDiscount');");
fix("label.textContent = 'Bonus Points Amount';", "label.textContent = mt('mRewardBonusPoints');");

console.log('\n=== FIX 2: New Item select default option ===');
fix("'-- Choose an item --'", "' + mt('mChooseAnItem') + '");

console.log('\n=== FIX 3: Hardcoded English toast messages ===');
fix("showToast(emoji + ' ' + name + ' added!');", "show(mt('mItemAdded') || (emoji + ' ' + name), 'success');");
fix("showToast('Item removed');", "showToast(mt('mItemRemoved') || 'Item removed', 'info');");

console.log('\n=== FIX 4: No stamp cards available hardcoded text ===');
fix("No stamp cards available</p>", `${mt('mNoStampCardsYet')}</p>`);
fix("No stamp cards available</small>", `${mt('mNoStampCardsYet')}</small>`);

fs.writeFileSync(file, content, 'utf8');
console.log(`\nTotal fixes applied: ${changes}`);
console.log('Done!');
