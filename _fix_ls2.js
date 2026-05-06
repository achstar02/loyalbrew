const fs = require('fs');
const path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
const buf = fs.readFileSync(path);
let content = buf.toString('utf8');
const origSize = buf.length;

// Step 1: Remove the safeLS block
const safeStart = content.indexOf('// ===== SAFE LOCALSTORAGE WRAPPER =====');
const safeEnd = content.indexOf('// ===== MERCHANT DATA ISOLATION HELPER =====');
if (safeStart >= 0 && safeEnd >= 0) {
  content = content.slice(0, safeStart) + content.slice(safeEnd);
  console.log('Removed safeLS block');
}

// Step 2: Reverse safeLS.json patterns back to JSON.parse(localStorage.getItem...)
let fixCount = 0;

// safeLS.json(X || '[]') -> JSON.parse(localStorage.getItem(X) || '[]')
content = content.replace(/safeLS\.json\((.+?)\s*\|\|\s*'\[\\]'\)/g, (m, inner) => {
  fixCount++;
  return 'JSON.parse(localStorage.getItem(' + inner.trim() + ") || '[]')";
});

// safeLS.json(X || '{}') -> JSON.parse(localStorage.getItem(X) || '{}')
content = content.replace(/safeLS\.json\((.+?)\s*\|\|\s*'\{\\}'\)/g, (m, inner) => {
  fixCount++;
  return "JSON.parse(localStorage.getItem(" + inner.trim() + ") || '{}')";
});

// safeLS.json(X || 'null') -> JSON.parse(localStorage.getItem(X) || 'null')
content = content.replace(/safeLS\.json\((.+?)\s*\|\|\s*'null'\)/g, (m, inner) => {
  fixCount++;
  return "JSON.parse(localStorage.getItem(" + inner.trim() + ") || 'null')";
});

// safeLS.json(X, []) -> JSON.parse(localStorage.getItem(X) || '[]')
content = content.replace(/safeLS\.json\((.+?),\s*\[\\])\)/g, (m, inner) => {
  fixCount++;
  return 'JSON.parse(localStorage.getItem(' + inner.trim() + ") || '[]')";
});

// safeLS.json(X, {}) -> JSON.parse(localStorage.getItem(X) || '{}')
content = content.replace(/safeLS\.json\((.+?),\s*\{\\})\)/g, (m, inner) => {
  fixCount++;
  return "JSON.parse(localStorage.getItem(" + inner.trim() + ") || '{}')";
});

// safeLS.json(X, null) -> JSON.parse(localStorage.getItem(X) || 'null')
content = content.replace(/safeLS\.json\((.+?),\s*null\)/g, (m, inner) => {
  fixCount++;
  return "JSON.parse(localStorage.getItem(" + inner.trim() + ") || 'null')";
});

// safeLS.json(X) no fallback -> JSON.parse(localStorage.getItem(X))
content = content.replace(/safeLS\.json\(([^,)]+)\)/g, (m, inner) => {
  fixCount++;
  return 'JSON.parse(localStorage.getItem(' + inner.trim() + '))';
});

// Step 3: Reverse safeLS.setJSON(X, V) -> localStorage.setItem(X, JSON.stringify(V))
content = content.replace(/safeLS\.setJSON\((.+?),\s*(.+?)\)/g, (m, key, val) => {
  fixCount++;
  return 'localStorage.setItem(' + key.trim() + ', JSON.stringify(' + val.trim() + '))';
});

// Step 4: Reverse simple replacements
content = content.replace(/safeLS\.get\(/g, () => { fixCount++; return 'localStorage.getItem('; });
content = content.replace(/safeLS\.set\(/g, () => { fixCount++; return 'localStorage.setItem('; });
content = content.replace(/safeLS\.del\(/g, () => { fixCount++; return 'localStorage.removeItem('; });

// Step 5: Add Proxy wrapper after first line
const headerEnd = content.indexOf('\n');
const proxyWrapper = [
  "// ===== SAFE LOCALSTORAGE WRAPPER (Proxy) =====",
  "const _origLS = (() => { try { return localStorage; } catch(e) { return null; } })();",
  "if (_origLS) {",
  "  const _ls = new Proxy(_origLS, {",
  "    get(t, p) {",
  "      if (p === 'getItem') return (k) => { try { return t.getItem(k); } catch(e) { return null; } };",
  "      if (p === 'setItem') return (k, v) => { try { t.setItem(k, String(v)); } catch(e) { /* quota */ } };",
  "      if (p === 'removeItem') return (k) => { try { t.removeItem(k); } catch(e) { /* noop */ } };",
  "      if (p === 'clear') return () => { try { t.clear(); } catch(e) { /* noop */ } };",
  "      if (p === 'length') return t.length;",
  "      if (typeof t[p] === 'function') return t[p].bind(t);",
  "      return Reflect.get(t, p);",
  "    }",
  "  });",
  "  Object.defineProperty(globalThis, 'localStorage', { value: _ls, writable: false, configurable: true });",
  "} else {",
  "  Object.defineProperty(globalThis, 'localStorage', {",
  "    value: { getItem: () => null, setItem: () => {}, removeItem: () => {}, clear: () => {}, length: 0 },",
  "    writable: false, configurable: true",
  "  });",
  "}",
  ""
].join('\n');

content = content.slice(0, headerEnd + 1) + proxyWrapper + content.slice(headerEnd + 1);

// Step 6: Verify
const remaining = (content.match(/safeLS\.\w+\(/g) || []).length;
const lsCalls = (content.match(/localStorage\.\w+\(/g) || []).length;

const outBuf = Buffer.from(content, 'utf8');

// Syntax check
let syntaxOk = false;
try { new Function(content); syntaxOk = true; } catch(e) {}

fs.writeFileSync(path, outBuf);

console.log('Total fixes:', fixCount);
console.log('Remaining safeLS calls:', remaining);
console.log('Total localStorage calls:', lsCalls);
console.log('Syntax OK:', syntaxOk);
console.log('Size:', origSize, '->', outBuf.length);
