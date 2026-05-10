# LoyalBrew i18n 深度分析（2026-05-10 补全）

## 关键数据

| 项目 | 数量 |
|------|------|
| HTML `data-mi18n` key 总数 | 223 |
| MERCHANT_LANGS 字典 key 总数 | 324 |
| HTML key 未在字典中（mt() fallback 处理） | 182 |
| HTML key 在字典中缺失（需人工添加） | ~40 估算 |

## mt() / t() snake_case auto-conversion 原理

```javascript
// mt() 中的 fallback（在 MERCHANT_LANGS 中 key 未找到时触发）
if (key.indexOf('_') !== -1) {
  var camelKey = 'm' + key.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
  if (dict[camelKey] !== undefined) return dict[camelKey];
}
// 例：filterAll → 不转换（无下划线）→ 返回 'filterAll'
// 例：end_date → mEndDate → 存在于字典 → 返回翻译
```

**关键限制**：auto-conversion 只处理含下划线的 key，不处理 `filterAll`（无下划线）。

## HTML 中文硬编码清单（共 60+ 处）

以下行只有中文文本，没有 `data-mi18n` 属性，需要添加：

| 行号 | 当前内容 | 修复方案 |
|------|----------|----------|
| ~109 | `<!-- 我的账号 -->` | 移除注释或添加 data-mi18n |
| ~110 | `<!-- 立即点餐 -->` | 同上 |
| ~111 | `<!-- 印章卡 -->` | 同上 |
| ~112 | `<!-- 充值 -->` | 同上 |
| ~113 | `<!-- 可选 quick access -->` | 同上 |
| 956 | `<span data-mi18n="mItemPrice">特价 (RM)` | 已有 key，`mItemPrice` = 'Price (RM)' → 需添加 `mItemPrice` 翻译 |
| 965 | `<span style="color:#888" data-mi18n="mOptional">optional</span>` | 已有 `mOptional`，EN='optional'，ZH='可选' |
| ~1216 | `<span data-mi18n="mItemPrice">特价 (RM)` | 重复修复 |
| ~1249 | `<span style="color:#888" data-mi18n="mOptional">optional` | 同上 |
| ~1323 | `placeholder="例如：咖啡爱好者卡"` | 需添加 `data-mi18n-placeholder` |
| ~1325 | `placeholder="例如：☕️"` | 已有 placeholder，非 i18n |
| ~1331 | `<option ...>每消费1次=1印章</option>` | 已有 `mRulePerOrderOpt` |
| ~1334 | `<option ...>每消费RM X=1印章</option>` | 已有 `mRulePerAmountOpt` |
| ~1337 | `<option ...>购买指定商品=1印章</option>` | 已有 `mRulePerItemOpt` |
| ~1343 | `<option ...>免费菜单商品</option>` | 已有 `mRewardFreeItemOpt` |
| ~1346 | `<option ...>固定折扣(RM)</option>` | 已有 `mRewardFlatDiscountOpt` |
| ~1348 | `<option value="discount_pct">百分比折扣(%)</option>` | 需添加 `mRewardPctDiscountOpt` |
| ~1351 | `<option ...>奖励积分</option>` | 已有 `mRewardBonusPointsOpt` |
| ~1367 | `<input ... placeholder="按姓名或电话搜索会员...">` | 需添加 `data-i18n-placeholder` |
| ~1400 | `placeholder="例如：100"` | 需添加 `data-i18n-placeholder` |
| ~1401 | `placeholder="例如：20"` | 需添加 `data-i18n-placeholder` |
| ~1432 | `placeholder="搜索会员..."` | 需添加 `data-i18n-placeholder` |
| ~1451 | `<input ... placeholder="按姓名或电话搜索...">` | 需添加 `data-i18n-placeholder` |
| ~1514 | `<input ... placeholder="例如：0123456789" />` (takeaway) | 需添加 `data-i18n-placeholder` |
| ~1516 | `<input ... placeholder="0123456789（可选）" />` | 需添加 `data-i18n-placeholder` |
| ~1518 | `<textarea ... placeholder="例如：少糖、去冰...">` | 需添加 `data-i18n-placeholder` |
| ~1524 | `<input ... placeholder="例如：0123456789" />` (login) | 需添加 `data-i18n-placeholder` |
| ~1530 | `<input ... placeholder="您的姓名" />` | 需添加 `data-i18n-placeholder` |
| ~1531 | `<input ... placeholder="例如：0123456789" />` (reg-phone) | 需添加 `data-i18n-placeholder` |
| ~1532 | `<input ... placeholder="您的邮箱@example.com" />` | 需添加 `data-i18n-placeholder` |
| ~1533 | `<input ... placeholder="例如：0123456789" />` (referrer) | 需添加 `data-i18n-placeholder` |
| ~1610 | `<label>Upload Photo (可选)</label>` | key `uploadPhoto可选`（乱码）→ 改为 `uploadPhotoOpt` |

## 待添加的翻译 key（4 语言）

已在 app.js 中存在但未翻译的语言 key：

- `mItemPrice` → EN='Price (RM)', ZH='价格 (RM)', BM='Harga (RM)', TA='விலை (RM)' ✅
- `mOptional` → EN='optional', ZH='可选', BM='pilihan', TA='விரும்பினால்' ✅

未在字典中的 key（需添加）：

- `mRewardPctDiscountOpt` - 百分比折扣选项
- `mFilterAllC` - 商户投诉"全部"筛选

## 乱码 key

- `uploadPhoto可选` → 应为 `uploadPhotoOpt`（Upload Photo (optional)）

## 部署后验证

需在 https://deploy-eight-rho-95.vercel.app/ 测试：
1. 商户仪表板 → 新项目标签 → "特价 (RM)" 和 "optional" 是否正确显示
2. 投诉页面 → 图片上传标签 → 不再显示乱码

**最后更新：** 2026-05-10 13:05
