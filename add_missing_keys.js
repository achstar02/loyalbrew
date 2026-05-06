// Add missing translation keys to MERCHANT_LANGS in app.js
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let content = fs.readFileSync(file, 'utf8');

// We need to add mChooseAnItem, mItemAdded, mItemRemoved to all 4 language sections
// Find each section by looking for unique context

// EN: after mMenuItems line
const fixes = [
    {
        // EN - find "mAddToMenu: 'Add to Menu', mMenuItems: 'Menu Items',"
        old: "mAddToMenu: 'Add to Menu', mMenuItems: 'Menu Items',",
        new: "mAddToMenu: 'Add to Menu', mMenuItems: 'Menu Items', mChooseAnItem: '-- Choose an item --', mItemAdded: 'Item added!', mItemRemoved: 'Item removed',"
    },
    {
        // ZH
        old: "mAddToMenu: '\u6dfb\u52a0\u5230\u83dc\u5355', mMenuItems: '\u83dc\u5355\u5217\u8868',",
        new: "mAddToMenu: '\u6dfb\u52a0\u5230\u83dc\u5355', mMenuItems: '\u83dc\u5355\u5217\u8868', mChooseAnItem: '-- \u9009\u62e9\u5546\u54c1 --', mItemAdded: '\u5546\u54c1\u5df2\u6dfb\u52a0\uff01', mItemRemoved: '\u5546\u54c1\u5df2\u79fb\u9664'"
    },
    {
        // MS
        old: "mAddToMenu: 'Tambah ke Menu', mMenuItems: 'Senarai Menu',",
        new: "mAddToMenu: 'Tambah ke Menu', mMenuItems: 'Senarai Menu', mChooseAnItem: '-- Pilih Item --', mItemAdded: 'Item ditambah!', mItemRemoved: 'Item dibuang'"
    },
    {
        // TA
        old: "mAddToMenu: '\u0bae\u0bc6\u0ba9\u0bc1\u0bb5\u0bbf\u0bb2\u0bcd \u0b9a\u0bc7\u0bb0\u0bcd', mMenuItems: '\u0bae\u0bc6\u0ba9\u0bc1 \u0baa\u0b9f\u0bcd\u0b9f\u0bbf\u0baf\u0bb2\u0bcd',",
        new: "mAddToMenu: '\u0bae\u0bc6\u0ba9\u0bc1\u0bb5\u0bbf\u0bb2\u0bcd \u0b9a\u0bc7\u0bb0\u0bcd', mMenuItems: '\u0bae\u0bc6\u0ba9\u0bc1 \u0baa\u0b9f\u0bcd\u0b9f\u0bbf\u0baf\u0bb2\u0bcd', mChooseAnItem: '-- \u0b92\u0bb0\u0bc1 \u0b89\u0bb0\u0bc1\u0bae\u0bc8\u0baf\u0bc8 \u0ba4\u0bc7\u0bb0\u0bcd\u0ba8\u0bcd\u0ba4\u0bc6\u0b9f\u0bc1\u0b95\u0bcd\u0b95\u0bb5\u0bc1\u0bae\u0bcd --', mItemAdded: '\u0b89\u0bb0\u0bc1\u0bae\u0bc8 \u0b9a\u0bc7\u0bb0\u0bcd\u0b95\u0bcd\u0b95\u0baa\u0bcd\u0baa\u0b9f\u0bcd\u0b9f\u0ba4\u0bcd\u0ba4\u0bc1!', mItemRemoved: '\u0b89\u0bb0\u0bc1\u0bae\u0bc8 \u0ba8\u0bc0\u0b95\u0bcd\u0b95\u0baa\u0bcd\u0baa\u0b9f\u0bcd\u0b9f\u0ba4\u0bcd\u0ba4\u0bc1'"
    }
];

let count = 0;
for (const f of fixes) {
    if (content.includes(f.old)) {
        content = content.replace(f.old, f.new);
        count++;
        console.log(`  Added keys for: ${f.old.substring(0, 40)}...`);
    } else {
        console.log(`  NOT FOUND: ${f.old.substring(0, 40)}`);
    }
}

fs.writeFileSync(file, content, 'utf8');
console.log(`\nDone! ${count}/4 languages updated.`);
