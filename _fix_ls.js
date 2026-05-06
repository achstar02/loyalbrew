const fs = require('fs');
const path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
const buf = fs.readFileSync(path);
let content = buf.toString('utf8');

const origSize = buf.length;

// 1. Insert safeLS helper after the first line
const headerEnd = content.indexOf('\n');
const safeLS = `
// ===== SAFE LOCALSTORAGE WRAPPER =====
const safeLS = (() => {
  const noop = () => {};
  const ls = (() => { try { return localStorage; } catch(e) { return { getItem: noop, setItem: noop, removeItem: noop }; } })();
  return {
    get(k, fb)  { try { const v = ls.getItem(k); return v !== null ? v : (fb !== undefined ? fb : null); } catch(e) { return fb !== undefined ? fb : null; } },
    set(k, v)  { try { ls.setItem(k, String(v)); } catch(e) { /* quota/unavailable */ } },
    del(k)     { try { ls.removeItem(k); } catch(e) { /* noop */ } },
    json(k, fb){ try { const v = ls.getItem(k); if (v === null) return fb !== undefined ? fb : null; return JSON.parse(v); } catch(e) { return fb !== undefined ? fb : null; } },
    setJSON(k, v) { try { ls.setItem(k, JSON.stringify(v)); } catch(e) { /* quota/unavailable */ } }
  };
})();
`;

content = content.slice(0, headerEnd + 1) + safeLS + content.slice(headerEnd + 1);

// 2. Replace JSON.parse(localStorage.getItem(...) || 'fallback') with safeLS.json(...)
// Pattern: JSON.parse(localStorage.getItem(ANYTHING) || 'FALLBACK')
let replaceCount = 0;

// 2a. JSON.parse(localStorage.getItem(...) || '[]')
content = content.replace(/JSON\.parse\(localStorage\.getItem\(([^)]+)\)\s*\|\|\s*'\[\]'\)/g, (m, key) => {
  replaceCount++;
  return `safeLS.json(${key.trim()}, [])`;
});

// 2b. JSON.parse(localStorage.getItem(...) || '{}')
content = content.replace(/JSON\.parse\(localStorage\.getItem\(([^)]+)\)\s*\|\|\s*'\{\}'\)/g, (m, key) => {
  replaceCount++;
  return `safeLS.json(${key.trim()}, {})`;
});

// 2c. JSON.parse(localStorage.getItem(...) || 'null')
content = content.replace(/JSON\.parse\(localStorage\.getItem\(([^)]+)\)\s*\|\|\s*'null'\)/g, (m, key) => {
  replaceCount++;
  return `safeLS.json(${key.trim()}, null)`;
});

// 2d. JSON.parse(localStorage.getItem(...)) without fallback
content = content.replace(/JSON\.parse\(localStorage\.getItem\(([^)]+)\)\)/g, (m, key) => {
  replaceCount++;
  return `safeLS.json(${key.trim()})`;
});

// 3. Replace localStorage.setItem(key, JSON.stringify(val)) with safeLS.setJSON(key, val)
content = content.replace(/localStorage\.setItem\(([^,]+),\s*JSON\.stringify\(([^)]+)\)\)/g, (m, key, val) => {
  replaceCount++;
  return `safeLS.setJSON(${key.trim()}, ${val.trim()})`;
});

// 4. Replace remaining localStorage.getItem(...) with safeLS.get(...)
content = content.replace(/localStorage\.getItem\(/g, () => {
  replaceCount++;
  return 'safeLS.get(';
});

// 5. Replace remaining localStorage.setItem(...) with safeLS.set(...)
content = content.replace(/localStorage\.setItem\(/g, () => {
  replaceCount++;
  return 'safeLS.set(';
});

// 6. Replace localStorage.removeItem(...) with safeLS.del(...)
content = content.replace(/localStorage\.removeItem\(/g, () => {
  replaceCount++;
  return 'safeLS.del(';
});

// Verify no bare localStorage calls remain
const remaining = (content.match(/localStorage\.\w+\(/g) || []).length;

const outBuf = Buffer.from(content, 'utf8');
fs.writeFileSync(path, outBuf);

console.log('Replacements made:', replaceCount);
console.log('Remaining bare localStorage calls:', remaining);
console.log('Size:', origSize, '->', outBuf.length);

// Verify the safeLS helper is in place
const hasHelper = content.includes('const safeLS =');
console.log('safeLS helper present:', hasHelper);

// Spot check
const idx1 = content.indexOf('getMembers()');
console.log('getMembers:', content.substring(idx1, idx1 + 90).replace(/\n/g,' '));
