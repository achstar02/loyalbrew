// Comprehensive fix for ALL merchant translation issues in app.js
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let content = fs.readFileSync(file, 'utf8');
let changes = 0;

function fix(old, newText) {
    if (content.includes(old)) {
        content = content.replace(old, newText);
        changes++;
        console.log(`  [OK] Line with: ${old.substring(0, 70)}`);
    } else {
        console.log(`  [SKIP] not found: ${old.substring(0, 70)}`);
    }
}

console.log('=== FIX 1: Stamp card reward type labels (lines 2521-2540) ===');
fix("label.textContent = 'Free Menu Item';", "label.textContent = mt('mRewardFreeItem');");
fix("label.textContent = 'Discount Amount (RM)';", "label.textContent = mt('mRewardFlatDiscount');");
fix("label.textContent = 'Discount Percentage (%)';", "label.textContent = mt('mRewardPctDiscount');");
fix("label.textContent = 'Bonus Points Amount';", "label.textContent = mt('mRewardBonusPoints');");

console.log('\n=== FIX 2: Hardcoded English toast messages ===');
fix("showToast(emoji + ' ' + name + ' added!');", "showToast(mt('mItemAdded') || (emoji + ' ' + name), 'success');");
fix("showToast('Item removed');", "showToast(mt('mItemRemoved') || 'Item removed', 'info');");

console.log('\n=== FIX 3: No stamp cards available hardcoded text ===');
// Use regex for template literals
content = content.replace(
    /No stamp cards available<\/p>/g,
    "` + mt('mNoStampCardsYet') + `</p>"
);
changes++;
console.log('  [OK] No stamp cards available</p> -> mt()');

content = content.replace(
    /No stamp cards available<\/small>/g,
    "` + mt('mNoStampCardsYet') + `</small>`"
);
changes++;
console.log('  [OK] No stamp cards available</small> -> mt()');

fs.writeFileSync(file, content, 'utf8');
console.log(`\nTotal fixes: ${changes}`);
console.log('Done!');
