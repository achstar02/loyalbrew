import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 6848-6879 (1-indexed) = 6847-6878 (0-indexed)
old_lines = lines[6847:6879]
print('Lines to replace: ' + str(len(old_lines)))

new_content = """    document.getElementById('sa-list').innerHTML = merchants.map(m => `
      <div style="display:grid;grid-template-columns:1.5fr 1fr 0.5fr 0.6fr 1.5fr;padding:12px 16px;border-bottom:1px solid #f1f1f1;align-items:center">
        <div style="font-weight:600">${m.name || '(ununnamed)'}</div>
        <div style="font-family:ui-monospace,monospace;font-size:0.75rem;color:#555">${m.id}</div>
        <div style="text-align:center">${m.promoEnabled ? '<span style="background:#e65100;color:#fff;font-size:0.7rem;padding:3px 8px;border-radius:10px">On</span>' : '<span style="color:#ccc;font-size:0.7rem">Off</span>'}</div>
        <div style="text-align:right;font-weight:700;color:${m.credits > 0 ? '#2e7d32' : '#c62828'};font-size:1rem">${m.credits}</div>
        <div>
          <a href="https://loyalbrew-app-2f8c7.web.app/?m=${m.id}" target="_blank" style="color:#1976d2;text-decoration:none;font-size:0.75rem;background:#e3f2fd;padding:3px 10px;border-radius:6px;border:1px solid #bbdefb;display:inline-block;margin-right:4px">CUSTOMER LINK</a>
          <button onclick="_saOpenTopup('${m.id}', ${m.credits})" style="background:#1b5e20;color:#fff;border:none;padding:5px 10px;border-radius:8px;cursor:pointer;font-size:0.78rem">CREDIT</button>
          <button onclick="_saDeactivateMerchant('${m.id}', '${escHtml(m.name)}')" style="background:#b91c1c;color:#fff;border:none;padding:5px 10px;border-radius:8px;cursor:pointer;font-size:0.78rem;margin-left:4px">DELETE</button>
        </div>
      </div>`).join('') + (deletedMerchants.length > 0 ? `
      <div style="margin-top:28px;padding:0 4px">
        <div style="font-size:0.82rem;font-weight:700;color:#b91c1c;margin-bottom:10px">DELETED MERCHANTS (${deletedMerchants.length})</div>
        ${deletedMerchants.map(m => `
          <div style="display:grid;grid-template-columns:1.5fr 1fr 0.5fr 0.6fr 1.5fr;padding:12px 16px;border-bottom:1px solid #f1f1f1;align-items:center;background:#fff5f5">
            <div style="font-weight:600;color:#888;text-decoration:line-through">${m.name || '(ununnamed)'}</div>
            <div style="font-family:ui-monospace,monospace;font-size:0.75rem;color:#888">${m.id}</div>
            <div style="text-align:center"><span style="color:#ccc;font-size:0.7rem">-</span></div>
            <div style="text-align:right;font-weight:700;color:#c62828;font-size:1rem">${m.credits}</div>
            <div>
              <a href="https://loyalbrew-app-2f8c7.web.app/?m=${m.id}" target="_blank" style="color:#1976d2;text-decoration:none;font-size:0.75rem;background:#e3f2fd;padding:3px 10px;border-radius:6px;border:1px solid #bbdefb;display:inline-block;margin-right:4px">CUSTOMER LINK</a>
              <button onclick="_saRestoreMerchant('${m.id}', '${escHtml(m.name || '')}')" style="background:#1e40af;color:#fff;border:none;padding:5px 10px;border-radius:8px;cursor:pointer;font-size:0.78rem">RESTORE</button>
            </div>
          </div>`).join('')}
      </div>
    ` : '');
"""

# The first line of new_content has the correct 4-space indent matching line 6848
new_lines = new_content.split('\n')
# Replace the range
lines[6847:6879] = new_lines

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('write done')