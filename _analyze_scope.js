// _analyze_scope.js - Find exact line where showSuperAdminPage ends
var fs = require('fs');

var code = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
var lines = code.split('\n');

var inFunc = false;
var depth = 0;
var startLine = -1;

for (var i = 0; i < lines.length; i++) {
  var line = lines[i];
  var lnum = i + 1;
  
  if (lnum >= 5075 && lnum <= 5220) {
    // Detect function start
    if (/window\.showSuperAdminPage\s*=\s*async\s+function/.test(line)) {
      inFunc = true;
      startLine = lnum;
      depth = 0;
      console.log('Found function start at line', lnum, ':', line.trim().substring(0, 60));
    }
    
    if (inFunc) {
      // Count braces (simple)
      for (var j = 0; j < line.length; j++) {
        if (line[j] === '{') depth++;
        if (line[j] === '}') depth--;
      }
      
      // Detect async function body opening
      if (/window\.showSuperAdminPage\s*=\s*async\s+function\s*\(/.test(line) || 
          (lnum === startLine && line.includes('async function'))) {
        // already found above
      }
      
      if (depth === 0 && lnum > startLine && startLine > 0) {
        console.log('Function ends at line', lnum, ':', line.trim());
        inFunc = false;
        break;
      }
    }
  }
}

// Also find line of _saToggleRegisterForm
for (var i = 0; i < lines.length; i++) {
  if (lines[i].includes('window._saToggleRegisterForm = function')) {
    console.log('_saToggleRegisterForm defined at line', i + 1);
  }
  if (lines[i].includes('// 注册新商家 - Toggle')) {
    console.log('Comment before toggle at line', i + 1);
  }
}

// Find the closing of showSuperAdminPage's async function
// by looking for the last 'return;' inside it
for (var i = 0; i < lines.length; i++) {
  var lnum = i + 1;
  if (lnum >= 5078 && lnum <= 5195) {
    if (/\breturn\b/.test(lines[i]) && !lines[i].includes('//') && lines[i].trim() === 'return;') {
      console.log('return; at line', lnum, ':', lines[i]);
    }
  }
}
