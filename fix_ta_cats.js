// Add missing TA category keys
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let content = fs.readFileSync(file, 'utf8');

const old = "mItemPhotoOpt: '(\u0bb5\u0bbf\u0bb0\u0bc1\u0bae\u0bcd\u0baa\u0bbf\u0ba9\u0bbe\u0bb2\u0bcd)', mClickToUpload:";
const newText = "mItemPhotoOpt: '(\u0bb5\u0bbf\u0bb0\u0bc1\u0bae\u0bcd\u0baa\u0bbf\u0ba9\u0bbe\u0bb2\u0bcd)', mCatHotDrinks: '\u0b9a\u0bc2\u0b9f\u0bbe\u0ba9 \u0baa\u0bbe\u0ba9\u0b99\u0bcd\u0b95\u0bb3\u0bcd', mCatColdDrinks: '\u0b95\u0bc1\u0bb3\u0bbf\u0bb0\u0bcd \u0baa\u0bbe\u0ba9\u0b99\u0bcd\u0b95\u0bb3\u0bcd', mCatFood: '\u0b89\u0ba3\u0bb5\u0bc1', mCatDesserts: '\u0baa\u0bc2\u0b9a\u0bcd\u0b9a\u0bbf \u0bae\u0bc1\u0bb2\u0bcd', mCatSnacks: '\u0b9a\u0bc1\u0bb5\u0bbe\u0ba4\u0bcd\u0ba4\u0bc8', mClickToUpload:";

if (content.includes(old)) {
    content = content.replace(old, newText);
    console.log('Added TA category keys');
} else {
    console.log('Pattern not found - checking actual text...');
    // Find the actual line
    const lines = content.split('\n');
    for (let i = 4100; i < 4200; i++) {
        if (lines[i] && lines[i].includes('mItemPhotoOpt')) {
            console.log(`Line ${i+1}: ${lines[i].trim().substring(0, 120)}`);
        }
    }
}

fs.writeFileSync(file, content, 'utf8');
console.log('Done!');
