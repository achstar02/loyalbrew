// Fix index.html - category dropdown options and other hardcoded English
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html';
let content = fs.readFileSync(file, 'utf8');
let changes = 0;

function fix(old, newText) {
    if (content.includes(old)) {
        content = content.replace(old, newText);
        changes++;
        console.log(`  FIXED: ${old}`);
    } else {
        console.log(`  SKIP: ${old}`);
    }
}

console.log('=== FIX: Category dropdown options ===');
// Replace hardcoded category options with data-mi18n-opt attributes
fix('<option>Hot Drinks</option>', '<option data-mi18n-opt="mCatHotDrinks">Hot Drinks</option>');
fix('<option>Cold Drinks</option>', '<option data-mi18n-opt="mCatColdDrinks">Cold Drinks</option>');
fix('<option>Food</option>', '<option data-mi18n-opt="mCatFood">Food</option>');
fix('<option>Desserts</option>', '<option data-mi18n-opt="mCatDesserts">Desserts</option>');
fix('<option>Snacks</option>', '<option data-mi18n-opt="mCatSnacks">Snacks</option>');

fs.writeFileSync(file, content, 'utf8');
console.log(`\nDone! ${changes} fixes applied.`);
