// Fix remaining issues in app.js
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let content = fs.readFileSync(file, 'utf8');
let changes = 0;

function fix(old, newText) {
    if (content.includes(old)) {
        content = content.replace(old, newText);
        changes++;
        console.log(`  FIXED: ${old.substring(0, 80)}`);
    } else {
        console.log(`  SKIP: not found`);
    }
}

console.log('=== FIX: Choose an item default option ===');
// The actual line uses backticks
fix("`<option value=\"\">-- Choose an item --</option>`", "`<option value=''>` + mt('mChooseAnItem') + `</option>`");

console.log('\n=== FIX: No stamp cards available ===');
fix("No stamp cards available</p>", "No stamp cards available</p>"); // check first
// Use string literal for template literal replacement
content = content.replace(
    /No stamp cards available<\/p>/g,
    "` + mt('mNoStampCardsYet') + `</p>"
);
console.log('  Applied regex fix for No stamp cards available</p>');

content = content.replace(
    /No stamp cards available<\/small>/g,
    "` + mt('mNoStampCardsYet') + `</small>`"
);
console.log('  Applied regex fix for No stamp cards available</small>');

fs.writeFileSync(file, content, 'utf8');
console.log(`\nDone! Total changes this run: variable`);
