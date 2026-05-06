const fs = require('fs');
const s = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

const langsMatch = s.match(/const LANGS\s*=\s*\{[\s\S]*?\n\};/);

function analyzeLangs(objStr) {
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
  
  console.log('=== Missing keys per language ===\n');
  
  ['en', 'zh', 'ms'].forEach(lang => {
    const missing = [...allKeys].filter(k => !langKeys[lang].includes(k));
    if (missing.length > 0) {
      console.log(`\n${lang.toUpperCase()} missing ${missing.length} keys:`);
      missing.forEach(k => console.log(`  - ${k}`));
    }
  });

  // Find which lang has the most complete set
  console.log('\n\n=== Reference (ta) has these translations ===\n');
  [...allKeys].forEach(k => {
    if (langKeys.ta.includes(k)) {
      console.log(`${k}: present in ta`);
    }
  });
}

if (langsMatch) analyzeLangs(langsMatch[0]);
