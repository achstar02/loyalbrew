const fs = require('fs');
const path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
const buf = fs.readFileSync(path);
let content = buf.toString('utf8');

// Fix calling patterns: safeLS.json(KEY || 'FALLBACK') -> safeLS.json(KEY, FALLBACK)
let fixCount = 0;
const fixes = [
  [" || '[]')", ", [])"],
  [" || '{}')", ", {})"],
  [" || 'null')", ", null)"],
];
for (const [from, to] of fixes) {
  const before = content.length;
  content = content.split(from).join(to);
  if (content.length !== before) {
    fixCount += (before - content.length) / (from.length - to.length);
  }
}
console.log('Fixed calling patterns:', fixCount);

// Rewrite safeLS helper with correct implementation
const safeStart = content.indexOf('// ===== SAFE LOCALSTORAGE WRAPPER =====');
const safeEnd = content.indexOf('\n// =====', safeStart + 10);
let blockEnd = safeEnd > safeStart ? safeEnd : content.length;

const newHelper = [
  '// ===== SAFE LOCALSTORAGE WRAPPER =====',
  'const safeLS = (() => {',
  '  const noop = () => {};',
  '  const ls = (() => { try { return localStorage; } catch(e) { return { getItem: noop, setItem: noop, removeItem: noop }; } })();',
  '  return {',
  "    get(k, fb)  { try { const v = ls.getItem(k); return v !== null ? v : (fb !== undefined ? fb : null); } catch(e) { return fb !== undefined ? fb : null; } },",
  "    set(k, v)  { try { ls.setItem(k, String(v)); } catch(e) { /* quota/unavailable */ } },",
  '    del(k)     { try { ls.removeItem(k); } catch(e) { /* noop */ } },',
  "    json(k, fb){ try { const v = ls.getItem(k); if (v === null) return fb !== undefined ? fb : null; return JSON.parse(v); } catch(e) { return fb !== undefined ? fb : null; } },",
  "    setJSON(k, v) { try { ls.setItem(k, JSON.stringify(v)); } catch(e) { /* quota/unavailable */ } }",
  '  };',
  '})();',
  ''
].join('\n');

if (safeStart >= 0) {
  content = content.slice(0, safeStart) + newHelper + content.slice(blockEnd);
  console.log('Rewrote safeLS helper');
} else {
  console.log('WARNING: safeLS block not found');
}

// Verify
const rawLS = (content.match(/localStorage\.\w+\(/g) || []).length;
let syntaxOk = false;
try { new Function(content); syntaxOk = true; } catch(e) { console.log('Syntax error:', e.message); }

const outBuf = Buffer.from(content, 'utf8');
fs.writeFileSync(path, outBuf);

console.log('Raw localStorage calls:', rawLS);
console.log('Syntax OK:', syntaxOk);
console.log('Size:', buf.length, '->', outBuf.length);

const idx = content.indexOf('getOrders()');
if (idx >= 0) console.log('Sample:', content.substring(idx, idx + 110).replace(/\n/g, ' '));
