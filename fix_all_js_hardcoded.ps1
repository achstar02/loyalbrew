# Comprehensive fix for ALL merchant translation issues in app.js
$file = "C:\Users\Administrator\CodeBuddy\20260416214625\app.js"
$lines = Get-Content $file -Encoding UTF8
$changes = 0

function Fix-Line($idx, $oldText, $newText) {
    global:lines, changes
    if ($global:lines[$idx] -match [regex]::Escape($oldText)) {
        $global:lines[$idx] = $global:lines[$idx].Replace($oldText, $newText)
        $script:changes++
        Write-Host "  FIXED Line $($idx+1): $oldText -> mt('...')"
    } else {
        Write-Host "  SKIP Line $($idx+1): pattern not found"
    }
}

Write-Host "=== FIX 1: Stamp card reward type labels (lines 2521-2540) ==="

# Line 2521: 'Free Menu Item' -> mt('mRewardFreeItem')
Fix-Line 2521 "label.textContent = 'Free Menu Item';" "label.textContent = mt('mRewardFreeItem');"

# Line 2528: 'Discount Amount (RM)' -> mt('mRewardFlatDiscount')
Fix-Line 2528 "label.textContent = 'Discount Amount (RM)';" "label.textContent = mt('mRewardFlatDiscount');"

# Line 2534: 'Discount Percentage (%)' -> mt('mRewardPctDiscount')
Fix-Line 2534 "label.textContent = 'Discount Percentage (%)';" "label.textContent = mt('mRewardPctDiscount');"

# Line 2540: 'Bonus Points Amount' -> mt('mRewardBonusPoints')
Fix-Line 2540 "label.textContent = 'Bonus Points Amount';" "label.textContent = mt('mRewardBonusPoints');"

Write-Host "`n=== FIX 2: New Item select default option (line 2085) ==="
Fix-Line 2085 "'<option value="">-- Choose an item --</option>'" "`'<option value=\"\">' + mt('mChooseAnItem') + '</option>'`"

Write-Host "`n=== FIX 3: Hardcoded English toast messages ==="
# Line 4534
Fix-Line 4534 "showToast(emoji + ' ' + name + ' added!');" "showToast(mt('mItemAdded') || (emoji + ' ' + name + ' added!'), 'success');"

# Line 4541
Fix-Line 4541 "showToast('Item removed');" "showToast(mt('mItemRemoved') || 'Item removed', 'info');"

# Line 2712 - customer stamp preview empty state
Fix-Line 2712 "'<p style=`"color:#aaa;font-size:0.82rem;text-align:center;padding:8px`">No stamp cards available</p>'" "`<p style='color:#aaa;font-size:0.82rem;text-align:center;padding:8px'>${mt('mNoStampCardsYet')}</p>`"

# Line 2700 - No stamp cards available in member list
Fix-Line 2700 "'<small style=`"color:#aaa`">No stamp cards available</small>'" "`<small style='color:#aaa'>${mt('mNoStampCardsYet')}</small>`"

Write-Host "`nTotal JS fixes: $changes"
$lines | Set-Content $file -Encoding UTF8
Write-Host "`nDone! File saved."
