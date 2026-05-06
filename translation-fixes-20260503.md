# LoyalBrew 翻译修复总结

## 修复日期
2026-05-03

## 修复内容

### 1. HTML 裸属性修复 (index.html)

**问题**: 62+ 处使用了裸属性名而不是 `data-i18n` 属性
- `<span members>` 应该是 `<span data-i18n="members">`

**已修复的元素**:
- `members`, `points_issued`, `orders_today`, `revenue_today`
- `add_points_manually`, `phone_number`, `bill_amount`
- `add_new_item`, `item_name`, `price_label`, `category`
- `emoji_icon`, `description`, `item_photo`, `click_to_upload_photo`, `remove_photo`
- `add_to_menu`, `menu_items`, `recent_transactions`
- `deactivate_member`, `confirm_deactivate`, `cancel`
- `launch_new_item`, `select_menu_item`, `announcement_text`
- `active_new_launches`, `past_launches`
- `create_stamp_card`, `card_name`, `card_emoji_icon`
- `stamps_required_to_complete`, `stamp_rule`, `reward_type`, `card_color_theme`
- `active_stamp_cards`, `member_stamp_progress`
- `top_up_bonus_settings`, `add_bonus_rule`, `add_rule`
- `member_wallet_balances`, `top_up_history`, `customer_complaints`
- `generate_table_qr_codes`, `number_of_tables`, `generate_qr_codes`
- `commission_settings`, `commission_records`
- `create_ad`, `ad_title`, `ad_link`, `start_date`, `end_date`
- `ad_image`, `ad_position`, `ad_priority`, `active_ads`
- `hot_drinks`, `cold_drinks`, `food`, `desserts`, `snacks`
- `click_to_upload_ad_image`, `no_active_ads`, `no_ads_yet`

### 2. Settings Promo Engine 硬编码修复 (index.html)

**问题**: "Off-Peak Special Promo Engine" 部分全部使用硬编码英文，没有 i18n

**已修复**:
- `promoEngineTitle`: "Off-Peak Special Promo Engine"
- `promoEngineDesc`: "Auto-show promo prices to customers when your shop is quiet..."
- `enablePromo`: "Enable Promo"
- `startTime`: "Start Time"
- `endTime`: "End Time"
- `activeDays`: "Active Days"
- `busyThreshold`: "Busy Threshold (in-progress orders)"
- `promoHideHint`: "Promo hides when active orders reach this number"
- 星期缩写: `sun`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`

### 3. app.js LANGS 字典补充

**已添加翻译 key 到 4 种语言 (EN/ZH/MS/TA)**:

**英语 (en)**:
- 52个新 key 添加到 LANGS.en
- 包含所有 merchant nav keys, menu item keys, promo engine keys 等

**中文 (zh)**:
- 52个新 key 添加到 LANGS.zh
- 包含所有 merchant keys 的中文翻译
- 修复 MERCHANT_LANGS.zh 中的乱码 (???, ????? 等)

**马来语 (ms)**:
- 52个新 key 添加到 LANGS.ms

**泰米尔语 (ta)**:
- 52个新 key 添加到 LANGS.ta

### 4. MERCHANT_LANGS 修复 (app.js)

**修复了 zh: 块中的乱码**:
- `mCatHotDrinks: '热饮'` (之前是 `??`)
- `mCatColdDrinks: '冷饮'` (之前是 `??`)
- 所有 zh 键从乱码修复为正确的中文

**添加了 promo engine keys** 到所有 4 种语言的 MERCHANT_LANGS:
- `mPromoEngineTitle`, `mPromoEngineDesc`, `mEnablePromo`
- `mStartTime`, `mEndTime`, `mActiveDays`
- `mBusyThreshold`, `mPromoHideHint`
- 星期缩写: `mDaySun` - `mDaySat`

## 验证方法

1. 打开 merchant dashboard
2. 切换语言到中文/马来语/泰米尔语
3. 检查 Settings 页面 → Off-Peak Special Promo Engine 部分
4. 应该显示对应的翻译，不再显示英文

## 可能还需要检查的地方

1. 文件末尾可能有其他乱码需要手动检查
2. 测试所有语言切换功能是否正常工作