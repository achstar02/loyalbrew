# LoyalBrew 全功能审查报告

**审查时间**: 2026-05-01 10:25 (MYT)  
**审查方式**: Python 静态代码分析 + 人工逐函数审查  
**审查范围**: app.js (8429行) + index.html (1552行) + firestore.rules + firebase-init.js + firebase.json

---

## 审查总结

| 类别 | 数量 |
|------|------|
| JS 引用的 DOM ID | 259 个 |
| HTML 定义的 ID | 287 个 |
| JS 引用但 HTML 缺失的 ID | 37 个 |
| 声明函数 | 222 个 |
| 重复定义函数 | 1 个 |
| HTML 事件处理函数缺失 | 2 个(1个误报) |
| 关键函数存在性 | 全部 40/40 OK |

---

## 严重问题 (需修复)

### 问题1: 重复函数定义 - openSuperAdminMerchants()

- 行号: 第 6440 行 和 第 6753 行
- 影响: 第一个定义只调用 _ensureShowSuperAdminPage()，第二个调用 showSuperAdminPage()。后者覆盖前者，功能上不会崩溃，但代码冗余
- 建议: 删除第一个定义(行6440)

### 问题2: Firestore 规则过于宽松

- 现状: 所有集合的 allow read: if true; 任何人可读取全部数据
- 风险: 会员手机号、商家信息、订单数据完全暴露
- 关键问题:
  - complaints 集合: allow create/update/delete: if true 完全开放
  - topupRequests 集合: allow create: if true 任何人可创建充值请求
  - orders 集合: allow create: if true 任何人可伪造订单
- 建议: 必须添加至少基本的 Auth 检查

### 问题3: renderMerchantComplaints 读取全量投诉再客户端过滤

- 行号: ~5512
- 问题: getDocs(collection('complaints')) 读取全部投诉文档，然后用 JS filter 按 merchantId 过滤
- 影响: 数据量增大时严重浪费带宽和 Firestore 读配额
- 建议: 使用 query + where 过滤

---

## 中等问题 (建议修复)

### 问题4: 三个手机号输入框 HTML 中缺失，但有保护逻辑

| 缺失 ID | JS 行号 | 当前保护 |
|---------|---------|---------|
| complaint-phone | 5362 | showPage 中未登录重定向到登录页 |
| topup-phone | 5016 | showPage 中未登录重定向到登录页 |
| stamp-phone | 4399 | showPage 中未登录重定向到登录页 |

- 分析: 这三个函数中的 getElementById 在当前流程中永远不会被执行到，因为 showPage 会在用户未登录时拦截并重定向
- 风险等级: 低 - 但代码中存在死路径
- 建议: 清理死代码分支 或 添加手机号输入框

### 问题5: showSuperAdminPage 非标准定义导致误报

- HTML onclick 调用该函数
- JS 中通过 window.showSuperAdminPage = async function() 定义（行6509），不是标准 function 声明
- 影响: 无实际功能问题，只是审计工具误报

### 问题6: main-content ID 在 HTML 中不存在

- JS 行6328: getElementById('main-content')
- 影响: Super Admin 功能中的商家管理页面可能无法渲染到目标容器
- 需确认: Super Admin 页面的 DOM 挂载点是什么

---

## 正常功能确认

### 顾客端功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 顾客登录/注册 | OK | 已修复 merchantId 隔离 |
| 浏览菜单 | OK | renderMenu() + maybeShowNewItemsAnnouncement() |
| 下单(堂食+外卖) | OK | placeOrder() 含钱包扣款、积分、印花 |
| 购物车 | OK | renderCart() |
| 印花卡 | OK | renderStampCardsDisplay() |
| 钱包充值 | OK | confirmTopup -> 商家审批 -> topupWallet |
| 投诉 | OK | submitComplaint + renderMyComplaints |
| 推荐佣金 | OK | triggerReferralCommission |
| 我的订单 | OK | page-my-orders |
| 优惠活动 | OK | page-promos |
| 语言切换 | OK | setLang() + t() |

