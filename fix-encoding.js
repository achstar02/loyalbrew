const fs = require('fs');
const path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\public\\app.js';

// Windows-1252 to UTF-8 mapping for bytes 0x80-0x9F
const win1252ToUtf8 = {
  0x80: 0x20AC, // €
  0x81: 0x0081, // (control)
  0x82: 0x201A, // ‚
  0x83: 0x0192, // ƒ
  0x84: 0x201E, // „
  0x85: 0x2026, // …
  0x86: 0x2020, // †
  0x87: 0x2021, // ‡
  0x88: 0x02C6, // ˆ
  0x89: 0x2030, // ‰
  0x8A: 0x0160, // Š
  0x8B: 0x2039, // ‹
  0x8C: 0x0152, // Œ
  0x8D: 0x008D, // (control)
  0x8E: 0x017D, // Ž
  0x8F: 0x008F, // (control)
  0x90: 0x0090, // (control)
  0x91: 0x2018, // '
  0x92: 0x2019, // '
  0x93: 0x201C, // "
  0x94: 0x201D, // "
  0x95: 0x2022, // •
  0x96: 0x2013, // –
  0x97: 0x2014, // —
  0x98: 0x02DC, // ˜
  0x99: 0x2122, // ™
  0x9A: 0x0161, // š
  0x9B: 0x203A, // ›
  0x9C: 0x0153, // œ
  0x9D: 0x009D, // (control)
  0x9E: 0x017E, // ž
  0x9F: 0x0178, // Ÿ
};

// Read file as buffer
const input = fs.readFileSync(path);
const output = [];
let changes = 0;

for (let i = 0; i < input.length; i++) {
  const byte = input[i];
  if (byte >= 0x80 && byte <= 0x9F) {
    // Windows-1252 character - convert to UTF-8
    const codePoint = win1252ToUtf8[byte];
    if (codePoint && codePoint <= 0xFFFF) {
      // Convert code point to UTF-8 bytes
      if (codePoint <= 0x7F) {
        output.push(codePoint);
      } else if (codePoint <= 0x7FF) {
        output.push(0xC0 | (codePoint >> 6));
        output.push(0x80 | (codePoint & 0x3F));
      } else {
        output.push(0xE0 | (codePoint >> 12));
        output.push(0x80 | ((codePoint >> 6) & 0x3F));
        output.push(0x80 | (codePoint & 0x3F));
      }
      changes++;
    } else {
      output.push(byte); // Keep original if no mapping
    }
  } else {
    output.push(byte);
  }
}

if (changes > 0) {
  fs.writeFileSync(path, Buffer.from(output), 'utf8');
  console.log(`Fixed ${changes} Windows-1252 characters in ${path}`);
} else {
  console.log('No Windows-1252 characters found');
}
