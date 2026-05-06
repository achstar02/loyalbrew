// Add category translation keys to MERCHANT_LANGS
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let content = fs.readFileSync(file, 'utf8');

// Add after mItemPhotoOpt in each language section
const fixes = [
    {
        old: "mItemPhotoOpt: '(optional)', mClickToUpload:",
        new: "mItemPhotoOpt: '(optional)', mCatHotDrinks: 'Hot Drinks', mCatColdDrinks: 'Cold Drinks', mCatFood: 'Food', mCatDesserts: 'Desserts', mCatSnacks: 'Snacks', mClickToUpload:"
    },
    {
        old: "mItemPhotoOpt: '\uff08\u53ef\u9009\uff09', mClickToUpload:",
        new: "mItemPhotoOpt: '\uff08\u53ef\u9009\uff09', mCatHotDrinks: '\u70ed\u996e', mCatColdDrinks: '\u51b7\u996e', mCatFood: '\u98df\u7269', mCatDesserts: '\u751c\u54c1', mCatSnacks: '\u5c0f\u5403', mClickToUpload:"
    },
    {
        old: "mItemPhotoOpt: '(pilihan)', mClickToUpload:",
        new: "mItemPhotoOpt: '(pilihan)', mCatHotDrinks: 'Minuman Panas', mCatColdDrinks: 'Minuman Sejuk', mCatFood: 'Makanan', mCatDesserts: 'Pencuci Mulut', mCatSnacks: 'Snek', mClickToUpload:"
    },
    {
        old: "mItemPhotoOpt: '\u0b89\u0bb0\u0bc1\u0baa\u0bcd\u0baa\u0bc1\u0b9f\u0ba4\u0bcd\u0ba4\u0bc1\u0b95\u0bcd\u0b95\u0bc2', mClickToUpload:",
        new: "mItemPhotoOpt: '\u0b89\u0bb0\u0bc1\u0baa\u0bcd\u0baa\u0bc1\u0b9f\u0ba4\u0bcd\u0ba4\u0bc1\u0b95\u0bcd\u0b95\u0bc2', mCatHotDrinks: '\u0b9a\u0bc2\u0b9f\u0bbe\u0ba9 \u0baa\u0bbe\u0ba9\u0b99\u0bcd\u0b95\u0bb3\u0bcd', mCatColdDrinks: '\u0b95\u0bc1\u0bb3\u0bbf\u0bb0\u0bcd \u0baa\u0bbe\u0ba9\u0b99\u0bcd\u0b95\u0bb3\u0bcd', mCatFood: '\u0b89\u0ba3\u0bb5\u0bc1', mCatDesserts: '\u0baa\u0bc2\u0b9a\u0bcd\u0b9a\u0bbf \u0bae\u0bc1\u0bb2\u0bcd', mCatSnacks: '\u0b9a\u0bc1\u0bb5\u0bbe\u0ba4\u0bcd\u0ba4\u0bc8', mClickToUpload:"
    }
];

let count = 0;
for (const f of fixes) {
    if (content.includes(f.old)) {
        content = content.replace(f.old, f.new);
        count++;
        console.log(`  OK`);
    } else {
        console.log(`  SKIP: ${f.old.substring(0, 50)}`);
    }
}

fs.writeFileSync(file, content, 'utf8');
console.log(`\nDone! ${count}/4 languages updated.`);
