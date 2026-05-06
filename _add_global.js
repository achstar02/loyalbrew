var fs = require('fs');
var code = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

var newFunctions = `

// ══════════════════════════════════════════════════════
// 商家注册 Modal 函数 (全局作用域)
// ══════════════════════════════════════════════════════
window._saOpenRegModal = function() {
  var old = document.getElementById('sa-reg-modal');
  if(old) old.remove();
  var m = document.createElement('div');
  m.id = 'sa-reg-modal';
  m.style = 'position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:99999;display:flex;align-items:center;justify-content:center';
  m.innerHTML = '<div style="background:#0f172a;padding:32px;border-radius:20px;width:400px;color:#f1f5f9;font-family:sans-serif">' +
    '<h2 style="margin:0 0 20px 0">🏪 新增商家</h2>' +
    '<input id="sa-reg-name" placeholder="商家名称 *" style="width:100%;padding:10px;margin-bottom:12px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:8px">' +
    '<div style="display:flex;gap:8px;margin-bottom:12px"><input id="sa-reg-id" placeholder="商家 ID *" style="flex:1;padding:10px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:8px"><button onclick="_saGenId2()" style="padding:0 16px;background:#1e3a5f;color:#60a5fa;border-radius:8px;border:1px solid #1e3a5f;cursor:pointer">🎲</button></div>' +
    '<input id="sa-reg-phone" placeholder="联系电话 (可选)" style="width:100%;padding:10px;margin-bottom:12px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:8px">' +
    '<input id="sa-reg-credits" type="number" value="100" placeholder="初始 Credits" style="width:100%;padding:10px;margin-bottom:12px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:8px">' +
    '<div id="sa-reg-err" style="display:none;color:#f87171;margin-bottom:12px;font-size:0.85rem"></div>' +
    '<div style="display:flex;gap:10px"><button onclick="_saSubmitReg()" style="flex:1;padding:12px;background:#15803d;color:#fff;border:none;border-radius:10px;cursor:pointer;font-size:1rem;font-weight:600">💾 保存</button><button onclick="_saCloseRegModal()" style="padding:12px 20px;background:#1e293b;color:#94a3b8;border:1px solid #334155;border-radius:10px;cursor:pointer">取消</button></div>' +
  '</div>';
  document.body.appendChild(m);
  var idInput = document.getElementById('sa-reg-id');
  if (idInput) {
    idInput.addEventListener('keydown', function(e) {
      if(e.key === 'Enter') _saSubmitReg();
    });
  }
};
window._saCloseRegModal = function() {
  var m = document.getElementById('sa-reg-modal');
  if(m) m.remove();
};
window._saGenId2 = function() {
  var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
  var id = '';
  for(var i = 0; i < 10; i++) id += chars[Math.floor(Math.random() * chars.length)];
  var el = document.getElementById('sa-reg-id');
  if(el) el.value = id;
};
window._saSubmitReg = async function() {
  var fb = window.__lbFirebase;
  if(!fb || !fb.db) {
    var err = document.getElementById('sa-reg-err');
    if(err) { err.textContent = 'Firebase未就绪'; err.style.display = 'block'; }
    return;
  }
  var name = document.getElementById('sa-reg-name').value.trim();
  var id = document.getElementById('sa-reg-id').value.trim();
  var phone = document.getElementById('sa-reg-phone').value.trim();
  var credits = parseFloat(document.getElementById('sa-reg-credits').value) || 100;
  var err = document.getElementById('sa-reg-err');
  if(!name || !id) {
    if(err) { err.textContent = '请填写名称和ID'; err.style.display = 'block'; }
    return;
  }
  if(err) { err.textContent = '提交中...'; err.style.display = 'block'; err.style.color = '#60a5fa'; }
  try {
    var ref = fb.doc(fb.db, 'merchants', id);
    var existing = await fb.getDoc(ref);
    if(existing.exists()) {
      if(err) { err.textContent = 'ID已存在'; err.style.color = '#f87171'; }
      return;
    }
    var now = new Date().toISOString();
    await fb.runTransaction(fb.db, function(tx) {
      return tx.get(ref).then(function(snap) {
        if(snap.exists()) throw new Error('冲突');
        tx.set(ref, {
          merchant_name: name,
          credits: credits,
          phone: phone || null,
          email: null,
          createdAt: now,
          updatedAt: now,
          createdBy: SUPER_ADMIN_EMAIL,
          active: true
        });
      });
    });
    showToast('商家 [' + name + '] 注册成功!', 'success');
    _saCloseRegModal();
    if(typeof _loadSuperAdminMerchants === 'function') _loadSuperAdminMerchants();
  } catch(e) {
    if(err) { err.textContent = '错误: ' + (e.message || '未知'); err.style.color = '#f87171'; }
    console.error(e);
  }
};
`;

code = code + newFunctions;
fs.writeFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', code);
console.log('Added global functions');