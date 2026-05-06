// _patch_register_merchant.js
var fs = require('fs');
var FILE = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js';
var code = fs.readFileSync(FILE, 'utf8');
var orig = code;

// ══════════════════════════════════════════════════════
// 1. 在 _renderSuperAdminPage() 之前插入注册函数
// ══════════════════════════════════════════════════════
var NEW_FUNCTIONS = ['',
'// ══════════════════════════════════════════════════════',
'// 注册新商家 - Toggle 折叠表单',
'// ══════════════════════════════════════════════════════',
"window._saToggleRegisterForm = function() {",
'  var panel = document.getElementById("sa-register-panel");',
'  if (!panel) return;',
'  var isHidden = panel.style.display === "none";',
'  panel.style.display = isHidden ? "block" : "none";',
'  var btn = document.getElementById("sa-toggle-reg-btn");',
'  if (btn) {',
'    btn.textContent = isHidden ? "- 收起表单" : "+ 新增商家";',
'    btn.style.background = isHidden ? "#374151" : "#1b5e20";',
'  }',
'};',
'',
'// ══════════════════════════════════════════════════════',
'// 注册新商家 - 随机生成商家 ID',
'// ══════════════════════════════════════════════════════',
"window._saGenerateMerchantId = function() {",
'  var chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";',
'  var id = "";',
'  for (var i = 0; i < 8; i++) id += chars[Math.floor(Math.random() * chars.length)];',
'  var el = document.getElementById("sa-reg-merchant-id");',
'  if (el) el.value = id;',
'};',
'',
'// ══════════════════════════════════════════════════════',
'// 注册新商家 - 提交处理',
'// ══════════════════════════════════════════════════════',
"window._saSubmitRegister = async function() {",
'  var fb = window.__lbFirebase;',
'  if (!fb || !fb.db) { showToast("Firebase 未就绪", "error"); return; }',
'',
'  var nameEl   = document.getElementById("sa-reg-merchant-name");',
'  var idEl     = document.getElementById("sa-reg-merchant-id");',
'  var creditEl = document.getElementById("sa-reg-credits");',
'  var emailEl  = document.getElementById("sa-reg-email");',
'',
'  var name       = nameEl  ? nameEl.value.trim()  : "";',
'  var merchantId  = idEl    ? idEl.value.trim()     : "";',
'  var creditsVal = parseFloat(creditEl ? creditEl.value : "0") || 0;',
'  var emailVal   = emailEl  ? emailEl.value.trim()  : "";',
'',
'  // 验证',
'  if (!name)      { showToast("请填写商家名称", "error"); if(nameEl) nameEl.focus(); return; }',
'  if (!merchantId){ showToast("请填写商家 ID",   "error"); if(idEl)   idEl.focus();   return; }',
'  if (creditsVal < 0){ showToast("Credits 不能为负数", "error"); return; }',
'  if (emailVal && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(emailVal)) {',
'    showToast("邮箱格式不正确", "error"); if(emailEl) emailEl.focus(); return;',
'  }',
'',
'  var btn = document.getElementById("sa-reg-submit-btn");',
'  var origText = btn ? btn.textContent : "提交注册";',
'  if (btn) { btn.disabled = true; btn.textContent = "提交中..."; }',
'',
'  try {',
'    // 检查 ID 是否已存在',
'    var ref = fb.doc(fb.db, "merchants", merchantId);',
'    var existing = await fb.getDoc(ref);',
'    if (existing.exists()) {',
'      showToast("商家 ID 已存在，请更换或重新生成", "error");',
'      if (btn) { btn.disabled = false; btn.textContent = origText; }',
'      return;',
'    }',
'',
'    // 写入 Firestore（事务保证原子性）',
'    var now = new Date().toISOString();',
'    await fb.runTransaction(fb.db, function(tx) {',
'      return tx.get(ref).then(function(snap) {',
'        if (snap.exists()) throw new Error("商家 ID 冲突，请重试");',
'        tx.set(ref, {',
'          merchant_name: name,',
'          credits:      creditsVal,',
'          email:        emailVal || null,',
'          createdAt:    now,',
'          updatedAt:    now,',
'          createdBy:    SUPER_ADMIN_EMAIL,',
'          active:       true,',
'        });',
'      });',
'    });',
'',
'    showToast("商家[" + name + "] 注册成功!", "success");',
'',
'    // 清空表单并刷新列表',
'    if (nameEl)  nameEl.value  = "";',
'    if (creditEl) creditEl.value = "";',
'    if (emailEl) emailEl.value = "";',
'    await _loadSuperAdminMerchants();',
'',
'    if (btn) { btn.disabled = false; btn.textContent = origText; }',
'  } catch(e) {',
'    console.error("_saSubmitRegister error:", e);',
'    showToast("注册失败：" + (e.message || "未知错误"), "error");',
'    if (btn) { btn.disabled = false; btn.textContent = origText; }',
'  }',
'};',
''
].join('\n');

// 找到插入点：在 "  // 内部：渲染超级管理页面" 之前
var INSERT_BEFORE = '  // 内部：渲染超级管理页面';
var idx = code.indexOf(INSERT_BEFORE);
if (idx === -1) { console.error('FAIL: 未找到插入点'); process.exit(1); }
code = code.slice(0, idx) + NEW_FUNCTIONS + code.slice(idx);
console.log('OK: 插入注册函数');

