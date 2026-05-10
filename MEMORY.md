# MEMORY.md

## LoyalBrew i18n 修复项目
**项目路径：** `C:\Users\Administrator\CodeBuddy\20260416214625\`
**部署地址：** https://deploy-eight-rho-95.vercel.app/
**涉及语言：** EN / 中文 / BM (Malay) / Tamil

---

## 深度分析结论（2026-05-10 13:05 补全）

### 关键数据
| 项目 | 数量 |
|------|------|
| HTML `data-mi18n` key 总数 | 223 |
| MERCHANT_LANGS 字典 key 总数 | 324 |
| HTML key 未在字典中（mt() fallback 处理） | 182 |
| HTML key 在字典中且有翻译 | ~41 |

### mt() / t() snake_case auto-conversion 原理
```javascript
// mt() 中的 fallback：当 key 在字典中找不到时
if (key.indexOf('_') !== -1) {
  var camelKey = 'm' + key.replace(/_([a-z])/g, function(m, c) { return c.toUpperCase(); });
  if (dict[camelKey] !== undefined) return dict[camelKey];
}
// 例：filterAll → 无下划线，不转换 → 返回 'filterAll'
// 例：end_date → mEndDate → 存在于字典 → 返回翻译
```
**关键限制**：auto-conversion 只处理含下划线的 key，无下划线的 key（如 `filterAll`）需要字典中存在。

### 乱码 key
- `uploadPhoto可选`（line 1610）→ 应为 `uploadPhotoOpt`

### 待添加翻译 key（少量）
- `mRewardPctDiscountOpt` - 百分比折扣选项（EN/ZH/BM/TA）
- `mFilterAllC` - 商户投诉"全部"筛选

### 已完成工作（汇总）
1. mt() 和 t() 添加了 snake_case → mCamelCase auto-conversion
2. 商户仪表板 8 处 key 修复（mAddNewItem 等）
3. app.js 中新增 5 个 key（mTitleQuickActions 等）到 4 种语言

---

## 项目背景
- 大量 fix/check 脚本、backup 文件（app.js.bak*）
- 之前已有多次 i18n 修复尝试

## 关键函数位置
- `mt()` 在 app.js — 商户翻译函数（约 line 7275）
- `t()` 在 app.js — 客户翻译函数
- `MERCHANT_LANGS` 在 app.js — 商户语言字典（line 6878-7274，238 keys）
- `LANGS` 在 app.js — 客户语言字典（line 241 开始）

**最后更新时间：** 2026-05-10 13:05
