// -*- coding: utf-8 -*-
const fs = require('fs');
const content = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js.bak', 'utf8');
const out = fs.createWriteStream('C:/Users/Administrator/CodeBuddy/20260416214625/structure_analysis.txt', {encoding:'utf8'});

function log(msg) {
    out.write(msg + '\n');
    console.log(msg);
}

log('Total file size: ' + content.length);

// MLANGS analysis
const mlStart = content.indexOf('const MERCHANT_LANGS = {');
log('MERCHANT_LANGS starts at: ' + mlStart);

// Find where en block ends (depth 0 after entering en)
let depth = 0, enEnd = -1, inEn = false;
for (let i = mlStart + 25; i < content.length; i++) {
    const c = content[i];
    if (c === '{') { depth++; inEn = true; }
    else if (c === '}') {
        depth--;
        if (inEn && depth === 0) { enEnd = i; break; }
    }
}
log('MERCHANT_LANGS en block ends at: ' + enEnd);

// Count indent of '  en:' in MLANGS
const enStart = content.indexOf('en:', mlStart);
log('  en: at ' + enStart + ' snippet: ' + JSON.stringify(content.slice(enStart, enStart+50)));

// After en block ends, what language block comes next?
const afterEn = content.slice(enEnd, enEnd + 200);
log('After en block (first 200 chars): ' + JSON.stringify(afterEn));

// Find zh/ms/ta in the range after en block
const markers = ['zh:', 'ms:', 'ta:'];
for (const m of markers) {
    const pos = content.indexOf(m, enEnd + 1);
    if (pos > 0 && pos < enEnd + 50000) {
        // Count leading spaces
        let sp = pos - 1;
        while (sp >= 0 && content[sp] === ' ') sp--;
        const indent = pos - sp - 1;
        log(m + ' at ' + pos + ' indent=' + indent + ' snippet: ' + JSON.stringify(content.slice(pos, pos+50)));
    } else {
        log(m + ' NOT FOUND near en block');
    }
}

// Find the end of the entire MERCHANT_LANGS object
depth = 0;
let mlEnd = -1;
for (let i = mlStart + 25; i < content.length; i++) {
    const c = content[i];
    if (c === '{') depth++;
    else if (c === '}') {
        depth--;
        if (depth === 0) { mlEnd = i; break; }
    }
}
log('MERCHANT_LANGS ends at: ' + mlEnd);
log('Content around end: ' + JSON.stringify(content.slice(mlEnd - 30, mlEnd + 30)));

// What's at 326180 (ta:)
const taPos = content.indexOf('ta:');
if (taPos > 0) {
    log('ta: at ' + taPos);
    log('Snippet: ' + JSON.stringify(content.slice(taPos - 30, taPos + 50)));
}

out.end();
console.log('Done. See structure_analysis.txt');