// ══════════════════════════════════════════════════════
// 2. 替换 HTML，加入注册表单
// ══════════════════════════════════════════════════════
var OLD_HTML = '        <div id="sa-summary" style="color:#666;margin-bottom:16px;font-size:0.9rem">加载中...</div>\n        <div id="sa-list" style="background:#fff;border-radius:14px;overflow:hidden;border:1px solid #eee">加载商家数据中...</div>';

var NEW_HTML = [
'        <div id="sa-summary" style="color:#666;margin-bottom:16px;font-size:0.9rem">加载中...</div>',
'',
'        <!-- 新增商家表单 -->',
'        <div style="background:#1e293b;border-radius:14px;overflow:hidden;margin-bottom:16px;border:1px solid #334155">',
'          <div style="padding:14px 18px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">',
'            <div style="display:flex;align-items:center;gap:10px">',
'              <span style="font-size:1.1rem">🏪</span>',
'              <span style="color:#f1f5f9;font-weight:700;font-size:0.95rem">新增商家</span>',
'            </div>',
'            <button id="sa-toggle-reg-btn" onclick="_saToggleRegisterForm()"',
'              style="background:#1b5e20;color:#fff;border:none;padding:7px 16px;border-radius:8px;cursor:pointer;font-size:0.82rem;font-weight:600">+ 新增商家</button>',
'          </div>',
'          <div id="sa-register-panel" style="display:none;padding:0 18px 18px">',
'            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">',
'              <div>',
'                <label style="display:block;color:#94a3b8;font-size:0.75rem;margin-bottom:5px;font-weight:600">商家名称 *</label>',
'                <input id="sa-reg-merchant-name" type="text" placeholder="如：大学档口 A"',
'                  style="width:100%;padding:9px 12px;background:#0f172a;border:1px solid #334155;color:#f1f5f9;border-radius:8px;font-size:0.88rem;box-sizing:border-box" />',
'              </div>',
'              <div>',
'                <label style="display:block;color:#94a3b8;font-size:0.75rem;margin-bottom:5px;font-weight:600">商家 ID（唯一标识） *</label>',
'                <div style="display:flex;gap:6px">',
'                  <input id="sa-reg-merchant-id" type="text" placeholder="8位字母数字"',
'                    style="flex:1;padding:9px 12px;background:#0f172a;border:1px solid #334155;color:#f1f5f9;border-radius:8px;font-size:0.88rem;box-sizing:border-box" />',
'                  <button onclick="_saGenerateMerchantId()" title="随机生成"',
'                    style="padding:0 12px;background:#334155;color:#f1f5f9;border:none;border-radius:8px;cursor:pointer;font-size:1.1rem;white-space:nowrap">&#127922;</button>',
'                </div>',
'              </div>',
'              <div>',
'                <label style="display:block;color:#94a3b8;font-size:0.75rem;margin-bottom:5px;font-weight:600">初始 Credits *</label>',
'                <input id="sa-reg-credits" type="number" min="0" step="0.01" placeholder="0.00"',
'                  style="width:100%;padding:9px 12px;background:#0f172a;border:1px solid #334155;color:#f1f5f9;border-radius:8px;font-size:0.88rem;box-sizing:border-box" />',
'              </div>',
'              <div>',
'                <label style="display:block;color:#94a3b8;font-size:0.75rem;margin-bottom:5px;font-weight:600">关联邮箱（可选）</label>',
'                <input id="sa-reg-email" type="email" placeholder="merchant@example.com"',
'                  style="width:100%;padding:9px 12px;background:#0f172a;border:1px solid #334155;color:#f1f5f9;border-radius:8px;font-size:0.88rem;box-sizing:border-box" />',
'              </div>',
'            </div>',
'            <div style="margin-top:12px;display:flex;gap:8px;align-items:center">',
'              <button id="sa-reg-submit-btn" onclick="_saSubmitRegister()"',
'                style="background:linear-gradient(135deg,#1b5e20,#2e7d32);color:#fff;border:none;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:0.88rem;font-weight:700">提交注册</button>',
'              <span style="color:#64748b;font-size:0.72rem">* 必填项 · 点击 &#127922; 随机生成商家 ID</span>',
'            </div>',
'          </div>',
'        </div>',
'',
'        <div id="sa-list" style="background:#fff;border-radius:14px;overflow:hidden;border:1px solid #eee">加载商家数据中...</div>'
].join('\n');

if (!code.includes(OLD_HTML)) { console.error('FAIL: 未找到替换 HTML 片段'); process.exit(1); }
code = code.replace(OLD_HTML, NEW_HTML);
console.log('OK: 替换 HTML');

// ══════════════════════════════════════════════════════
// 3. 注册全局函数
// ══════════════════════════════════════════════════════
var BIND_TARGET = 'window._showSuperAdminBtn = _showSuperAdminBtn;';
var BIND_NEW = 'window._saToggleRegisterForm = _saToggleRegisterForm;\n' + BIND_TARGET;
if (!code.includes('window._saToggleRegisterForm = _saToggleRegisterForm;')) {
  var idx2 = code.indexOf(BIND_TARGET);
  if (idx2 === -1) { console.error('FAIL: 未找到 window 绑定插入点'); process.exit(1); }
  code = code.slice(0, idx2) + BIND_NEW + code.slice(idx2);
  console.log('OK: 添加 window 绑定');
}

fs.writeFileSync(FILE, code, 'utf8');
console.log('DONE: 商家注册功能补丁已应用');