### 商家端功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 商家登录/登出 | OK | merchantLogin / merchantLogout |
| 仪表盘 | OK | loadMerchantDashboard |
| 订单管理 | OK | renderMerchantOrders + 状态切换 |
| 菜单管理 | OK | renderMenuMgmt + 促销价 |
| 新品管理 | OK | populateNewItemSelect + renderNewItemsMgmt |
| 会员管理 | OK | renderMemberTable + 激活/停用 |
| 印花卡管理 | OK | initStampMgmtTab + createStampCard |
| 充值审批 | OK | initTopupMgmtTab + approveTopup/rejectTopup |
| 投诉管理 | OK | initComplaintsMgmtTab + openComplaintDetail |
| 佣金管理 | OK | initCommissionsTab |
| QR码 | OK | initMerchantShopQR |
| 广告管理 | OK | renderMerchantAds |
| 设置 | OK | loadPromoSettings + loadShopSettings + loadPointsSettings |
| 厨房屏 | OK | loadKitchenOrders |

### 超级管理功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 登录(Firebase Auth) | OK | 自定义 modal + Email/Password |
| 商家列表 | OK | renderSuperAdminMerchantsList |
| 新增商家 | OK | _saOpenRegModal |
| 解除商家 | OK | _saDeactivateMerchant |
| 恢复商家 | OK | _saRestoreMerchant |
| 充值管理 | OK | _saOpenTopup |

### 数据层

| 组件 | 状态 | 说明 |
|------|------|------|
| FSSync 同步层 | OK | 内存+localStorage+Firestore 三写 |
| DB 对象 | OK | 商家隔离存储 |
| 钱包数据结构 | OK | 已改为 Array 格式 |
| getMemberWallet | OK | 行4942 |
| saveMemberWallet | OK | 行4952 |

### 基础设施

| 组件 | 状态 | 说明 |
|------|------|------|
| Firebase 初始化 | OK | __lbFirebase + __lbFirebaseReady |
| Firestore 引用 | OK | getFirestore |
| Firebase Auth | OK | getAuth |
| firebase.json | OK | public=. rewrite to index.html |
| hosting 部署 | OK | loyalbrew-app-2f8c7.web.app |

---

## 修复优先级建议

| 优先级 | 问题 | 工作量 |
|--------|------|--------|
| P0 紧急 | Firestore 规则过于宽松(数据泄露风险) | 中 |
| P1 高 | renderMerchantComplaints 全量读取 | 小 |
| P2 中 | 删除重复函数 openSuperAdminMerchants | 极小 |
| P3 低 | 清理三个死代码手机号分支 | 小 |
| P3 低 | 确认 main-content 挂载点 | 极小 |

---

## 37个缺失DOM ID 分类说明

大部分缺失的 ID 是动态创建的 Modal 元素，不影响功能：

| 类别 | ID列表 | 创建方式 |
|------|--------|---------|
| Super Admin Modal | sa-login-modal, sa-login-email, sa-login-pass, sa-login-error, sa-email-badge, sa-reg-modal, sa-reg-merchant-id, sa-reg-merchant-name, sa-reg-credits, sa-reg-email, sa-reg-submit-btn, sa-register-panel, sa-toggle-reg-btn, sa-summary, sa-list, sa-deactivate-confirm | JS createElement 动态创建 |
| 商家注册 Modal | mreg-name, mreg-id, mreg-password, mreg-credits, mreg-phone, mreg-err, mreg-submit | JS createElement 动态创建 |
| 促销价 Modal | promo-price-modal, ppm-item-name, ppm-normal-price, ppm-item-id, ppm-promo-price, ppm-clear-btn | createPromoPriceModal() 动态创建 |
| 印花卡创建 | sc-rule-item, sc-rule-value, sc-reward-val-input | 动态创建 |
| 真正缺失 | complaint-phone, topup-phone, stamp-phone, main-content, merchant-complaints-mid | 见上方分析 |
