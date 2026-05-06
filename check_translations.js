const fs = require('fs');
const s = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

// Find LANGS object
const langsMatch = s.match(/const LANGS\s*=\s*\{[\s\S]*?\n\};/);
const merchantMatch = s.match(/const MERCHANT_LANGS\s*=\s*\{[\s\S]*?\n\};/);

function analyzeLangs(objStr, name) {
  const lines = objStr.split('\n');
  let inLang = false;
  let langKeys = { en: [], zh: [], ms: [], ta: [] };
  let currentLang = '';

  lines.forEach(l => {
    const langMatch = l.match(/^\s*(en|zh|ms|ta):\s*\{/);
    if (langMatch) {
      currentLang = langMatch[1];
      inLang = true;
    } else if (l.match(/^\s*\}\s*,?\s*$/)) {
      inLang = false;
    } else if (inLang) {
      const keyMatch = l.match(/^\s*(\w+):\s*['"]/);
      if (keyMatch) {
        langKeys[currentLang].push(keyMatch[1]);
      }
    }
  });

  const allKeys = new Set([...langKeys.en, ...langKeys.zh, ...langKeys.ms, ...langKeys.ta]);
  console.log(`\n=== ${name} ===`);
  console.log(`Total unique keys: ${allKeys.size}`);

  ['en', 'zh', 'ms', 'ta'].forEach(lang => {
    const missing = [...allKeys].filter(k => !langKeys[lang].includes(k));
    if (missing.length > 0) {
      console.log(`${lang}: MISSING ${missing.length} keys`);
      missing.slice(0, 10).forEach(k => console.log(`  - ${k}`));
      if (missing.length > 10) console.log(`  ... and ${missing.length - 10} more`);
    } else {
      console.log(`${lang}: OK (${langKeys[lang].length} keys)`);
    }
  });
}

if (langsMatch) analyzeLangs(langsMatch[0], 'LANGS (Customer)');
if (merchantMatch) analyzeLangs(merchantMatch[0], 'MERCHANT_LANGS');
